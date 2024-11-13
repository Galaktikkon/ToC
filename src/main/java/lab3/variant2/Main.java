package lab3.variant2;

import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

class Fork extends ReentrantLock {

}


class Philosopher implements Runnable {

    private Fork leftFork;
    private Fork rightFork;

    public Philosopher(Fork leftFork, Fork rightFork) {
        this.leftFork = leftFork;
        this.rightFork = rightFork;
    }

    @Override
    public void run() {
        try {
            while (true) {

                doAction("Thinking");

                if (leftFork.tryLock()) {
                    try {
                        if (rightFork.tryLock()) {

                                doAction("Picked up both forks - eating");

                                doAction("Put down both forks. Back to thinking");

                                rightFork.unlock();
                        }
                    } finally {

                        leftFork.unlock();
                    }
                }

            }

        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            return;
        }
    }

    private void doAction(String action) throws InterruptedException {
        System.out.println("Philosopher " + Thread.currentThread().getName() + ": " + action);
    }
}


public class Main {

    public static void main(String[] args) throws Exception {
        Philosopher[] philosophers = new Philosopher[5];
        Fork[] forks = new Fork[philosophers.length];

        for (int i = 0; i < forks.length; i++) {
            forks[i] = new Fork();
        }

        for (int i = 0; i < philosophers.length; i++) {
            Fork leftFork = forks[i];
            Fork rightFork = forks[(i + 1) % forks.length];

            philosophers[i] = new Philosopher(leftFork, rightFork);

            Thread t = new Thread(philosophers[i], String.valueOf (i + 1));
            t.start();
        }
    }
}
