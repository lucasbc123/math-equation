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
            equation = function.bracket_solve(equation)
            if equation: result = function.get_simple_result(equation)

            if result == True:
                equation[1] = ' ' + equation[1] + ' '
                print('Your input: ' + initial_equation + ' is TRUE')
                print(''.join(equation))
            elif result == False:
                equation[1] = ' ' + equation[1] + ' '
                print('Your input: ' + initial_equation + ' is FALSE')
                print(''.join(equation))
            else:
                print('The answer for your equation: ' + initial_equation + ' is:')
                print(result)
                
        else:
            print('Variable solve is still not supported.')        
            equation = function.bracket_solve(equation)
            print(equation)


if __name__ == "__main__":
    equation = input('Please write your equation: ')
    solve(equation)
