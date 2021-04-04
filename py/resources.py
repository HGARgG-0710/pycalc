from sys import exit


def analyze_str(input_message="Input expression, that you wish to be calculated or command, "
                              "that you wish to be executed. For help type '-h' or '--help'.\n$ "):
    input_str = input(input_message)
    numbers = []
    operators = []

    index = 0

    for _ in input_str:
        if index >= len(input_str):
            break

        char = input_str[index]

        try:
            int(char)
            t = "int"
        except ValueError:
            t = "float" if char == "f" else "str"

        if t == "int":
            numbers += [char]
            index += 1
            while True:
                try:
                    curr_symbol = input_str[index if index < len(
                        input_str) else index - 1]
                    int(curr_symbol)  # checking if a number

                    if index == len(input_str):
                        break
                    index += 1
                    numbers[len(numbers) - 1] += curr_symbol
                except ValueError:
                    break
        elif t == "str" and char != " ":
            allowed_operators = ["+", "-", "*", "/", "%", "#", "^"]

            if char == "-" and index == 0:
                # command
                handle_command(input_str)
                return analyze_str("\n$ ")
            elif char in allowed_operators:
                # operator
                operators += char
            else:
                raise Exception("Invalid character " + char + " inputted.")
        elif t == "float":
            raise Exception("Sorry, no support for floats yet!")
        index = index + 1

    return numbers, operators


def handle_command(command):
    if command == "-e" or command == "--exit":
        exit()
    elif command == "-h" or command == "--help":
        print("To exit the app type command '-e' or '--exit'. \n"
              "Operators: \n"
              "1. division: /\n"
              "2. addition: +\n"
              "3. subtraction: -\n"
              "4. multiplication: *\n"
              "5. taking the remainder of the division: %\n"
              "6. exponentiation: ^\n"
              "7. whole division: #\n"
              "To specify a float number type the 'f' letter and only then the number itself. \n"
              "Example: f4.2\n")


def calculate(expression):
    nums = expression[0]
    operators = expression[1]
    expr = ""

    for i in range(0, len(nums)):
        expr += nums[i]
        if i != len(nums) - 1:
            expr += operator_evaluator(operators[i])

    result = eval(expr)
    print(result)


def operator_evaluator(operator):
    common_operators = ["+", "-", "*", "/", "%"]
    return operator if operator in common_operators else \
        "//" if operator == "#" else "**"
