def choose_channel():
    while True:
        answer = input("\n\nChoose channel: \n-BSC\n-GE (Gilbert-Elliot)\n(Input BSC or GE)\n").lower()
        if answer == "bsc":
            return 0
        elif answer == "ge":
            return 1
        else:
            print("Must be BSC or GE!")


def choose_correction_code():
    while True:
        answer = input(
            "\n\nChoose type of error correction code: \n-RS (Reed-Solomon)\n-H (Hamming)\n(Input RS or H)\n").lower()
        if answer == "rs":
            return 0
        elif answer == "h":
            return 1
        else:
            print("Must be RS or H!")


def initialize_input():
    txt_input = input("\nInput text: " + '\n')
    return txt_input
