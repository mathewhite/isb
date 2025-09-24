import java.util.Random;

/**
 *class generates a pseudorandom binary sequence of 128 bit
 */
public class RandomGenerator {

    /**
    * generates and prints to the console a 128-bit binary sequence
    *
    * <p>uses {@link java.util.Random} to generate random numbers 0 or 1</p>
    */
    public static void generate_128() {
        Random rand = new Random();
        StringBuilder sequence = new StringBuilder();

        for (int i = 0; i < 128; ++i) {
            sequence.append(rand.nextInt(2));
        }

        System.out.println("generated seq:");
        System.out.println(sequence.toString());
    }

    public static void main(String[] args) {
        generate_128();
    }
}