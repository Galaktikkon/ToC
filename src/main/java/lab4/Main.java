package lab4;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

class Node {
    Lock lock = new ReentrantLock();
    Object value;
    Node prev;
    Node next;
    public Node(Object value){
        this.value = value;
    }
}

class List extends Node{
    public List() {
        super(null);
    }

    public boolean contains(Object o){

        Node current = this;
        try {
            while (current != null) {

                current.lock.lock();
                if (o.equals(current.value)) {
                    return true;
                }

                Node nextNode = current.next;

                if (nextNode != null) {
                    nextNode.lock.lock();
                }

                current.lock.unlock();
                current = nextNode;
            }

        } finally {
            if(current != null) {
                current.lock.unlock();
            }
        }

        return false;
    }

    public void add(Object o) {
        Node current = this;
        current.lock.lock();

        try {
            while (current.next != null) {

                Node nextNode = current.next;
                nextNode.lock.lock();
                current.lock.unlock();
                current = nextNode;
            }

            Node newNode = new Node(o);
            current.next = newNode;
            newNode.prev = current;

        } finally {
            current.lock.unlock();
        }
    }
}

class Reader extends Thread {

    private final Object toRead;

    private final int readCount;

    private final List list;

    public Reader(Object toRead, int readCount, List list){
        this.toRead = toRead;
        this.readCount = readCount;
        this.list = list;
    }

    public void run(){
        System.out.println("Reader " + this.getName() + " is now reading the list");
        for (int i = 0; i < readCount; i++) {
            if (list.contains(toRead)){
                System.out.println("Reader " + this.getName() + " found element " + toRead.toString());
                return;
            }
            else{
                System.out.println("Reader " + this.getName() + " did not found element " + toRead.toString());
            }
        }
    }
}

public class Main {

    public static void main(String[] args) throws Exception {
        List list = new List();
        list.add("apple");
        list.add("banana");
        list.add("cherry");

        Reader reader1 = new Reader("apple", 5, list);
//        Reader reader2 = new Reader("banana", 5, list);
        Reader reader3 = new Reader("grape", 5, list);

        reader1.start();
//        reader2.start();
        reader3.start();

        reader1.join(1000);
//        reader2.join(100);
        reader3.join(1000);

    }
}
