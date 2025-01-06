import numpy as np
import matplotlib.pyplot as plt
import csv
from LDPC import LDPC

# Functions simulating transmission channels
def bsc_channel(bits, ber):
    return [bit if np.random.rand() > ber else 1 - bit for bit in bits]

def gilbert_elliott_channel(bits, p, r, h, k):
    state = 0  # Start in Good state
    transmitted_bits = []

    for bit in bits:
        if state == 0:
            if np.random.rand() < p:
                state = 1
            error_prob = h
        else:
            if np.random.rand() < r:
                state = 0
            error_prob = k

        if np.random.rand() < error_prob:
            transmitted_bits.append(1 - bit)
        else:
            transmitted_bits.append(bit)

    return transmitted_bits

# Function to simulate and save results
def simulate_and_save_results(channel_fn, channel_name, ldpc_params, input_bits, bers, output_dir_figures, output_dir_csv, word_size, *channel_args):
    results = []
    for ber in bers:
        print(f"Simulating {channel_name} channel with BER={ber}")
        for n, k in ldpc_params:
            ldpc = LDPC(n, k)
            input_chunks = [input_bits[i:i + k] for i in range(0, len(input_bits), k)]
            bit_errors = 0
            for chunk in input_chunks:
                # Pad with zeros if necessary
                if len(chunk) < k:
                    chunk.extend([0] * (k - len(chunk)))
                encoded_bits = ldpc.encode(chunk)
                if channel_name == "GE":
                    transmitted_bits = channel_fn(encoded_bits, *channel_args)
                else:
                    transmitted_bits = channel_fn(encoded_bits, ber)
                decoded_bits = ldpc.decode(transmitted_bits)

                # Correctly compare errors
                if len(decoded_bits) < len(chunk):
                    decoded_bits = np.pad(decoded_bits, (0, len(chunk) - len(decoded_bits)), 'constant')
                elif len(decoded_bits) > len(chunk):
                    decoded_bits = decoded_bits[:len(chunk)]

                bit_errors += np.sum(np.array(chunk) != np.array(decoded_bits))
            results.append((ber, n, k, bit_errors))

    # Save results to CSV file
    csv_file = f"{output_dir_csv}/{channel_name}_results_combined.csv"
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["BER", "n", "k", "t", "Bit Errors"])
        writer.writerows(results)

    return results

# LDPC parameters
ldpc_params = [
    (15, 7),
    (31, 16),
    (63, 32),
    (127, 64)
]

# Word sizes to iterate over (limited to 120 or less)
word_sizes = [4, 5, 7, 11, 26, 39, 50, 57, 120]

# BER range
bers = np.logspace(-6, -2, 20)

# Output directories
output_dir_figures = "../figures"
output_dir_csv = "../CSV"

# Gilbert-Elliott channel parameters
p, r, h, k = 0.01, 0.1, 0.001, 0.8

# Create a plot grid with enough subplots for BSC channel
fig_bsc, axes_bsc = plt.subplots(len(word_sizes), 1, figsize=(12, 5 * len(word_sizes)))
axes_bsc = axes_bsc.flatten()  # Flatten axes for easier iteration

# Create a plot grid with enough subplots for GE channel
fig_ge, axes_ge = plt.subplots(len(word_sizes), 1, figsize=(12, 5 * len(word_sizes)))
axes_ge = axes_ge.flatten()  # Flatten axes for easier iteration

# Loop over the desired word sizes and run the simulation for each
for i, word_size in enumerate(word_sizes):
    print(f"Simulating for word size {word_size}")
    input_bits = np.random.randint(0, 2, word_size).tolist()

    # Simulate for BSC channel
    results_bsc = simulate_and_save_results(bsc_channel, "BSC", ldpc_params, input_bits, bers, output_dir_figures, output_dir_csv, word_size)

    # Simulate for Gilbert-Elliott channel
    results_ge = simulate_and_save_results(gilbert_elliott_channel, "GE", ldpc_params, input_bits, bers, output_dir_figures, output_dir_csv, word_size, p, r, h, k)

    # Get the current axis for plotting for BSC
    ax_bsc = axes_bsc[i]
    # Plot results for BSC
    for n, k in ldpc_params:
        errors_bsc = [r[3] for r in results_bsc if r[1] == n and r[2] == k]
        ax_bsc.plot(bers, errors_bsc, label=f"BSC (n={n}, k={k}, word size={word_size})", marker='o')

    ax_bsc.set_xscale('log')
    ax_bsc.set_xlabel("BER")
    ax_bsc.set_ylabel("Bit Errors")
    ax_bsc.set_title(f"BSC Channel - Word Size {word_size}")
    ax_bsc.grid(True)
    ax_bsc.legend(loc='upper left', bbox_to_anchor=(1.05, 1), ncol=1)  # Add legend for each plot

    # Get the current axis for plotting for GE
    ax_ge = axes_ge[i]
    # Plot results for GE
    for n, k in ldpc_params:
        errors_ge = [r[3] for r in results_ge if r[1] == n and r[2] == k]
        ax_ge.plot(bers, errors_ge, label=f"GE (n={n}, k={k}, word size={word_size})", marker='x')

    ax_ge.set_xscale('log')
    ax_ge.set_xlabel("BER")
    ax_ge.set_ylabel("Bit Errors")
    ax_ge.set_title(f"GE Channel - Word Size {word_size}")
    ax_ge.grid(True)
    ax_ge.legend(loc='upper left', bbox_to_anchor=(1.05, 1), ncol=1)  # Add legend for each plot

# Adjust layout to prevent overlap for BSC and GE and add more space for the legend
fig_bsc.tight_layout(pad=4.0)
fig_ge.tight_layout(pad=4.0)

# Increase figure width for better visibility of the legend
fig_bsc.set_figwidth(15)
fig_ge.set_figwidth(15)

# Save the BSC and GE plots separately
fig_bsc.savefig(f"{output_dir_figures}/bsc_performance_combined.png")
fig_ge.savefig(f"{output_dir_figures}/ge_performance_combined.png")

# Show both plots separately
fig_bsc.show()
fig_ge.show()
