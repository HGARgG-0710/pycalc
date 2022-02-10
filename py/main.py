from resources import analyze_str, calculate, CommandHandler, History
from os import system, path, chdir

def loop (input_phrase: str, history: History, handler: CommandHandler): 
    history.add(input_phrase)
    expression = analyze_str(input_phrase.strip(), handler)
    calculate(expression)

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
    errindex: int = 0 

    input_str: str = input("Input expression, that you wish to be calculated or command, "
                           "that you wish to be executed. For help type '-h' or '--help'.\n$ ")

    while True:
        try: 
            if errindex == 0: 
                loop(input_str, history, handler) 
                input_str = input("\n$ ")
            else: 
                loop(input("\n$"), history, handler) 
        except Exception: 
            print("UnknownError: your input caused an unexpected exception to occur. \n") 
            errindex += 1 
