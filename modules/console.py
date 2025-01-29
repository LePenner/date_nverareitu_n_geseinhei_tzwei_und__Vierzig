import os

# class to display spinner and a status, log any displayed messages


class Console():

    # please edit spinner speed from main.py
    spinner_speed = 0
    spinner = ['/', '-', '\\', '|']

    # spinners at https://github.com/manrajgrover/py-spinners/blob/master/spinners/spinners.py
    # alt spinners:

    # spinner = [".", "o", "O", "o"]
    # spinner = ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█", "▇", "▆", "▅", "▄", "▃", "▂", "▁"]
    # spinner = ["o", " o", "  o", "   o", "    o", "     o", "      o", "       o"]
    # spinner = ["⠁", "⠉", "⠒", "⠤", "⠦", "⠴", "⠶", "⠷", "⠿"]
    # spinner = ["⊶", "⊷"]
    # spinner = ["■", "□"]

    spinner_width = 0
    for fin in spinner:
        if len(fin) > spinner_width:
            spinner_width = len(fin)

    def init():
        print(' >>>', end='\r')

    def clear():
        os.system('cls')
        Console.init()

    # when a function is called the spinner indicates execution of code
    # also clears console on execution
    def spinner_spin():
        Console.clear()
        spinner = Console.spinner
        spinner.append(spinner.pop(0))
        print(f'\033[5C{spinner[0]}', end='\r')
        return spinner[0]

    def status(text, spin=True):

        if spin == True:
            Console.spinner_spin()
        print(f'\033[{6+Console.spinner_width}C{text}', end='\r')
