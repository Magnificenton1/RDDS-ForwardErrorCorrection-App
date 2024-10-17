from BSC_channel import BSC_err
from GE_channel import GE_err
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

    if channel == 0:
        print("\nBSC funkcja\n")
        # Placeholder for BSC error function
        # errors_made = BSC_err(BER, bit_input)
    else:
        print("\nGE funkcja\n")
        # Placeholder for GE error function
        # errors_made = GE_err(BER, bit_input)

    # Count final errors (for now this won't work without BSC or GE error functions)
    final_errors = count_differences(bit_input, bit_input_reference)
    print(f"Original: {bit_input_reference}")
    print(f"Channel: {bit_input}\n")
    #print(f"Errors made in channel: {errors_made}")
    print(f"Final number of errors: {final_errors}")

if __name__ == "__main__":
    main()

