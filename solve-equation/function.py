#order of operations:
#   simple_character_check
#       validade characters, and take away space bar, and normalizes all dots to "."
#       counts how many times the character '=' appears, only once it's allowed.

#   validate_groupers
#       validade if the opening and closing of brackets is correct
#       and standardize all brackets to parentheses

#   list_transform
#       transforms the String equation into a List for further analysis
#       groups numbers and dots together
#       adds '*' before or after brackets when needed, and before and after variables

#   insert_multiplication_symbol
#       insert multiplication symbol in certain cases
#       before / after parentheses
#       before after variables

#   simplify_plus_minus
#       resolves cases where there are more then one plus or minus character in a row

#   simple_solve_preparation
#       to help solve equations, the plus and minus symbol are part of the number
#       therefore '-', '2' is transformed to '-2'

#   simple_solve
#       solves a part of the equation without any parenthesis, and with the correct order of operations
#       calls "insert_multiplication_symbol", "simplify_plus_minus" and "simple_solve_preparation" before starting

#   bracket_solve
#       calls "simple_solve" when it identifies a "bracket section"

#   get_simple_result
#       converts the equation result from "bracket_solve" into a string.
#       incase of equality symbol, check if both sides are equal
#       return True if both sides are equal
#       return False if both sides aren't equal

import random

class functionClass:
            
    def __init__(self):
        self.variables = [chr(i) for i in range(ord('a'),ord('z')+1)] + [chr(i) for i in range(ord('A'),ord('Z')+1)]

        self.numbers = [chr(i) for i in range(ord('0'),ord('9')+1)]

        self.plus_minus_symbols = ['+','-']
        self.rest_symbols = ['*','/','^']
        self.equality = ['=']

        self.main_divider = ['.']
        self.aux_divider = [',']

        self.opening_groupers = ['(','[','{']
        self.closing_groupers = [')',']','}']

        self.auxiliar_symbols = [' ']

        self.all_symbols = []
        for _,value in vars(self).items():
            self.all_symbols = self.all_symbols + value

        self.together = self.numbers + self.main_divider
        self.most_math_symbols = self.plus_minus_symbols + self.rest_symbols + self.equality

    def is_number(self,text):
        try:
            float(text)
            return True
        except:
            return False

    def simple_character_check(self,equation=''):
        count_equals = 0
        message = "All characters are valid. "
        if type(equation) is not str:
            message = 'Current input: ' + str(type(equation)) + '. Input should be of <str> type. '
            return False, equation, message
        
        equation = equation.replace(self.auxiliar_symbols[0],'')
        if equation == '':
            message = "No equation given. "
            return False, equation, message
        else:
            not_accepted = []
            for char in equation:
                if char not in self.all_symbols and char not in not_accepted:
                    not_accepted.append(char)
                elif char == self.equality[0]:
                    count_equals = count_equals + 1
            
            if count_equals > 1:
                message = "Too many equal signs. "
                return False, equation, message

            if not_accepted == []:
                equation = equation.replace(',','.')
                return True, equation, message
            else:
                text = ''
                for aux in not_accepted:
                    text = text + "'" + aux + "' , "
                message = "Not supported symbols: " + text[:-3]
                return False, equation, message
    
    def validate_groupers(self,equation):

        opening_groupers = 0
        closing_groupers = 0
        last_grouper = []
        parentheses = [self.opening_groupers[0], self.closing_groupers[0]]
        brackets = [self.opening_groupers[1], self.closing_groupers[1]]
        curly_brackets = [self.opening_groupers[2], self.closing_groupers[2]]

        message = "Brackets are correct. "

        i = 0
        for char in equation:
            if char in self.opening_groupers:
                opening_groupers = opening_groupers + 1
                last_grouper.append(char)

            elif char in self.closing_groupers:
                closing_groupers = closing_groupers + 1
                
                if closing_groupers > opening_groupers:
                    message = "Unexpected closing brackets at index: " + str(i)
                    return False, equation, message

                if (last_grouper[-1] in parentheses and char not in parentheses) \
                    or (last_grouper[-1] in brackets and char not in brackets) \
                    or (last_grouper[-1] in curly_brackets and char not in curly_brackets):
                    message = "Closing brackets of unexpected type at index: " + str(i)
                    return False, equation, message
                else:
                    last_grouper.pop()

            i = i + 1

        if opening_groupers == closing_groupers:
            for i in range(len(self.opening_groupers)):
                equation = equation.replace(self.opening_groupers[i],self.opening_groupers[0])
                equation = equation.replace(self.closing_groupers[i],self.closing_groupers[0])
            return True, equation, message
        else:
            message = "Missing at least one closing bracket. "
            return False, equation, message

    def list_transform(self, equation):
        equation = equation.replace(',','.')

        was_number = False
        list_equation = []
        message = "Equation transformed to list format. "
        for char in equation:
            if char not in self.together:
                list_equation.append(char)
                was_number = False
            elif was_number:
                list_equation[-1] = list_equation[-1] + char
                was_number = True
            else:
                list_equation.append(char)
                was_number = True

        i = 0
        for item in list_equation:
            if item.count('.') > 1:
                message = 'The number "' + item + '" is written incorrectly. '
                return False, list_equation, message
            elif item == '.':
                message = "There is an isolated number divider ('.' or ','). "
                return False, list_equation, message
            else:
                if item[0] == '.':
                    list_equation[i] = '0' + item
                elif item[-1] == '.':
                    list_equation[i] = item[:-1]

            i = i + 1

        return True, list_equation, message    

    def insert_multiplication_symbol(self, equation):
        initial_length = len(equation)
        i = 1
        while i < len(equation):
            char = str(equation[i])
            previous_char = str(equation[i-1])
            #   cases when it's needed to add a '*' sign.
            #   1-  before '(' (when there is a number / variable before, or another ')')
            #   2-  after ')' (when there is a number / variable after)
            #   3-  before / after variables

            #separate conditions to make it easier to read / understad
            
            #   1-  before '(', when there is a number / variable before
            if char == self.opening_groupers[0] and (self.is_number(previous_char) or previous_char in self.variables or previous_char in self.closing_groupers[0]):
                equation.insert(i,'*')
                i = i + 1
            #   2-  after ')', when there is a number / variable after
            elif (self.is_number(char) or char in self.variables) and previous_char == self.closing_groupers[0]:
                equation.insert(i,'*')
                i = i + 1
            #   3-  before / after variables, when next to a number or a different variable
            #elif (char in self.variables or self.is_number(char)) and (self.is_number(previous_char) or previous_char in self.variables):
            elif (char in self.variables and (self.is_number(previous_char) or previous_char in self.variables)) or\
                (self.is_number(char) and previous_char in self.variables):
                equation.insert(i,'*')
                i = i + 1

            i = i + 1

        message = "No added multiplication symbols. "
        counter = len(equation) - initial_length
        if counter > 0:
            message = "Number of aditional multiplication symbols added: " + str(counter)
        return equation, message, counter

    def simplify_plus_minus(self,equation):
        i = 1
        counter = 0
        while i < len(equation):

            if equation[i] in self.plus_minus_symbols and equation[i-1] in self.plus_minus_symbols:
                counter = counter + 1
                if equation[i] == equation[i-1]:
                    equation[i] = '+'
                    equation.pop(i-1)
                else:
                    equation[i] = '-'
                    equation.pop(i-1)
                i = i - 1
            i = i + 1
        message = "No plus or minus symbols where changed. "
        if counter > 0:
            message = "Number of plus or minus symbols simplified: " + str(counter)
        return equation, message, counter

    def simple_solve_preparation(self,equation):
        if self.is_number(equation[0]):
            equation[0] = str(float(equation[0]))

        if len(equation) > 1:
            i = 1
            while i < len(equation):
                char = str(equation[i])
                previous_char = str(equation[i-1])
                if self.is_number(char):
                    if previous_char in self.plus_minus_symbols[0]:
                        equation[i] = str(float(equation[i]))
                        equation.pop(i-1)
                        i = i - 1
                    elif previous_char in self.plus_minus_symbols[1]:
                        equation[i] = str(float(equation[i]) * -1)
                        equation.pop(i-1)
                        i = i - 1
                    else:
                        equation[i] = str(float(char))
                i = i + 1

        return equation

    def full_preparation(self, equation):
        equation = self.insert_multiplication_symbol(equation)[0]
        equation = self.simplify_plus_minus(equation)[0]
        equation = self.simple_solve_preparation(equation)

        return equation        

    def simple_solve(self,equation):
        equation = self.full_preparation(equation)
        message = "Section solved. "
        #solve exponentiation
        i = 1
        while i < len(equation):
            if self.is_number(equation[i-1]) and equation[i] == '^' and self.is_number(equation[i+1]):
                equation[i+1] = str(float(equation[i-1]) ** float(equation[i+1]))
                equation.pop(i-1)
                equation.pop(i-1)
                i = i - 1
            i = i + 1
        #solve multiplication and division
        i = 1
        while i < len(equation):
            if self.is_number(equation[i-1]) and equation[i] in self.rest_symbols[0:2] and self.is_number(equation[i+1]):
                if equation[i] == '*':
                    equation[i+1] = str(float(equation[i-1]) * float(equation[i+1]))
                elif equation[i] == '/':
                    if float(equation[i+1]) != 0:
                        equation[i+1] = str(float(equation[i-1]) / float(equation[i+1]))
                    else:
                        if random.randint(0,100) < 5:  message = "Hey, that's illegal! You can't just divide by zero. "
                        else:   message = "Can't divide by zero. "
                        return False, message
                equation.pop(i-1)
                equation.pop(i-1)
                i = i - 1
            i = i + 1  
        #solve addition and subtraction
        i = 1
        while i < len(equation):

            if self.is_number(equation[i-1]) and self.is_number(equation[i]):
                equation[i] = str(float(equation[i-1]) + float(equation[i]))
                equation.pop(i-1)
                i = i - 1
            i = i + 1

        #final check for inconsistencies
        i = 1
        while i < len(equation):
            if equation[i] in self.most_math_symbols and equation[i-1] in self.most_math_symbols:
                message = "Invalid series of symbols. "
                return False, message
            i = i + 1
        return equation, message

    def bracket_solve(self, equation):     
        equation = self.full_preparation(equation)
        result = True
        message = "All bracket solved. "
        error_message = ''
        last_opening = 0
        first_closing = 0
        i = 0
        while equation and i < len(equation) and first_closing == 0:
            if equation[i] == self.opening_groupers[0]:
                last_opening = i + 1
            if equation[i] == self.closing_groupers[0]:
                first_closing = i
                equation_section,error_message = self.simple_solve(equation[last_opening:first_closing])
                if equation_section != False and len(equation_section) == 1:
                    equation = equation[:last_opening-1] + equation_section + equation[first_closing+1:]
                    result, equation, error_message = self.bracket_solve(equation)
                elif equation_section != False and len(equation_section) > 1:
                    equation = equation[:last_opening-1] + [self.opening_groupers[1]] + equation_section + [self.closing_groupers[1]] + equation[first_closing+1:]
                    result, equation, error_message = self.bracket_solve(equation)
                else:
                    equation = False
                
            i = i + 1

        if result: equation,error_message = self.simple_solve(equation)
        if equation: 
            for i in range(len(equation)):
                if equation[i] == self.opening_groupers[1]: equation[i] = self.opening_groupers[0]
                elif equation[i] == self.closing_groupers[1]: equation[i] = self.closing_groupers[0]
            return True, equation, message

        else:   
            return False, equation, error_message


    def get_simple_result(self, equation):
        if self.equality[0] in equation:
            if equation[0] == equation[2]:
                return True, ''.join(equation),"Both sides are equal:\n"
            else:
                return False, ''.join(equation),"Both sides aren't equal:\n"
        else:
            
            return True, ''.join(equation), "Answer:\n"
