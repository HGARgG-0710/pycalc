from resources import analyze_str, calculate

if __name__ == '__main__':
    calculate(analyze_str())
    while True:
        calculate(analyze_str("\n$ "))
