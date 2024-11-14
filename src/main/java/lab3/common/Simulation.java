package lab3.common;

import lab3.variant5.Philosopher5;
import lab3.variant6.Philosopher6;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.lang.reflect.InvocationTargetException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.concurrent.*;

public class Simulation {

    public static void getResults(int low, int high, int step, String filename, int iterations, int maxRuntime, Class<? extends Philosopher> philosopherClass) throws InterruptedException, NoSuchMethodException, InvocationTargetException, InstantiationException, IllegalAccessException {

        ArrayList<Double> res = new ArrayList<>();

        for (int i = low; i <= high; i += step) {
            res.add(Simulation.runSimulation(i, iterations, maxRuntime, philosopherClass));
        }

        System.out.println(res);

        try (BufferedWriter writer = new BufferedWriter(new FileWriter("python\\lab3_results\\"+filename))) {
            for (Double value : res) {
                writer.write(value.toString());
                writer.newLine();
            }
        } catch (IOException e) {
            System.err.println(e.getMessage());
        }
    }

    public static double runSimulation(int numPhilosophers, int iterations, int maxRuntime, Class<? extends Philosopher> philosopherClass) throws InterruptedException, NoSuchMethodException, InvocationTargetException, InstantiationException, IllegalAccessException, InvocationTargetException {

        double[] avgWaitTimes = new double[numPhilosophers];

        for (int i = 0; i < iterations; i++) {

            Fork[] forks = new Fork[numPhilosophers];
            Philosopher[] philosophers = new Philosopher[numPhilosophers];
            Semaphore moderator = new Semaphore(numPhilosophers - 1);

            ExecutorService executor = Executors.newFixedThreadPool(numPhilosophers);

            for (int j = 0; j < numPhilosophers; j++) {
                forks[j] = new Fork();
            }

            for (int j = 0; j < numPhilosophers; j++) {
                Fork leftFork = forks[j];
                Fork rightFork = forks[(j + 1) % numPhilosophers];

                if (philosopherClass == Philosopher5.class || philosopherClass == Philosopher6.class) {
                    philosophers[j] = philosopherClass
                            .getConstructor(Fork.class, Fork.class, Semaphore.class)
                            .newInstance(leftFork, rightFork, moderator);
                } else {
                    philosophers[j] = philosopherClass
                            .getConstructor(Fork.class, Fork.class)
                            .newInstance(leftFork, rightFork);
                }

                philosophers[j].setThinkingTime(1);

                executor.submit(philosophers[j]);
            }

            executor.shutdown();
            if (!executor.awaitTermination(maxRuntime, TimeUnit.SECONDS)) {
                executor.shutdownNow();
            }

            for (int j = 0; j < numPhilosophers; j++) {
                avgWaitTimes[j] += philosophers[j].getWaitTime() == -1 ? maxRuntime : philosophers[j].getWaitTime();
            }
        }

        for (int i = 0; i < avgWaitTimes.length; i++) {
            avgWaitTimes[i] /= iterations;
        }


        return Arrays.stream(avgWaitTimes).average().orElse(0.0);
    }
}
