package lab2;

import java.util.LinkedList;
import java.util.Queue;

class UnikalneNumery {
    private static int numerId = 0;

    public synchronized static int nowyID() {
        return numerId++;
    }
}

class Buffer {
    private final int size;
    private final Queue<Integer> buffer = new LinkedList<>();

    public Buffer(int m) {
        this.size = m;
    }

    public synchronized void put(int i) throws InterruptedException {
        while (buffer.size() == size) {
            System.out.println("Bufor jest pełny!");
            wait();
        }
        buffer.add(i);
        notifyAll();
    }

    public synchronized int get() throws InterruptedException {
        while (buffer.isEmpty()) {
            System.out.println("Bufor jest pusty!");
            wait();
        }
        int item = buffer.remove();
        notifyAll();
        return item;
    }
}

class Producer extends Thread {
    private final Buffer _buf;
    public final int id;

    public Producer(Buffer buffer) {
        this._buf = buffer;
        this.id = UnikalneNumery.nowyID();
    }

    public void run() {
        while (true) {
            try {
                int new_id = UnikalneNumery.nowyID();
                _buf.put(new_id);
                System.out.println("Producent " + id + " produkuje pizze " + new_id);
                Thread.sleep(1000);
            } catch (InterruptedException ignored) {
            }
        }
    }
}

class Consumer extends Thread {
    private final Buffer _buf;
    public final int id;

    public Consumer(Buffer buffer) {
        this._buf = buffer;
        this.id = UnikalneNumery.nowyID();
    }

    public void run() {
        while (true) {
            try {
                int item = _buf.get();
                System.out.println("Konsument K" + id + " zjada pizze " + item);
                Thread.sleep(500);
            } catch (InterruptedException ignored) {
            }
        }
    }
}

class Pipe {

    public Pipe(Buffer buffer_in, Buffer buffer_out,  int pipe_id) {
        this.buffer_in = buffer_in;
        this.buffer_out = buffer_out;
        this.pipe_id = pipe_id;
    }

    private final Buffer buffer_in;
    private final Buffer buffer_out;
    private final int pipe_id;

    public void run() {
        while (true) {
            try {
                buffer_in.get();
                System.out.println("Pisarz " + pipe_id + " pisze do czytelnika " + pipe_id + 1);
                Thread.sleep(1000);
                buffer_out.put(UnikalneNumery.nowyID());
            } catch (InterruptedException ignored) {
            }
        }
    }
}



public class SymulacjaPK {
    public static void main(String[] args) {
        Buffer buffer = new Buffer(4);
        for (int i = 0; i < 100; i++) {

        }
    }
}
