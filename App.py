def choose_channel():
    while True:
        answer = input("\n\nWybierz kanal: \n-BSC\n-GE (Gilbert-Elliot)\n(Wpisz BSC lub GE)\n").lower()
        if answer == "bsc":
            return 0
        elif answer == "ge":
            return 1
        else:
            print("Musisz wpisac BSC albo GE!")

def initialize_input():
    txt_input = input("Wpisz tekst: " + '\n')
    return txt_input

def string_to_bits(s):
    # Convert each character to its ASCII value, then to its binary representation.
    return ''.join(format(ord(char), '08b') for char in s)

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
    text_input = initialize_input()
    bit_input = string_to_bits(text_input)
    bit_input_reference = bit_input  # reference to unchanged bits

    if channel == 0:
        print("BSC funkcja")
        # Placeholder for BSC error function
        # errors_made = BSC_err(BER, bit_input)
    else:
        print("GE funkcja")
        # Placeholder for GE error function
        # errors_made = GE_err(BER, bit_input)

    # Count final errors (for now this won't work without BSC or GE error functions)
    final_errors = count_differences(bit_input, bit_input_reference)
    print(f"Final number of errors: {final_errors}")

if __name__ == "__main__":
    main()

