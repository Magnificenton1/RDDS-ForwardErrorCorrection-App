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
    txt_input = input("\nWpisz tekst: " + '\n')
    return txt_input