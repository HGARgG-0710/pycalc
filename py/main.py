import math
from resources import analyze_str, calculate, CommandHandler, History, DefinitionHandler, FunctionCallHandler, Parser
from os import system, path, chdir

def loop (input_phrase: str, history: History, cmdhandler: CommandHandler, parser: Parser): 
	history.add(input_phrase)
	calculate(analyze_str(input_phrase.strip(), cmdhandler, parser))

if __name__ == '__main__':
	# * Lately thought of system for auto-updating pycalc :)
	print("Checking for possible updates...")
	chdir(f"{path.dirname(path.dirname(__file__))}")
	system("git pull")

	print("\n")

	commands: dict = {
		"exit": ["--exit", "-e"],
		"help": ["--help", "-h"],
		"history": ["--history", "-hi"], 
		"readdef": ["--readvar", "-rv"], 
		"makedef": [ "--definevars", "-dv"], 
		"setdef": ["--setvar", "-sv"], 
		"listdefs": ["--listvars", "-lv"], 
		"deldef": ["--deletevars", "-delv"]
	}

	predefined: dict = {
		"pi": math.pi,  
		"e": math.e, 
		"phi": (1+math.sqrt(5))/2
	} 

	functions = ()

	defhandler: DefinitionHandler = DefinitionHandler(predefined)
	funchandler: FunctionCallHandler = FunctionCallHandler(functions) 
	history: History = History()
	cmdhandler: CommandHandler = CommandHandler(commands, history, defhandler, funchandler)
	
	# TODO: extend this thing, pray [id est, add many more operators]...
	# todo: generalize the thing in question (let arbitrarily many places be allowed for an operator -- not just binary); 
	# TODO: pray add a way of creating one's own functions within the calculator's context; 
	parser = Parser(cmdhandler, ["+", "-", "*", "/", "%", "#", "^"])
	cmdhandler._parser = parser

	errindex: int = 0 
	input_str: str = input("Input expression, that you wish to be calculated or command, "
						   "that you wish to be executed. For help type '-h' or '--help'.\n$ ")

	while True:
		try: 
			if errindex == 0: 
				loop(input_str, history, cmdhandler, parser)
				input_str = input("\n$ ")
			else: 
				loop(input("\n$ "), history, cmdhandler, parser) 
		except Exception as e: 
			# print("UnknownError: your input caused an unexpected exception to occur (error text: " + str(e) + ")") 
			raise e 
			# errindex += 1 
