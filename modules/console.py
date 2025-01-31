import os
import datetime as dt
import platform

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

    # holds width of widest spinner part
    spinner_width = 0
    for fin in spinner:
        if len(fin) > spinner_width:
            spinner_width = len(fin)

    # delete old log
    try:
        os.remove("log.txt")
    except:
        pass

    # display default state
    def default():
        print(' >>>', end='\r')

    # clears console to remove artifacts
    def clear():

        print(f'\033[H >>>\033[{
              Console.spinner_width+2}C\033[J\033[K', end='\r')

    # when a function is called the spinner indicates execution of code
    # also clears console on execution
    def spinner_spin():
        Console.clear()
        spinner = Console.spinner
        spinner.append(spinner.pop(0))
        print(f'\033[5C{spinner[0]}', end='\r')
        return spinner[0]

    # prints a status next to the spinner for one frame
    # and logs status
    def status(text, spin=True):

        if spin == True:
            Console.spinner_spin()
        print(f'\033[{6+Console.spinner_width}C{text}', end='\r')
        Console.log(text)

    # logs to log.txt
    def log(text):
        with open("log.txt", "a") as f:
            print(f"[{dt.datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S')}] {text}", file=f)
