package lab3.variant6;

import java.lang.reflect.InvocationTargetException;

import static lab3.common.Simulation.getResults;

public class Main {
    public static void main(String[] args) throws InterruptedException, InvocationTargetException, NoSuchMethodException, InstantiationException, IllegalAccessException {
        getResults(5, 100, 5,"results6.txt", 5, 5, Philosopher6.class);
    }
}
