package lab3.variant2;

import lab3.common.Fork;
import lab3.common.Philosopher;

public class Philosopher2 extends Philosopher {

    public Philosopher2(Fork leftFork, Fork rightFork) {
        super(leftFork, rightFork);
    }

    @Override
    public void run() {
        try {

            while (!Thread.currentThread().isInterrupted()) {

                long startWait = System.nanoTime();

//                doAction("Thinking");

                if (leftFork.tryLock()) {
                    try {
                        if (rightFork.tryLock()) {

                            totalWaitTime += (System.nanoTime() - startWait);
                            eatCount += 1;

                            doAction("Picked up both forks - eating");

//                            doAction("Put down both forks. Back to thinking");

                            rightFork.unlock();
                        }
                    } finally {
                        leftFork.unlock();
                    }
                }
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
