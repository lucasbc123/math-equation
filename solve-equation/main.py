from typing import NoReturn
from function import functionClass

def solve(equation=''):
    function = functionClass()

    result, equation, message = function.simple_character_check(equation)
    if result: result, equation, message = function.validate_groupers(equation)
    if result: result, equation, message = function.list_transform(equation)

    #if no variable detected, simply solve the equation
    if result:
        if  not any(char in function.variables for char in equation):
            result, equation, message = function.bracket_solve(equation)
            if equation:
                result, equation, message = function.get_simple_result(equation)
                return result, equation, message
            else:
                return False, equation, message
                
        else:
            aux_message = 'Variable solve is still not supported:\n'
            return False, ''.join(equation), aux_message

def main():
    equation = input('Please write your equation: ')
    _, equation, message = solve(equation)
    if equation:    print(str(message) + str(equation))
    else:
        print(str(message))

if __name__ == "__main__":
    main()
