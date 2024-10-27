from BSC_channel import bsc_channel
from GE_channel import gilbert_elliott_channel
from hamming_code import HammingCode
from string_modification import bits_to_string
from string_modification import string_to_bits
from inputs import choose_channel
from inputs import initialize_input

def count_differences(str1, str2):
    # Initialize a counter for differences
    differences = 0
    # Find the length of the shorter string to avoid index errors
    min_len = min(len(str1), len(str2))
    # Compare characters in both strings up to the length of the shorter one
    for i in range(min_len):
        if str1[i] != str2[i]:
            differences += 1
    # Add the length difference between the strings to the differences count
    differences += abs(len(str1) - len(str2))
    return differences

def main():
    channel = choose_channel()
    #need to add BER - bit error rate
    text_input = initialize_input()
    bit_input = string_to_bits(text_input)
    bit_input_reference = bit_input  # reference to unchanged bits

    hamming = HammingCode(len(bit_input))
    bit_input = hamming.encode(bit_input)

    if channel == 0:
        bit_input, flipped_bits = bsc_channel(bit_input)
        # Placeholder for BSC error function
        # errors_made = BSC_err(BER, bit_input)
    else:
        bit_input, flipped_bits = gilbert_elliott_channel(bit_input)
        # Placeholder for GE error function
        # errors_made = GE_err(BER, bit_input)

    # Count final errors (for now this won't work without BSC or GE error functions)
    bit_input = hamming.decode(bit_input)
    final_errors = count_differences(bit_input, bit_input_reference)
    print(f"Original: {bit_input_reference}")
    print(f"\n: {bits_to_string(bit_input_reference)}\n\n")
    print(f"Channel: {bit_input}")
    print(f"\n: {bits_to_string(bit_input)}\n\n")
    print(f"Errors made in channel: {flipped_bits}")
    print(f"Final number of errors: {final_errors}")

if __name__ == "__main__":
    main()

