from typing import Callable

# TODO: the library don't use the power of this API fully -- add capability to "go back in time" for the past currency excange rates (for this, change syntax;)...
# ! There is a problem: this thing don't support ruble (RUB)...
# TODO: find a more general API and use it instead (this one won't do); when having found, pray do write using
# from forex_python.converter import CurrencyRates
# ^ idea: add multiple bank currency rates APIs, then attempt to get the currency in different ones [first to succeed gets printed];


class History:
    def __init__(self):
        self._history = []

    def get(self):
        return self._history

    def add(self, command: str):
        self._history.append(command)


class DefinitionHandler:
    def __init__(self, predefined: dict = {}):
        self.definitions: dict = predefined

    def define(self, name: str, value: str):
        if name in self.definitions.keys():
            print("DefineError: You have already defined the given variable. ")
            return 0
        self.definitions[name] = value

    def setval(self, name: str, value: str):
        if name in self.definitions.keys():
            self.definitions[name] = value
            return
        print(
            "SetValueError: The given variable name is not defined. First define it. "
        )
        return 0

    def readval(self, name: str) -> str:
        return self.definitions[name]

    def listdefs(self) -> dict:
        return self.definitions

    def deletevar(self, varname: str):
        return self.definitions.pop(varname, None)


class FunctionCallHandler:
    def __init__(self, functions: tuple):
        self.functions: tuple = functions

    def getfuncvalue(self, index: int, value):
        return self.function[index](value)

    def getfuncindex(self, funcname: str):
        return self.index(funcname)


class CommandHandler:
    # TODO: problem -- Python't typehints don't support type dependencies;
    # * Conclusion: nah, they're going to go, alright...
    # ? Pray do something about it...
    def __init__(
        self,
        commands: dict,
        history: History,
        defhandler: DefinitionHandler,
        funchandler: FunctionCallHandler,
        parser=None,
    ):
        self.allowedCommands = commands

        self._history = history
        self._defhandler = defhandler
        self._funchandler = funchandler
        self._parser = parser

    def handle(self, command: str, additional: str = "", should_return: bool = False):
        command = command.strip(" ")

        if command in self.allowedCommands["exit"]:
            from sys import exit

            print("Goodbye!")
            exit()
        elif command in self.allowedCommands["help"]:
            print(
                "\nCommands: \n\n"
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
                '\t1. Syntax: it is as xy, where x, y are the currency letters. This essentially means "how many currency y in x" (Letters may also be capital: xY); \n'
                "\t2. Letters: \n\n"
                "\t\t2.1. RUB - r; \n"
                "\t\t2.2. USD - d; \n"
                "\t\t2.3. INR - i; \n"
                "\t\t2.4. UAH - u; \n"
                "\t\t2.5. EUR - e; \n"
                "\t\t2.6. CNY - y; \n"
                "\t\t2.7. GBP - b; \n"
                "\t\t2.8. CAD - c; \n"
                "\t\t2.9. JPY - j; \n"
            )
        elif command in self.allowedCommands["history"]:
            print("History:\n")
            for i in range(0, len(self._history.get())):
                print(str(i + 1) + ".", self._history.get()[i])
        elif command in self.allowedCommands["listdefs"]:
            defs: dict = self._defhandler.listdefs()
            keys: list = list(defs.keys())

            print("Variables:")
            for i in range(len(defs)):
                print(str(i + 1) + ". " + keys[i] + " = " + str(defs[keys[i]]))
        elif (
            command[:3] in self.allowedCommands["makedef"]
            or command[:12] in self.allowedCommands["makedef"]
        ):
            defs: list = [
                list(filter(lambda x: x != "", q))
                for q in [
                    a.split(" ") for a in [s.strip() for s in additional.split(",")]
                ]
            ]
            for i in range(len(defs)):
                for j in range(2, len(defs[i])):
                    defs[i][1] += " " + defs[i][j]
                res = self._defhandler.define(
                    defs[i][0],
                    calculate(
                        analyze_str(defs[i][1], self, self._parser, True), False, True
                    ),
                )
                if res != 0:
                    print(
                        "Variable added: "
                        + defs[i][0]
                        + " := "
                        + str(self._defhandler.readval(defs[i][0]))
                    )
        elif (
            command[:8] in self.allowedCommands["setdef"]
            or command[:3] in self.allowedCommands["setdef"]
        ):
            sets: list = [
                list(filter(lambda x: x != "", q))
                for q in [
                    a.split(" ") for a in [s.strip() for s in additional.split(",")]
                ]
            ]
            for i in range(len(sets)):
                for j in range(2, len(sets[i])):
                    sets[i][1] += " " + sets[i][j]
                res = self._defhandler.setval(
                    sets[i][0],
                    calculate(analyze_str(sets[i][1], self, True), False, True),
                )
                if res != 0:
                    print(
                        "Value changed: "
                        + sets[i][0]
                        + " = "
                        + str(self._defhandler.readval(sets[i][0]))
                    )
        elif (
            command[:3] in self.allowedCommands["readdef"]
            or command[:9] in self.allowedCommands["readdef"]
        ):
            # TODO (1): separate these commands onto separate functions;
            # TODO (2): implement the reading of the variables properly -- let it choose the priority of things [stuff like 'pie' won't be read as '(pi)e']
            defs: dict = self._defhandler.listdefs()
            l: int = len(defs)
            currstr: str = additional

            for i in range(l):
                currstr = currstr.replace(
                    list(defs.keys())[i], str(list(defs.values())[i])
                )

            currstr = currstr.replace("^", "**")
            res = eval(currstr, {}, {})
            if should_return:
                return res
            print(res)
        elif (
            command[:5] in self.allowedCommands["deldef"]
            or command[:12] in self.allowedCommands["deldef"]
        ):
            todelete = [a.strip() for a in additional.split(",")]
            for key in todelete:
                res = self._defhandler.deletevar(key)
                if res != None:
                    print("Successfully deleted the variable " + key)
                    continue

                calculator_error(
                    "Error: the variable "
                    + key
                    + " is not defined, thus - cannot be deleted. "
                )

        else:
            calculator_error("Error: Unknown command inputted.")

    def getHistory(self) -> History:
        return self._history

    def getFuncHandler(self) -> FunctionCallHandler:
        return self._funchandler

    def getDefHandler(self) -> DefinitionHandler:
        return self._defhandler


class Parser:
    cmdhandler: CommandHandler
    operators: list[str]

    @staticmethod
    def parse_bracket():
        pass

    # TODO: destroy the limitations of parser; make it far more unlimited;

    # TODO: handle the ambiguities within the parser (multiple --, the use of letters, which can be used for currencies, et cetera...)
    # * Don't delete this thing -- instead, pray keep it;
    # ^ IDEA: make the project into a proper 'module' or however is this programmatic unit called in Python lingo -- an importable entity [if it isn't already...];
    # ^ IDEA: generalize this powerfully -- create a CalcSyntax thing, a library with a very wide calculator implemented in it with possibility of choosing syntax for it;
    # ^ IDEA: make the 'pycalc' more configurable -- add a '--config' command; Let it correspond to changing the notation for things [and let it be general enough... -- make proper syntax for it];
    @staticmethod
    def parse_int(string: list[str], index: int):
        # TODO: generalize to array of symbols for inverse of the number over positiveness...
        endInd = readwhile(
            string, index, lambda x: not x.isdigit() and x == "-" or x == "n"
        )
        d = readwhile(string, endInd, lambda x: x.isdecimal())
        return (int((((endInd - index) % 2) * "-") + "".join(string[endInd:d])), d)

    @staticmethod
    def checkifcommand(string, index):
        while index < len(string):
            # TODO: generalize this thing to an array of characters NOT appearing within a command [used to distinguish between commands and other things;vI]...
            if (
                string[index] == "."
                or string[index].isdecimal()
                or string[index] == "("
                or string[index] == ")"
            ):
                return False
            index += 1

        return True

    @staticmethod
    def validify(string: str, allowed_syms: list[str] | str, replace_map: dict[str, str], skipped: list[str] = []):
        return "".join([a if a in allowed_syms else replace_map[a] for a in string if not a in skipped])

    # todo: GENERALIZE to have the arbitrary n-ary system (for now, only decimals are supported...); 
    @classmethod
    def num_validify(cls, numstr: str):
        return cls.validify(numstr, "".join([str(i) for i in range(10)]) + ".", {",": "."})

    # TODO: generalize the 'indicator' symbols -- here it's ['f'];
    @classmethod
    def parse_number(cls, string: list[str], index: int):
        if string[index] == "f":
            index = index + 1
        endInd = readwhile(
            string, index, lambda x: not x.isdigit() and x == "-" or x == "n"
        )
        d = readwhile(string, endInd, lambda x: x.isdecimal())
        if d < len(string) and (string[d] in [".", ","]):
            d = readwhile(string, d + 1, lambda x: x.isdecimal())
        # TODO: the first argument should get converted to 'int' (when it's an integer - the output is ALWAYS a float...);
        return (
            float(
                (((endInd - index) % 2) * "-")
                + "".join(cls.num_validify(string[endInd:d]))
            ),
            d,
        )

    @staticmethod
    def parse_operator():
        pass

    def parse_command():
        pass

    def __init__(self, _cmdhandler: CommandHandler, _operators: list[str]):
        self.cmdhandler = _cmdhandler
        self.operators = _operators


def calculator_error(message):
    print(message)
    return ((), ())


# TODO: let the type annotations be intact with the actually used types...
def readwhile(string, index: int, property: Callable):
    ind = index
    while ind < len(string) and property(string[ind]):
        ind += 1
    return ind


def analyze_str(
    input_str, cmdhandler: CommandHandler, parser: Parser, should_return: bool = False
) -> tuple:
    numbers = []
    operators = []

    input_str_list = list(input_str)
    index = 0

    # todo: rewrite this into a "while True" + checking for index to be 'too high' [this'd be more manual but greater control over the loop too]...
    while True:
        if index == len(input_str):
            break

        char = input_str[index]

        # TODO: see if one wants to separate the calculator code further onto differing steps or not...
        isCommand = False

        if char == "-":
            isCommand = parser.checkifcommand(input_str, index)
            if not isCommand and index < len(input_str) - 1 and input_str[index + 1].isdecimal():
                char = "n"

        if (char.isdecimal() or char == "n" or char == "f") and not isCommand:
            numstr, index = parser.parse_number(input_str_list, index)
            numbers += [str(numstr)]
            continue
        else:
            from re import match

            if isCommand:
                # command
                # TODO: clean up all this ridiculous mess as well; Change the types -- make code more... "possible" [though, with this language, it probably won't make much difference]
                res = cmdhandler.handle(
                    input_str, " ".join(input_str.split(" ")[1:]), should_return
                )
                if res != None:
                    return res

                input_str = input("\n$ ")
                cmdhandler.getHistory().add(input_str)

                return analyze_str(input_str, cmdhandler, parser)
            elif char in parser.operators:
                # operator
                # TODO (1): this should check for more complex operators
                # TODO (2): this don't work generally at all, just HAPPENS to work for the operators that take only 1 symbol [which really shouldn't and is only a Python feature];i
                operators += char
            elif char == "(" or char == ")":
                # todo: Wrap the handing of brackets into something, check that they are not error-prone...
                # bracket
                operators += ["+"]
                numbers += [
                    ("0" if char == ")" else "") + char + ("0" if char == "(" else "")
                ]

            # ? Do something about that notation???
            elif match("[A-Za-z]", char):
                index += 1
                numbers += [
                    "(" + eval_currency(char.upper(), input_str[index].upper()),
                    "0)",
                ]
                operators += ["+"]
            else:
                if char != " " and char != "\t":
                    return calculator_error(
                        "Error: Unknown character " + char + " inputted."
                    )
            index += 1

    return numbers, operators


def calculate(expression: tuple, should_output=True, should_return=False):
    if type(expression) == float or type(expression) == int:
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
    return (
        operator if operator in common_operators else "//" if operator == "#" else "**"
    )


def eval_currency(originalCurrency: str, targetCurrency: str):
    from requests import get

    # * note: this does not depend upon the fact if
    # * the currency is acceptable or not!
    if originalCurrency.upper() == targetCurrency.upper():
        return "1"

    # TODO: Expand this thing... Add more of them...
    currency_names: dict = {
        "D": "USD",
        "E": "EUR",
        "R": "RUB",
        "U": "UAH",
        "I": "INR",
        "Y": "CNY",
        "B": "GBP",
        "J": "JPY",
        "C": "CAD",
    }

    # TODO: This thing is no longer free. Calculator can no longer rely on it.
    # * Shame. Such a wonderful idea.
    # ! Never mind, will just find an alternative free api for doing this (or fetch data directly from somewhere, hehe).

    if (
        originalCurrency.upper() not in currency_names
        or targetCurrency.upper() not in currency_names
    ):
        err_currency = (
            originalCurrency
            if originalCurrency.upper() not in currency_names
            else targetCurrency
        )

        return str(
            len(calculator_error(f"Error: no such currency as {err_currency}")[0])
        )

    original: str = currency_names[originalCurrency]
    target: str = currency_names[targetCurrency]

    address: str = r"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE"
    query_text: str = (
        f"{address}&from_currency={original}&to_currency={target}&apikey=H88SANVRLLXS7BD9"
    )

    result = get(query_text).json()
    exchange_rate = result["Realtime Currency Exchange Rate"]["5. Exchange Rate"]

    return exchange_rate
