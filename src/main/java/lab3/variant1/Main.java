package lab3.variant1;

import lab3.common.Simulation;

import java.lang.reflect.InvocationTargetException;

public class Main {

    public static void main(String[] args) throws InterruptedException, InvocationTargetException, NoSuchMethodException, InstantiationException, IllegalAccessException {
        System.out.println(Simulation.runSimulation(5, 5, 5, Philosopher1.class));
    }
}
