// Run `java Race.java` from cmdline

public class Race extends Thread {
    public static int counter = 0;

    public static void main(String[] args) {
        var threads = new Thread[8];

        // Create and start threads
        for (int tid = 0; tid < 8; tid++) {
            threads[tid] = new Thread(new Race());
            threads[tid].start();
        }

        // Wait for all threads to finish
        for (int tid = 0; tid < 8; tid++) {
            try {
                threads[tid].join();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

        // Print the final counter value
        System.out.println("counter = " + counter);
    }

    @Override
    public void run() {
        for (int i = 0; i < 100000; i++) {
            counter++;
            System.out.println("counter: " + counter);
        }
    }
}
