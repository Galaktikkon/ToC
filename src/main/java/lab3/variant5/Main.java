package lab3.variant5;

class Philosopher implements Runnable {

    private Object leftFork;
    private Object rightFork;

    public Philosopher(Object leftFork, Object rightFork) {
        this.leftFork = leftFork;
        this.rightFork = rightFork;
    }

    @Override
    public void run() {
        try {
            while (true) {


                doAction("Thinking");
                synchronized (leftFork) {
                    doAction("Picked up left fork");
                    synchronized (rightFork) {

                        doAction("Picked up right fork - eating");

                        doAction("Put down right fork");
                    }


                    doAction("Put down left fork. Back to thinking");
                }
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            return;
        }
    }

    private void doAction(String action) throws InterruptedException {
        System.out.println("Philosopher " + Thread.currentThread().getName() + ":  " + action);
        Thread.sleep(((int) (Math.random() * 100)));
    }
}


public class Main {

    public static void main(String[] args) throws Exception {
        Philosopher[] philosophers = new Philosopher[5];
        Object[] forks = new Object[philosophers.length];

        for (int i = 0; i < forks.length; i++) {
            forks[i] = new Object();
        }

        for (int i = 0; i < philosophers.length; i++) {
            Object leftFork = forks[i];
            Object rightFork = forks[(i + 1) % forks.length];

            philosophers[i] = new Philosopher(leftFork, rightFork);

            Thread t = new Thread(philosophers[i], String.valueOf (i + 1));
            t.start();
        }
    }
}
