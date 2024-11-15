package lab3.common;

public abstract class Philosopher implements Runnable {

    private static int thinkingTime;
    protected final Fork leftFork;
    protected final Fork rightFork;
    protected long totalWaitTime = 0;
    protected int eatCount = 0;

    public Philosopher(Fork leftFork, Fork rightFork) {
        this.leftFork = leftFork;
        this.rightFork = rightFork;
    }

    public void setThinkingTime(int time) {
        thinkingTime = time;
    }

    public double getWaitTime() {
        return eatCount == 0 ? -1 : (((double) totalWaitTime / eatCount) / 1e9);
    }

    @Override
    abstract public void run();

    protected void doAction(String action) throws InterruptedException {
//        System.out.println("Philosopher " + Thread.currentThread().getName() + ":  " + action);
        Thread.sleep(Philosopher.thinkingTime);
    }

}
