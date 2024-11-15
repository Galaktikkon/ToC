package lab1;

class Watek extends Thread {

    private final int counter;
    private static boolean isShot = false;

    public Watek(int counter){
        this.counter = counter;
    }

    public void run(){
        for (int i = 0; i < counter; i++) {
            System.out.println(i);
            if(isShot){
                try {
                    this.join(1);
                    break;
                } catch (InterruptedException e) {
                    throw new RuntimeException(e);
                }
            }
        }
        if(!isShot){
            isShot = true;
            System.out.println("Pif!Paf!");
        }
    }
}

public class Main {
    public static void main(String[] args) {
        final int n = Integer.parseInt(args[0]);
//        ExecutorService exec = Executors.newFixedThreadPool(n);
//        exec.execute(new Watek(n));
//        exec.shutdown();
        for (int i = 0; i < n; i++) {
            Watek w = new Watek(n);
            w.start();
        }
    }
}