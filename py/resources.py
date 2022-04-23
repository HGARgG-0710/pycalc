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
    
    def define(self, name:str, value:str): 
        if (name in self.definitions.keys()):
            print("DefineError: You have already defined the given variable. ")
            return 0
        self.definitions[name] = value

    def setval(self, name:str, value:str):
        if (name in self.definitions.keys()): 
            self.definitions[name] = value
            return
        print("SetValueError: The given variable name is not defined. First define it. ")       
        return 0

    def readval(self, name: str) -> str: 
        return self.definitions[name]

    def listdefs(self) -> dict: 
        return self.definitions

    def deletevar(self, varname: str): 
        return self.definitions.pop(varname, None)

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

    def handle(self, command: str, additional:str = "", should_return: bool = False):
        command = command.strip(" ")

        if command in self.allowedCommands["exit"]:
            from sys import exit
            print("Goodbye!")
            exit()
        elif command in self.allowedCommands["help"]:
            print("\nCommands: \n\n"
                  "\t1. (--exit, -e): exit the pycalc; \n"
                  "\t2. (--history, -hi): history, output the already provided commands; \n"
                  "\t3. (--help, -h): help, give this particulare list; \n"
                  "\t4. (--definevars, -dv) [varname1 varvalue1, ..., varname_n varvalue_n]: create new variables varname1, ..., varname_n and assign to them values varvalue1, ..., varvalue_n correspondently (they are arbitrary pycalc commands); \n"
                  "\t5. (--listvars, -lv): lists all of the defined variables; \n"
                  "\t6. (--readvars, -rv) [expression]: executes an expression with variables and arithmetic (without currency, it won't work); \n"
                  "\t7. (--setvars, -sv) [varname1 varvalue1, ..., varname_n varvalue_n]: sets values varvalue_1, ..., varvalue_n to already existing variables varname1, ..., varname_n correspondently. \n"
                  "\t8. (--deletevars, -delv) [varname1, ..., varname_n]: deletes the already existing variables varname1, ..., varname_n. "
                  "\n\nArithmetic: \n\n"
                  "\t1. Addition: a+b; \n"
                  "\t2. Subtraction: a-b; \n"
                  "\t3. Additive inverse: na (Example: n42); \n"
                  "\t4. Multiplication: a*b; \n"
                  "\t5. Division: a/b; \n"
                  "\t6. Exponentiation: a^b; \n"
                  "\t7. Whole division: a#b; \n"
                  "\t8. Remainder of division: a%b; \n"
                  "\t9. Brackets: (a) (They can help with the order of operations, it is as in BOMDAS); \n"
                  "\t10. Floating numbers: they are given as fa.b or fa,b (example: f42.42, fn42.42 [= -42.42])"
                  "\n\nCurrency exchange: \n\n"
                  "\t1. Syntax: it is as xy, where x, y are the currency letters. This essentially means \"how many currency y in x\" (Letters may also be capital: xY); \n"
                  "\t2. Letters: \n\n"
                  "\t\t2.1. RUB - r; \n"
                  "\t\t2.2. USD - d; \n"
                  "\t\t2.3. INR - i; \n"
                  "\t\t2.4. UAH - u; \n"
                  "\t\t2.5. EUR - e; \n"
                  "\t\t2.6. CNY - y; \n"
                  "\t\t2.7. GBP - b; \n"
                  "\t\t2.8. CAD - c; \n"
                  "\t\t2.9. JPY - j; \n")
        elif command in self.allowedCommands["history"]:
            print("History:\n")
            for i in range(0, len(self._history.get())):
                print(str(i+1) + ".", self._history.get()[i])
        elif command in self.allowedCommands["listdefs"]: 
            defs:dict = self._defhandler.listdefs()
            keys: list = list(defs.keys())

            print("Variables:")
            for i in range(len(defs)): 
                print(str(i + 1) + ". " + keys[i] + " = " + str(defs[keys[i]]))
        elif command[:3] in self.allowedCommands["makedef"] or command[:12] in self.allowedCommands["makedef"]: 
            defs: list = [list(filter(lambda x: x != "", q)) for q in [a.split(" ") for a in [s.strip() for s in additional.split(",")]]]
            for i in range(len(defs)): 
                for j in range(2, len(defs[i])): 
                    defs[i][1] += " " + defs[i][j]
                res = self._defhandler.define(defs[i][0], calculate(analyze_str(defs[i][1], self, True), False, True))
                if res != 0:
                    print("Variable added: " + defs[i][0] + " := " + str(self._defhandler.readval(defs[i][0])))
        elif command[:8] in self.allowedCommands["setdef"] or command[:3] in self.allowedCommands["setdef"]: 
            sets: list = [list(filter(lambda x: x != "", q)) for q in [a.split(" ") for a in [s.strip() for s in additional.split(",")]]]
            for i in range(len(sets)): 
                for j in range(2, len(sets[i])): 
                    sets[i][1] += " " + sets[i][j]
                res = self._defhandler.setval(sets[i][0], calculate(analyze_str(sets[i][1], self, True), False, True))
                if res != 0: 
                    print("Value changed: " + sets[i][0] + " = " + str(self._defhandler.readval(sets[i][0]))) 
        elif command[:3] in self.allowedCommands["readdef"] or command[:9] in self.allowedCommands["readdef"]: 
            defs: dict = self._defhandler.listdefs()
            l: int = len(defs)
            currstr: str = additional

            for i in range(l): 
                currstr = currstr.replace(list(defs.keys())[i], str(list(defs.values())[i]))

            currstr = currstr.replace("^", "**")
            res = eval(currstr, {}, {})
            if should_return: 
                return res
            print(res)
        elif command[:5] in self.allowedCommands["deldef"] or command[:12] in self.allowedCommands["deldef"]: 
            todelete = [a.strip() for a in additional.split(",")]
            for key in todelete: 
                res = self._defhandler.deletevar(key) 
                if res != None: 
                    print("Successfully deleted the variable " + key)
                    continue
                
                print("Error: the variable " + key + " is not defined, thereby - cannot be deleted. ")

        else:
            print("Error: Unknown command inputted.")

    def getHistory(self) -> History:
        return self._history

    def getFuncHandler(self) -> FunctionCallHandler: 
        return self._funchandler

    def getDefHandler(self) -> DefinitionHandler: 
        return self._defhandler

def analyze_str(input_str: str, cmdhandler: CommandHandler, should_return: bool = False) -> tuple:
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
                res = cmdhandler.handle(input_str, " ".join(input_str.split(" ")[1:]), should_return)
                if res != None: return res

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
    if (type(expression) == float or type(expression) == int): 
        return expression
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
