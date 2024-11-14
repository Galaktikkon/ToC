package lab3.variant5;

import lab3.common.Fork;
import lab3.common.Philosopher;

import java.util.concurrent.Semaphore;

public class Philosopher5 extends Philosopher {

    protected final Semaphore moderator;

    public Philosopher5(Fork leftFork, Fork rightFork, Semaphore moderator) {
        super(leftFork, rightFork);
        this.moderator = moderator;
    }

    @Override
    public void run() {
        try {
            while (!Thread.currentThread().isInterrupted()) {

                long startWait = System.nanoTime();

//                doAction("Thinking");

                moderator.acquire();

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

                moderator.release();
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
