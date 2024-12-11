import numpy as np
import matplotlib.pyplot as plt
import csv
from concurrent.futures import ThreadPoolExecutor
from BCH_code import BCHCode

# Functions simulating transmission channels
def bsc_channel(bits, ber):
    return [bit if np.random.rand() > ber else 1 - bit for bit in bits]

def gilbert_elliott_channel(bits, p, r, h, k):
    state = 'G'  # Start in Good state
    transmitted_bits = []

    for bit in bits:
        if state == 'G':
            if np.random.rand() < p:
                state = 'B'
            error_prob = h
        else:
            if np.random.rand() < r:
                state = 'G'
            error_prob = k

        if np.random.rand() < error_prob:
            transmitted_bits.append(1 - bit)
        else:
            transmitted_bits.append(bit)

    return transmitted_bits

# Function to simulate and save results
def simulate_and_save_results(channel_fn, channel_name, bch_params, input_bits, bers, output_dir_figures, output_dir_csv, *channel_args):
    results = []
    for ber in bers:
        print(f"Simulating {channel_name} channel with BER={ber}")
        for n, k, t in bch_params:
            bch = BCHCode(n, k, t)
            input_chunks = [input_bits[i:i + k] for i in range(0, len(input_bits), k)]
            bit_errors = 0
            for chunk in input_chunks:
                # Pad with zeros if necessary
                if len(chunk) < k:
                    chunk.extend([0] * (k - len(chunk)))
                encoded_bits = bch.encode(chunk)
                if channel_name == "GE":
                    transmitted_bits = channel_fn(encoded_bits, *channel_args)
                else:
                    transmitted_bits = channel_fn(encoded_bits, ber)
                decoded_bits = bch.decode(transmitted_bits)

                # Correctly compare errors
                if len(decoded_bits) < len(chunk):
                    decoded_bits = np.pad(decoded_bits, (0, len(chunk) - len(decoded_bits)), 'constant')
                elif len(decoded_bits) > len(chunk):
                    decoded_bits = decoded_bits[:len(chunk)]

                bit_errors += np.sum(np.array(chunk) != np.array(decoded_bits))
            results.append((ber, n, k, t, bit_errors))

    # Save results to CSV file
    csv_file = f"{output_dir_csv}/{channel_name}_results.csv"
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["BER", "n", "k", "t", "Bit Errors"])
        writer.writerows(results)

    # Generate plot
    plt.figure()
    for n, k, t in bch_params:
        errors = [r[4] for r in results if r[1] == n and r[2] == k and r[3] == t]
        plt.plot(bers, errors, label=f"BCH (n={n}, k={k}, t={t})")

    plt.xlabel("BER")
    plt.ylabel("Bit Errors")
    plt.title(f"Error Correction Performance in {channel_name} Channel")
    plt.legend(loc='upper right',bbox_to_anchor=(1, 1))
    plt.grid(True)
    plt.xscale('log')
    plt.savefig(f"{output_dir_figures}/{channel_name}_performance.png")
    plt.show()
    plt.close()

# BCH parameters
bch_params = [
    (7, 4, 1),
    (15, 11, 1),
    (15, 7, 2),
    (15, 5, 3),
    (31, 26, 1),
    (31, 11, 4),
    (63, 57, 1),
    (63, 39, 5),
    (127, 120, 1),
    (127, 50, 6)
]

# Input data
word_size = int(input("Enter the size of the input data (must be less than 255):\n"))
input_bits = np.random.randint(0, 2, word_size).tolist()

# BER range
bers = np.logspace(-6, -2, 20)

# Output directories
output_dir_figures = "../figures"
output_dir_csv = "../CSV"

# Gilbert-Elliott channel parameters
p, r, h, k = 0.1, 0.1, 0.01, 0.1

# Simulation
with ThreadPoolExecutor() as executor:
    futures = [
        executor.submit(simulate_and_save_results, bsc_channel, "BSC", bch_params, input_bits, bers, output_dir_figures, output_dir_csv),
        executor.submit(simulate_and_save_results, gilbert_elliott_channel, "GE", bch_params, input_bits, bers, output_dir_figures, output_dir_csv, p, r, h, k)
    ]
    for future in futures:
        future.result()  # Wait for all threads to complete