import numpy as np
from inputs import choose_channel, choose_correction_code, initialize_input
from string_modification import string_to_bits, bits_to_string
from BSC_channel import bsc_channel
from GE_channel import gilbert_elliott_channel
from BCH_code import BCHCode
from hamming_code import HammingCode
from ReedSolomon import ReedSolomon


def main():
    print("=== Data Transmission Simulation ===")

    # 1. Get user input
    input_text = initialize_input()
    input_bits = string_to_bits(input_text)
    m = len(input_bits)  # m is the number of data bits (length of input bits)

    print(f"Number of data bits (m): {m}")

    print(f"Original data: {input_bits}")

    # 2. Choose transmission channel
    channel_choice = choose_channel()

    # 3. Choose error correction code
    code_choice = choose_correction_code()

    # 4. Set up simulation parameters
    if code_choice == 0:  # Reed-Solomon
        nsym = int(input("\nEnter the number of correction symbols for RS: "))
        encode_fn = lambda b: ReedSolomon.encode_text_rs(b, nsym)
        decode_fn = lambda eb: ReedSolomon.decode_text_rs(eb, nsym)
    elif code_choice == 1:  # Hamming
        hamming = HammingCode(m)  # Create HammingCode object with m (data bits)
        encode_fn = hamming.encode
        decode_fn = hamming.decode
    elif code_choice == 2:  # BCH
        # Calculate BCH parameters based on the number of data bits
        if m <= 7:
            n = 15
            k = 7
            t = 1  # Error correction capability
        elif m <= 63:
            n = 63
            k = 57
            t = 2
        elif m <= 127:
            n = 127
            k = 113
            t = 3
        elif m <= 255:
            n = 255
            k = 223
            t = 4
        else:
            print("Error: Input size too large for BCH coding.")
            return

        bch = BCHCode(n, k, t)
        encode_fn = bch.encode
        decode_fn = bch.decode
        print(f"Using BCH code with n={n}, k={m}, t={t}.")
    else:
        print("Unsupported correction code!")
        return

    # 5. Encode data
    encoded_bits = encode_fn(input_bits)
    print("\nEncoded data: ", encoded_bits)

    # 6. Transmit through the chosen channel
    if channel_choice == 0:  # BSC
        transmitted_bits = bsc_channel(encoded_bits)
    elif channel_choice == 1:  # Gilbert-Elliot
        transmitted_bits = gilbert_elliott_channel(encoded_bits)
    else:
        print("Unsupported transmission channel!")
        return

    print("\nData after channel transmission: ", transmitted_bits)

    # 7. Decode data
    # If transmitted_bits is a tuple (which can happen in some channels), take the first element
    if isinstance(transmitted_bits, tuple):
        transmitted_bits = transmitted_bits[0]  # Take the array part of the tuple

    transmitted_bits = np.array(transmitted_bits, dtype=int).tolist()
    decoded_bits = decode_fn(transmitted_bits)
    if decoded_bits[0] != input_bits[0]:
        decoded_bits = np.insert(decoded_bits, 0, 0)
    print("\nDecoded data: ", decoded_bits)

    # 8. Convert to text
    try:
        output_text = bits_to_string(decoded_bits)
        print("\nReceived text: ", output_text)
    except Exception as e:
        print("\nError decoding to text: ", str(e))
        output_text = None

    # 9. Analyze results
    bit_errors = np.sum(input_bits != decoded_bits[:len(input_bits)])
    ber = bit_errors / len(input_bits)
    print("\n=== Simulation Results ===")
    print(f"Number of bit errors: {bit_errors}")
    print(f"BER (Bit Error Rate): {ber:.4f}")
    if output_text:
        print(f"Received text matches original: {output_text == input_text}")


if __name__ == "__main__":
    main()
