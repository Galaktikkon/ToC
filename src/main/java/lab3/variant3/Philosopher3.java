package lab3.variant3;

import lab3.common.Fork;
import lab3.common.Philosopher;

public class Philosopher3 extends Philosopher {

    public Philosopher3(Fork leftFork, Fork rightFork) {
        super(leftFork, rightFork);
    }

    @Override
    public void run() {
        try {
            while (!Thread.currentThread().isInterrupted()) {

                long startWait = System.nanoTime();

//                doAction("Thinking");
                String ThreadName = Thread.currentThread().getName();
                String threadNo = ThreadName.substring(ThreadName.length() - 1);
                if (Integer.parseInt(threadNo) % 2 == 0) {
                    synchronized (leftFork) {

//                        doAction("Picked up left fork");

                        synchronized (rightFork) {

                            totalWaitTime += (System.nanoTime() - startWait);
                            eatCount += 1;

                            doAction("Picked up right fork - eating");

//                            doAction("Put down right fork");
                        }
//                        doAction("Put down left fork. Back to thinking");
                    }
                } else {
                    synchronized (rightFork) {

//                        doAction("Picked up right fork");

                        synchronized (leftFork) {

                            totalWaitTime += (System.nanoTime() - startWait);
                            eatCount += 1;

                            doAction("Picked left fork - eating");

//                            doAction("Put down left fork");
                        }
//                        doAction("Put down right fork. Back to thinking");
                    }
                }
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
