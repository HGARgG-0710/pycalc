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
            t = "float" if char == "f" else "str" if char != "n" else "int"

        if t == "int":
            numbers += ([char] if char != "n" else "-")
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
            index -= 1
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
            numbers += (input_str[index + 1]
                        if input_str[index + 1] != "n" else "-")
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
                        break

                except ValueError:
                    break
            index -= 1
        index = index + 1

    return numbers, operators


def handle_command(command):
    if command == "-e" or command == "--exit":
        exit()
    elif command == "-h" or command == "--help":
        print("To exit the app type command '-e' or '--exit'. \n\n"
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
              "Example of a negative float number: fn84.6"
              )


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
