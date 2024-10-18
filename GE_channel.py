import numpy as np

def gilbert_elliott_channel(input_bits):
    # Ask user for parameters of the Gilbert-Elliott Channel
    while True:
        try:
            p_gb = float(input("\nPodaj p_gb (Probability of Good-to-Bad transition):\n"))
            p_bg = float(input("\nPodaj p_bg (Probability of Bad-to-Good transition):\n"))
            p_g = float(input("\nPodaj p_g (Error probability in Good state):\n"))
            p_b = float(input("\nPodaj p_b (Error probability in Bad state):\n"))
            if all(0.0 <= prob <= 1.0 for prob in [p_gb, p_bg, p_g, p_b]):
                break  # Exit the loop if all probabilities are valid
            else:
                print("Error: Probabilities must be between 0 and 1. Please try again.")
        except ValueError:
            print("Error: Invalid input. Please enter valid float values between 0 and 1.")
    
    # Convert input_bits from string (if needed) to a NumPy array of integers
    if isinstance(input_bits, str):
        input_bits = np.array([int(bit) for bit in input_bits], dtype=int)
    
    # Initialize state to 'Good' (0 = Good, 1 = Bad)
    state = 0  # Start in Good state
    
    # Output bits
    output_bits = np.zeros(len(input_bits), dtype=int)
    
    # Counter for flipped bits
    flipped_bits_count = 0
    
    for i in range(len(input_bits)):
        # Determine error probability based on the current state
        if state == 0:  # Good state
            error_prob = p_g
        else:  # Bad state
            error_prob = p_b
        
        # Generate a random number to see if we flip the bit
        if np.random.rand() < error_prob:
            output_bits[i] = 1 - input_bits[i]  # Flip the bit
            flipped_bits_count += 1  # Increment the flip counter
        else:
            output_bits[i] = input_bits[i]  # No error
        
        # Determine the next state based on transition probabilities
        if state == 0:  # If in Good state
            state = 1 if np.random.rand() < p_gb else 0  # Switch to Bad with probability p_gb
        else:  # If in Bad state
            state = 0 if np.random.rand() < p_bg else 1  # Switch to Good with probability p_bg
    
    return output_bits, flipped_bits_count