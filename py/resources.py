class History:
    def __init__(self):
        self._history = []

    def get(self):
        return self._history

    def add(self, command: str):
        self._history.append(command)

class DefinitionHandler: 
    def __init__(self, predefined: dict = {}):
        self.definitions:dict = predefined
    
    def define(self, name:str, value:str) -> None: 
        if (name in self.definitions.keys()):
            print("DefineError: You have already defined the given variable. ")
            return
        self.definitions[name] = value

    def setval(self, name:str, value:str) -> None:
        if (name in self.definitions.keys()): 
            self.definitions[name] = value
            return
        print("SetValueError: The given variable name is not defined. First define it. ")       

    def readval(self, name: str) -> str: 
        return self.definitions[name]

    def listdefs(self) -> dict: 
        return self.definitions

class FunctionCallHandler: 
    def __init__(self, functions: tuple): 
        self.functions:tuple = functions

    def getfuncvalue(index: int, value): 
        return self.function[index](value)

    def getfuncindex(funcname:str):
        return self.index(funcname)

class CommandHandler:
    def __init__(self, commands: dict, history: History, defhandler: DefinitionHandler, funchandler: FunctionCallHandler):
        self.allowedCommands = commands

        self._history = history
        self._defhandler = defhandler
        self._funchandler = funchandler

    def handle(self, command: str, additional:str = ""):
        command = command.strip(" ")

        if command in self.allowedCommands["exit"]:
            from sys import exit
            print("Goodbye!")
            exit()
        elif command in self.allowedCommands["help"]:
            print("To exit the app type command '-e' or '--exit'. \n"
                  "To see your history type '-hi' or '--history' command.\n\n"
                  "Operators: \n"
                  "1. division: /\n"
                  "2. addition: +\n"
                  "3. subtraction: -\n"
                  "4. multiplication: *\n"
                  "5. taking the remainder of the division: %\n"
                  "6. exponentiation: ^\n"
                  "7. whole division: #\n\n"
                  "To specify a float number type the 'f' letter and only then the number itself. \n"
                  "Example: f4.2\n\n"
                  "To specify a negative number type the 'n' letter and only then the number itself (note: do NOT write the 'minus' sign).\n"
                  "Example: n42\n"
                  "This would give you the -42 result\n"
                  "Example of a negative float number: fn84.6\n\n"
                  "Also you can use brackets:\n"
                  "(fn32.6 + fn55.1) ^ fn8.33\n\n"
                  "If you need to get exchange rate from one currency to another "
                  "(for example, to get rubles from dollars), then you can do this too.\n"
                  "Example: dr\n"
                  "First letter is the original currency (USD) "
                  "and the second one is target currency (RUB, in this exact case).\n"
                  "Also they can be capital letters.\n"
                  "Currencies, that are allowed: \n  "
                  "USD - d,\n  RUB - r,\n  INR - i,\n  UAH - u,\n  EUR - e,\n  "
                  "CNY - y,\n  GBP - b,\n  CAD - c,\n  JPY - j\n\n"
                  "And those can be used in actual mathematical expressions.\n"
                  "Example: 40000 * dr, will give you the amount of rubles that there are in 40000 dollars.\n\n"
                  "Wish you happy using!\n"
                  )
        elif command in self.allowedCommands["history"]:
            print("History:\n")
            for i in range(0, len(self._history.get())):
                print(str(i+1) + ".", self._history.get()[i])
        elif command in self.allowedCommands["listdefs"]: 
            defs:dict = self._defhandler.listdefs()
            keys: list = list(defs.keys())

            print("Variables:")
            for i in range(len(defs)): 
                print(str(i + 1) + "." + keys[i] + " = " + str(defs[keys[i]]))
        elif command[:3] in self.allowedCommands["makedef"] or command[:12] in self.allowedCommands["makedef"]: 
            defs: list = [list(filter(lambda x: x != "", q)) for q in [a.split(" ") for a in [s.strip() for s in additional.split(",")]]]
            for i in range(len(defs)): 
                self._defhandler.define(defs[i][0], calculate(analyze_str(defs[i][1], self), False, True))
                print("Variable added: " + defs[i][0] + " = " + str(self._defhandler.readval(defs[i][0])))
        elif command in self.allowedCommands["setdef"]: 
            pass # TODO: Make a body later
        elif command in self.allowedCommands["readdef"]: 
            pass # TODO: Make a body later 
        else:
            print("Error: Unknown command inputted.")

    def getHistory(self) -> History:
        return self._history

    def getFuncHandler(self) -> FunctionCallHandler: 
        return self._funchandler

    def getDefHandler(self) -> DefinitionHandler: 
        return self._defhandler

def analyze_str(input_str: str, cmdhandler: CommandHandler) -> tuple:
    numbers = []
    operators = []

    index = 0

    for _ in input_str:
        if index >= len(input_str):
            break

        char = input_str[index]

        # checking whether current char is an integer or not
        # (I know there is a function for doing it, but still)
        try:
            int(char)
            t = "int"
        except ValueError:
            t = "float" if char == "f" else "str" if char != "n" else "int"

        if t == "int":
            is_negative = char == "n"
            numbers += ([char] if not is_negative else ["(-"])
            index += 1
            while True:
                try:
                    curr_symbol = input_str[index if index < len(
                        input_str) else index - 1]
                    int(curr_symbol)  # checking if a number

                    if index == len(input_str):
                        raise ValueError("break")

                    index += 1
                    numbers[len(numbers) - 1] += curr_symbol
                except ValueError:
                    if is_negative:
                        numbers[len(numbers) - 1] += ")"
                    break
        elif t == "str":
            from re import match
            allowed_operators = ["+", "-", "*", "/", "%", "#", "^"]

            if char == "-" and index == 0:
                # command
                cmdhandler.handle(input_str, " ".join(input_str.split(" ")[1:]))
                input_str = input("\n$ ")
                cmdhandler.getHistory().add(input_str)

                return analyze_str(input_str, cmdhandler)
            elif char in allowed_operators:
                # operator
                operators += char
            elif char == "(" or char == ")":
                # bracket
                operators += ["+"]
                numbers += [("0" if char == ")" else "") +
                            char + ("0" if char == "(" else "")]

            elif match("[A-Za-z]", char):
                index += 1
                numbers += ["(" + eval_currency(char.upper(),
                                                input_str[index].upper()), "0)"]
                operators += ["+"]
            else:
                if char != " ":
                    print("Error: Invalid character " + char + " inputted.")
                    return (), ()
            index += 1
        elif t == "float":
            is_negative = input_str[index + 1] == "n"
            numbers += (input_str[index + 1]
                        if not is_negative else ["(-"])
            index += 2
            while True:
                try:
                    curr_symbol = input_str[index if index < len(
                        input_str) else index - 1]

                    if(curr_symbol != "." and curr_symbol != ","):
                        int(curr_symbol)
                        index += 1
                    else:
                        numbers[len(numbers) - 1] += "."
                        index += 1
                        continue

                    numbers[len(numbers) - 1] += curr_symbol

                    if index == len(input_str):
                        raise ValueError("Ended")

                except ValueError:
                    if is_negative:
                        numbers[len(numbers) - 1] += ")"
                    break

    return numbers, operators

def calculate(expression: tuple, should_output = True, should_return = False):
    nums = expression[0]
    operators = expression[1]
    expr = ""

    for i in range(0, len(nums)):
        expr += nums[i]
        if i != len(nums) - 1:
            expr += operator_evaluator(operators[i])

    if expr != "":
        result = eval(expr)
        if should_output:
            print(result)

    return result if should_return else None

def operator_evaluator(operator: str):
    common_operators = ["+", "-", "*", "/", "%"]
    return operator if operator in common_operators else \
        "//" if operator == "#" else "**"

def eval_currency(originalCurrency:str, targetCurrency:str):
    from requests import get

    # * note: this does not depend upon the fact if
    # * the currency is acceptable or not!
    if originalCurrency.upper() == targetCurrency.upper():
        return "1"

    currency_names:dict = {
        "D": "USD",
        "E": "EUR",
        "R": "RUB",
        "U": "UAH",
        "I": "INR",
        "Y": "CNY",
        "B": "GBP",
        "J": "JPY",
        "C": "CAD"
    }

    if originalCurrency.upper() not in currency_names or targetCurrency.upper() not in currency_names:
        err_currency = originalCurrency if originalCurrency.upper(
        ) not in currency_names else targetCurrency

        print(f"Error: no such currency as {err_currency}")
        return "0"

    original:str = currency_names[originalCurrency]
    target:str = currency_names[targetCurrency]

    address:str = r"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE"
    query_text:str = f"{address}&from_currency={original}&to_currency={target}&apikey=H88SANVRLLXS7BD9"

    result = get(query_text).json()
    exchange_rate = result["Realtime Currency Exchange Rate"]["5. Exchange Rate"]

    return exchange_rate
