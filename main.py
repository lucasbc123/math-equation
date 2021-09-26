from typing import NoReturn
from function import functionClass

def solve(equation=''):

    #initial preparation
    function = functionClass()
    initial_equation = equation

    equation, message = function.simple_character_check(equation)
    if equation: equation, message = function.validate_groupers(equation)
    if equation: equation, message = function.list_transform(equation)

    #if no variable detected, simply solve the equation
    if equation:
        if  not any(char in function.variables for char in equation):
            equation, message = function.bracket_solve(equation)
            if equation:
                result, full_equation, message = function.get_simple_result(equation)
                return result, full_equation, message
            else:
                return False, equation, message
                
        else:
            aux_message = 'Variable solve is still not supported: '
            return False, ''.join(equation), aux_message



if __name__ == "__main__":
    equation = input('Please write your equation: ')
    result, equation, message = solve(equation)
    if equation:    print(str(message) + str(equation))
    else:
        print(str(message))
