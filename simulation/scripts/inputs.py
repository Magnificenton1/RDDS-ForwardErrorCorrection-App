def choose_channel():
    """
    Prompts the user to choose a transmission channel.

    Returns:
    int: 0 for BSC (Binary Symmetric Channel), 1 for GE (Gilbert-Elliot Channel).
    """
    while True:
        answer = input("\n\nChoose channel: \n-BSC\n-GE (Gilbert-Elliot)\n(Input BSC or GE)\n").lower()
        if answer == "bsc":
            return 0
        elif answer == "ge":
            return 1
        else:
            print("Must be BSC or GE!")


def choose_correction_code():
    """
    Prompts the user to choose an error correction code.

    Returns:
    int: 0 for RS (Reed-Solomon), 1 for H (Hamming), 2 for BCH (Bose-Chaudhuri-Hocquenghem), 3 for LDPC.
    """
    while True:
        answer = input(
           "\n\nChoose type of error correction code: \n-RS (Reed-Solomon)\n-H (Hamming)\n-BCH (Bose-Chaudhuri-Hocquenghem)\n-LDPC\n(Input RS, H, BCH or LDPC)\n").lower()
        if answer == "rs":
            return 0
        elif answer == "h":
            return 1
        elif answer == "bch":
            return 2
        elif answer == "ldpc":
            return 3
        else:
            print("Must be RS, H, or BCH!")


def initialize_input():
    """
    Prompts the user to input text for transmission.

    Returns:
    str: The input text provided by the user.
    """
    txt_input = input("\nInput text: " + '\n')
    return txt_input