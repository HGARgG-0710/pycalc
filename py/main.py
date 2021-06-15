from resources import analyze_str, calculate, CommandHandler, History
from os import system, path, chdir

if __name__ == '__main__':
    # * Lately thought of system for auto-updating pycalc :)
    print("Checking for possible updates...")
    chdir(f"{path.dirname(path.dirname(__file__))}")
    system("git pull")

    print("\n")

    commands = {
        "exit": ["--exit", "-e"],
        "help": ["--help", "-h"],
        "history": ["--history", "-hi"]
    }

    history: History = History()
    handler: CommandHandler = CommandHandler(commands, history)

    input_str: str = input("Input expression, that you wish to be calculated or command, "
                           "that you wish to be executed. For help type '-h' or '--help'.\n$ ")

    while True:
        history.add(input_str)
        expression = analyze_str(input_str.strip(), handler)
        calculate(expression)
        input_str = input("\n$ ")
