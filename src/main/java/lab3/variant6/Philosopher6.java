package lab3.variant6;

import lab3.common.Fork;
import lab3.variant5.Philosopher5;

import java.util.concurrent.Semaphore;

public class Philosopher6 extends Philosopher5 {

    public Philosopher6(Fork leftFork, Fork rightFork, Semaphore moderator) {
        super(leftFork, rightFork, moderator);
    }

    @Override
    public void run() {
        try {
            while (!Thread.currentThread().isInterrupted()) {

                long startWait = System.nanoTime();

//                doAction("Thinking");

                if (moderator.availablePermits() == 0) {

                    if (rightFork.tryLock()) {
                        try {
                            if (leftFork.tryLock()) {

                                totalWaitTime += (System.nanoTime() - startWait);
                                eatCount += 1;

                                doAction("Eating in the hallway (picked right fork first)");
                                leftFork.unlock();
                            }
                        } finally {
                            rightFork.unlock();
                        }
                    }
                } else {

                    moderator.acquire();

                    try {
                        if (leftFork.tryLock()) {
                            try {
                                if (rightFork.tryLock()) {

                                    totalWaitTime += (System.nanoTime() - startWait);
                                    eatCount += 1;

                                    doAction("Eating in the dining room (picked left fork first)");

                                    rightFork.unlock();
                                }
                            } finally {
                                leftFork.unlock();
                            }
                        }
                    } finally {
                        moderator.release();
                    }
                }
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
