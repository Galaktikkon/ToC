package lab3.variant1;

import lab3.common.Fork;
import lab3.common.Philosopher;

public class Philosopher1 extends Philosopher {

    public Philosopher1(Fork leftFork, Fork rightFork) {
        super(leftFork, rightFork);
    }

    @Override
    public void run() {
        try {
            while (!Thread.currentThread().isInterrupted()) {

                long startWait = System.nanoTime();

//                doAction("Thinking");

                synchronized (leftFork) {

//                    doAction("Picked up left fork");

                    synchronized (rightFork) {

                        totalWaitTime += (System.nanoTime() - startWait);
                        eatCount += 1;

                        doAction("Picked up right fork - eating");

//                        doAction("Put down right fork");
                    }

//                    doAction("Put down left fork. Back to thinking");
                }
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

}
