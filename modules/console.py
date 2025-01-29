import os


class Console():

    spinner_speed = 0
    spinner = ['/', '-', '\\', '|']

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
        print(f'\033[7C{text}', end='\r')
