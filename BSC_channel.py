import numpy as np

import numpy as np

def bsc_channel(input_bits):
    while True:
        try:
            ber = float(input("\nInput BER (must be between 0.00 and 1.00):\n"))
            if 0.0 <= ber <= 1.0:
                break  # Exit the loop if valid
            else:
                print("Error: BER must be between 0 and 1. Please try again.")
        except ValueError:
            print("Error: Invalid input. Please enter a float value between 0 and 1.")
    
    # Convert input_bits from string (if needed) to a NumPy array of integers
    """
    if isinstance(input_bits, str):
        input_bits = np.array([int(bit) for bit in input_bits], dtype=int)
    """
    input_bits = np.array([int(bit) for bit in input_bits], dtype=int)

    # Generate random numbers for each bit to simulate errors
    random_values = np.random.rand(len(input_bits))
    
    # Flip bits based on the BER
    output_bits = np.where(random_values < ber, 1 - input_bits, input_bits)
    
    # Count the number of bits that were flipped
    flipped_bits_count = np.sum(output_bits != input_bits)
    
    return output_bits, flipped_bits_count

