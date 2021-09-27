import unittest
from function import functionClass

function = functionClass()

class TestFunctionClass(unittest.TestCase):

    def test_simple_character_check(self):

        type_list = [
            20, 20.5,   1j, ["apple", "banana", "cherry"],  ("apple", "banana", "cherry"),
            range(6),   {"name" : "John", "age" : 36},  {"apple", "banana", "cherry"},
            frozenset({"apple", "banana", "cherry"}),   True,   b"Hello",   bytearray(5),
            memoryview(bytes(5))
        ]
        correct_message = "Input should be of <str> type."
        for equation in type_list:
            input = str(equation)
            result, _, message = function.simple_character_check(equation)
            self.assertEqual(result, False,\
                "input: " + input + " output: " + str(result) + " correct output: False" )
            self.assertIn(correct_message,message,\
                "input: " + input + " Error message is incorrect. It should have: " + correct_message)

        wrong_example_list = [
            '',
            '  ',
            '         '
        ]
        correct_message = "No equation given."

        for equation in wrong_example_list:
            input = str(equation)
            resutl, _, message = function.simple_character_check(equation)
            self.assertEqual(resutl, False,\
                "input: " + input + " output: " + str(resutl) + " correct output: False" )
            self.assertIn(correct_message,message,\
                "input: " + input + " Error message is incorrect. It should have: " + correct_message)

        wrong_example_list = [
            '1==1', '2=2=2'
        ]
        correct_message = "Too many equal signs."

        for equation in wrong_example_list:
            input = str(equation)
            resutl, _, message = function.simple_character_check(equation)
            self.assertEqual(resutl, False,\
                "input: " + input + " output: " + str(resutl) + " correct output: False" )
            self.assertIn(correct_message,message,\
                "input: " + input + " Error message is incorrect. It should have: " + correct_message)                

        correct_example_list = [
            '2',                '2',
            '2,2',              '2.2',
            '2.2',              '2.2',
            ' 2 . 2',           '2.2',
            '2.2+2,2',          '2.2+2.2',
            '.,.,',             '....',
            '1   1',            '11',
            '1.1   +   1,1',    '1.1+1.1'
        ]
        correct_message = "All characters are valid."
        aux_index = [i*2 for i in range(int(len(correct_example_list)/2))]
        for i in aux_index:
            input = correct_example_list[i]
            output = correct_example_list[i+1]
            result, equation, message = function.simple_character_check(input)
            self.assertEqual(result, True,\
                "input: " + input + " output: " + str(result) + " correct output: True")                       
            self.assertEqual(equation,correct_example_list[i+1],\
                "input: " + str(input) + " output: " + str(equation) + " correct output: " + str(output))
            self.assertIn(correct_message,message,\
                "input: " + input + " Error message is incorrect. It should have: " + correct_message)                                

        wrong_example_list = [
            "@",    "1+@",  "2*#$%",    "\\",   "1+2(3-4)¨",    "~",    "ç",    "|",    '_'
        ]
        correct_message = "Not supported symbols: "
        for equation in wrong_example_list:
            input = str(equation)
            result, equation, message = function.simple_character_check(equation)
            self.assertEqual(result, False,\
                "input: " + input + " output: " + str(result) + " correct output: False" )
            self.assertIn(correct_message,message,\
                "input: " + input + " Error message is incorrect. It should have: " + correct_message)                
        

        
    def test_validate_groupers(self):
        wrong_example_list = [
            '1+2)+3',   '1+2]+3',   '1+2}+3',   '(1+2))',   ']1+2', '[1+2]]',   '(1+2)]'
        ]
        correct_message = "Unexpected closing brackets at index:"
        for equation in wrong_example_list:
            input = str(equation)
            result, _, message = function.validate_groupers(equation)
            self.assertEqual(result, False,\
                "input: " + input + " output: " + str(result) + " correct output: False" )
            self.assertIn(correct_message,message,\
                "input: " + input + " Error message is incorrect. It should have: " + correct_message) 

        wrong_example_list = [
            '(1+2]',    '(1+2}',    '[1+2)',    '[1+2}',    '{1+2)',    '{1+2]',    '(1+2[1+2)]'
        ]
        correct_message = "Closing brackets of unexpected type at index:"
        for equation in wrong_example_list:
            input = str(equation)
            result, _, message = function.validate_groupers(equation)
            self.assertEqual(result, False,\
                "input: " + input + " output: " + str(result) + " correct output: False" )
            self.assertIn(correct_message,message,\
                "input: " + input + " Error message is incorrect. It should have: " + correct_message)

        wrong_example_list = [
            '(2+1', '[1+2*(2+1)',   '2+{1-2'
        ]
        correct_message = "Missing at least one closing bracket."
        for equation in wrong_example_list:
            input = str(equation)
            result, _, message = function.validate_groupers(equation)
            self.assertEqual(result, False,\
                "input: " + input + " output: " + str(result) + " correct output: False" )
            self.assertIn(correct_message,message,\
                "input: " + input + " Error message is incorrect. It should have: " + correct_message)                

        #input, correct output,
        correct_example_list = [
            '(1+2)',            '(1+2)',
            '[1+2]',            '(1+2)',
            '{1+2}',            '(1+2)',
            '{1[2(3)2]1}',      '(1(2(3)2)1)',
            '{1(2[3]2)1}',      '(1(2(3)2)1)',
            '[1{2(3)2}1]',      '(1(2(3)2)1)',
            '[1(2{3+1}2)1]',    '(1(2(3+1)2)1)'
        ]
        correct_message = "Brackets are correct."
        aux_index = [i*2 for i in range(int(len(correct_example_list)/2))]
        for i in aux_index:
            input  = str(correct_example_list[i])
            output = str(correct_example_list[i+1])
            result, equation, message = function.validate_groupers(correct_example_list[i])
            self.assertEqual(equation,correct_example_list[i+1],\
                "input: " + input + " output: " + str(equation) + " correct output: " +  output)
            self.assertIn(correct_message,message,\
                "input: " + input + " Error message is incorrect. It should have: " + correct_message)                

    def test_list_transform(self):
        wrong_example_list = [
            '1.1.*1',   '.1.*1',    '..1*1'
        ]
        correct_message = "is written incorrectly."
        for equation in wrong_example_list:
            input = str(equation)
            result, _, message = function.list_transform(equation)
            self.assertEqual(result, False,\
                "input: " + input + " output: " + str(result) + " correct output: False" )
            self.assertIn(correct_message,message,\
                "input: " + input + " Error message is incorrect. It should have: " + correct_message)       

        wrong_example_list = [
        '1*.*1',    '1*,*2',    '2+,-2',    '+2-.-2',   '1/.^2'
        ]
        correct_message = "There is an isolated number divider ('.' or ',')."
        for equation in wrong_example_list:
            input = str(equation)
            result, _, message = function.list_transform(equation)
            self.assertEqual(result, False,\
                "input: " + input + " output: " + str(result) + " correct output: False" )
            self.assertIn(correct_message,message,\
                "input: " + input + " Error message is incorrect. It should have: " + correct_message)                                         

        correct_example_list = [
            '12',                   ['12'],
            '12.12',                ['12.12'],
            '.12',                  ['0.12'],
            '12.',                  ['12'],
            'abc',                  ['a','b','c'],
            '(1+1.-.1*1.1/a^b)',    ['(','1','+','1','-','0.1','*','1.1','/','a','^','b',')']
        ]
        correct_message = "Equation transformed to list format."
        aux_index = [i*2 for i in range(int(len(correct_example_list)/2))]
        for i in aux_index:
            input  = str(correct_example_list[i])
            output = str(correct_example_list[i+1])
            result, equation, message = function.list_transform(correct_example_list[i])
            self.assertEqual(equation,correct_example_list[i+1],\
                "input: " + input + " output: " + str(equation) + " correct output: " +  output)
            self.assertIn(correct_message,message,\
                "input: " + input + " Error message is incorrect. It should have: " + correct_message)                                
                
    def test_insert_multiplication_symbol(self):
        correct_example_list = [
            ['2'],                                                                                  ['2'],
            ['a'],                                                                                  ['a'],
            ['a','*','b'],                                                                          ['a','*','b'],
            ['a','*','b'],                                                                          ['a','*','b'],
            ['a','+','b'],                                                                          ['a','+','b'],
            ['(','2',')','*','2'],                                                                  ['(','2',')','*','2'],
            ['2','*','(','2',')'],                                                                  ['2','*','(','2',')'],
            ['a','*','2','+','(','a','*','b',')','*','a'],                                          ['a','*','2','+','(','a','*','b',')','*','a'],
            ['1.0','-2.0','*','3.0','^','4.0'],                                                     ['1.0','-2.0','*','3.0','^','4.0'],
            ['1','*','a','*','(','2','*','b',')','*','(','2','*','(','(','a',')','*','a',')',')'],  ['1','*','a','*','(','2','*','b',')','*','(','2','*','(','(','a',')','*','a',')',')']
        ]
        correct_message = "No added multiplication symbols."
        aux_index = [i*2 for i in range(int(len(correct_example_list)/2))]
        for i in aux_index:
            input  = str(correct_example_list[i])
            output = str(correct_example_list[i+1])
            test, message, _ = function.insert_multiplication_symbol(correct_example_list[i])
            self.assertEqual(test,correct_example_list[i+1],\
                "input: " + input + " output: " + str(test) + " correct output: " +  output)
            self.assertIn(correct_message,message,\
                "input: " + input + " Error message is incorrect. It should have: " + correct_message)    

        correct_example_list = [
            ['a','b'],                                                      ['a','*','b'],
            ['(','2',')','2'],                                              ['(','2',')','*','2'],
            ['2','(','2',')'],                                              ['2','*','(','2',')'],
            ['a','2','+','(','a','b',')','a'],                              ['a','*','2','+','(','a','*','b',')','*','a'],
            ['1','a','(','2','b',')','(','2','(','(','a',')','a',')',')'],  ['1','*','a','*','(','2','*','b',')','*','(','2','*','(','(','a',')','*','a',')',')']
        ]
        correct_message = "Number of aditional multiplication symbols added:"
        aux_index = [i*2 for i in range(int(len(correct_example_list)/2))]
        for i in aux_index:
            input  = str(correct_example_list[i])
            output = str(correct_example_list[i+1])
            test, message, _ = function.insert_multiplication_symbol(correct_example_list[i])
            self.assertEqual(test,correct_example_list[i+1],\
                "input: " + input + " output: " + str(test) + " correct output: " +  output)
            self.assertIn(correct_message,message,\
                "input: " + input + " Error message is incorrect. It should have: " + correct_message)                                                            

    def test_simplify_plus_minus(self):
        correct_example_list = [
            ['2'],                                              ['2'],
            ['2','+','2'],                                      ['2','+','2'],
            ['2','-','2'],                                      ['2','-','2'],
            ['1','+','2','-','3'],                              ['1','+','2','-','3']
            
        ]
        correct_message = "No plus or minus symbols where changed."
        aux_index = [i*2 for i in range(int(len(correct_example_list)/2))]
        for i in aux_index:
            input  = str(correct_example_list[i])
            output = str(correct_example_list[i+1])
            test, message, _ = function.simplify_plus_minus(correct_example_list[i])
            self.assertEqual(test,correct_example_list[i+1],\
                "input: " + input + " output: " + str(test) + " correct output: " +  output)
            self.assertIn(correct_message,message,\
                "input: " + input + " Error message is incorrect. It should have: " + correct_message)              

        correct_example_list = [
            ['2','-','-','2'],                                  ['2','+','2'],
            ['2','+','+','2'],                                  ['2','+','2'],
            ['2','+','-','2'],                                  ['2','-','2'],
            ['2','-','+','2'],                                  ['2','-','2'],
            ['-','+','2','+','-','+','2','+','+','-','-','2'],  ['-','2','-','2','+','2'],
            
        ]
        correct_message = "Number of plus or minus symbols simplified:"
        aux_index = [i*2 for i in range(int(len(correct_example_list)/2))]
        for i in aux_index:
            input  = str(correct_example_list[i])
            output = str(correct_example_list[i+1])
            test, message, _ = function.simplify_plus_minus(correct_example_list[i])
            self.assertEqual(test,correct_example_list[i+1],\
                "input: " + input + " output: " + str(test) + " correct output: " +  output)         
            self.assertIn(correct_message,message,\
                "input: " + input + " Error message is incorrect. It should have: " + correct_message)

    def test_simple_solve_preparation(self):
        correct_example_list = [
            ['2'],                                                  ['2.0'],
            ['2.0'],                                                ['2.0'],
            ['-','2'],                                              ['-2.0'],
            ['+','2'],                                              ['2.0'],
            ['+','2','-','2'],                                      ['2.0','-2.0'],
            ['-','2.0'],                                            ['-2.0'],
            ['2','+','2','-','2','+','2.0','*','2.0','^','2.0'],    ['2.0','2.0','-2.0','2.0','*','2.0','^','2.0'],
        ]

        aux_index = [i*2 for i in range(int(len(correct_example_list)/2))]
        for i in aux_index:
            input  = str(correct_example_list[i])
            output = str(correct_example_list[i+1])
            test = function.simple_solve_preparation(correct_example_list[i])
            self.assertEqual(test,correct_example_list[i+1],\
                "input: " + input + " output: " + str(test) + " correct output: " +  output)

    def test_full_preparation(self):
        correct_example_list = [
            ['2'],                                                                  ['2.0'],
            ['a'],                                                                  ['a'],
            ['a','b'],                                                              ['a','*','b'],
            ['a','*','b'],                                                          ['a','*','b'],
            ['a','+','b'],                                                          ['a','+','b'],
            ['2','(','2',')','2'],                                                  ['2.0','*','(','2.0',')','*','2.0'],                                     
            ['a','2','+','(','a','b',')','a'],                                      ['a','*','2.0','+','(','a','*','b',')','*','a'],
            ['1','-2','*','3','^','4'],                                             ['1.0','-2.0','*','3.0','^','4.0'],
            ['2','+','2'],                                                          ['2.0','2.0'],
            ['2','-','2'],                                                          ['2.0','-2.0'],
            ['2','+','-','2'],                                                      ['2.0','-2.0'],
            ['2','-','+','2'],                                                      ['2.0','-2.0'],
            ['-','+','2','+','-','+','2','+','+','-','-','2'],                      ['-2.0','-2.0','2.0'],
            ['2','+','2','-','2','+','2.0','*','2.0','^','2.0'],                    ['2.0','2.0','-2.0','2.0','*','2.0','^','2.0'],
            ['1.0','a','(','2.0','b',')','(','2.0','(','(','a',')','a',')',')'],    ['1.0','*','a','*','(','2.0','*','b',')','*','(','2.0','*','(','(','a',')','*','a',')',')'],
            ['2','^','-','(','1','+','2',')'],                                      ['2.0','^','-','(','1.0','2.0',')']

        ]

        aux_index = [i*2 for i in range(int(len(correct_example_list)/2))]
        for i in aux_index:
            input  = str(correct_example_list[i])
            output = str(correct_example_list[i+1])
            test = function.full_preparation(correct_example_list[i])
            self.assertEqual(test,correct_example_list[i+1],\
                "input: " + input + " output: " + str(test) + " correct output: " +  output)

    def test_simple_solve(self):
        wrong_example_list = [
            ['1','/','0'],  ['1','/','0','*','2']
        ]

        correct_message = "divide by zero."
        for equation in wrong_example_list:
            input = str(equation)   
            test, message = function.simple_solve(equation)
            self.assertEqual(test, False,\
                "input: " + input + " output: " + str(test) + " correct output: False" )
            self.assertIn(correct_message,message,\
                "input: " + input + " Error message is incorrect. It should have: " + correct_message) 

        wrong_example_list = [
            ['1','*','*','2'],  ['1','/','/','2'],  ['1','^','^','2']
        ]

        correct_message = "Invalid series of symbols."
        for equation in wrong_example_list:
            input = str(equation)   
            test, message = function.simple_solve(equation)
            self.assertEqual(test, False,\
                "input: " + input + " output: " + str(test) + " correct output: False" )
            self.assertIn(correct_message,message,\
                "input: " + input + " Error message is incorrect. It should have: " + correct_message)


        correct_example_list = [
            ['2'],                                                                          ['2.0'],
            ['2.0'],                                                                        ['2.0'],
            ['+','-','2'],                                                                  ['-2.0'],
            ['+','+','2'],                                                                  ['2.0'],
            ['+','2','-','2'],                                                              ['0.0'],
            ['-','2.0'],                                                                    ['-2.0'],
            ['2','+','2','-','2','+','2.0','*','2.0','^','2.0'],                            ['10.0'],
            ['1.0','-2.0','*','3.0','^','4.0'],                                             ['-161.0'],
            ['+','2','^','2','/','2','^','4'],                                              ['0.25'],
            ['1','-','2','*','4','/','2','^','1','+','2','-','4','*','2','/','1','^','2'],  ['-9.0'],
            ['2','^','4','*','6','*','8','-','6','+','4','/','2','/','2'],                  ['763.0']
        ]
        correct_message = "Section solved."
        aux_index = [i*2 for i in range(int(len(correct_example_list)/2))]
        for i in aux_index:
            input  = str(correct_example_list[i])
            output = str(correct_example_list[i+1])
            test, message = function.simple_solve(correct_example_list[i])
            self.assertEqual(test,correct_example_list[i+1],\
                "input: " + input + " output: " + str(test) + " correct output: " +  output)
            self.assertIn(correct_message,message,\
                "input: " + input + " Error message is incorrect. It should have: " + correct_message)                
        
    def test_bracket_solve(self):
        wrong_example_list = [
            ['0','/','0'],  ['1','/','0'],  ['1','/','0','*','*','2'],  ['1','/','(','1','-','1',')']

        ]
        correct_message = "divide by zero."
        for equation in wrong_example_list:
            input = str(equation)            
            result, _, message = function.bracket_solve(equation)
            self.assertEqual(result, False,\
                "input: " + input + " output: " + str(result) + " correct output: False" )
            self.assertIn(correct_message,message,\
                "input: " + input + " Error message is incorrect. It should have: " + correct_message)

        wrong_example_list = [
            ['1','*','*','2'],  ['1','/','/','2'],  ['1','^','^','2'],  ['2','+','*','2'],  ['2','-','/','2'],
            ['2','+','^','2']

        ]
        correct_message = "Invalid series of symbols."
        for equation in wrong_example_list:
            input = str(equation)            
            result, _, message = function.bracket_solve(equation)
            self.assertEqual(result, False,\
                "input: " + input + " output: " + str(result) + " correct output: False" )
            self.assertIn(correct_message,message,\
                "input: " + input + " Error message is incorrect. It should have: " + correct_message)                

        correct_example_list = [
            ['1'],                                                                                  ['1.0'],
            ['2','+','3'],                                                                          ['5.0'],
            ['2','-','3'],                                                                          ['-1.0'],
            ['2','*','3'],                                                                          ['6.0'],
            ['2','^','3'],                                                                          ['8.0'],
            ['-','2','^','-','3'],                                                                  ['-0.125'],
            ['2','^','-','(','1','+','2',')'],                                                      ['0.125'],
            ['1','+','1','(','2','*','3','/','2',')','2','(','(','2','^','2',')','+','2',')','2'],  ['97.0'],
            ['a'],                                                                                  ['a'],
            ['2','a'],                                                                              ['2.0','*','a'],
            ['1','+','a','(','2','*','b','/','2',')','2','(','(','2','^','b',')','+','2',')','b'],  ['1.0','+','a','*','(','2.0','*','b','/','2.0',')','*','2.0','*','(','(','2.0','^','b',')','*','2.0',')','*','b'],
            ['1','=','2','+','3'],                                                                  ['1.0','=','5.0'],
            ['2','-','3','=','2','*','3'],                                                          ['-1.0','=','6.0'],
            ['2','^','3','=','-','2','^','-','3'],                                                  ['8.0','=','-0.125'],
            ['2','^','-','(','1','+','2',')','=','1','/','8'],                                      ['0.125','=','0.125']
        
        ]
        correct_message = "All bracket solved."
        aux_index = [i*2 for i in range(int(len(correct_example_list)/2))]
        for i in aux_index:
            input  = str(correct_example_list[i])
            output = str(correct_example_list[i+1])
            result, equation, message = function.bracket_solve(correct_example_list[i])
            self.assertEqual(result, True,\
                "input: " + input + " output: " + str(result) + " correct output: True" )            
            self.assertEqual(equation,correct_example_list[i+1],\
                "input: " + input + " output: " + str(equation) + " correct output: " +  output)           
            self.assertIn(correct_message,message,\
                "input: " + input + " Error message is incorrect. It should have: " + correct_message)                

    def test_get_simple_result(self):
        true_example_list = [
            ['1.0','=','1.0'],  ['-1.0','=','-1.0']
        ]
        correct_message = "Both sides are equal:"
        for equation in true_example_list:
            input = str(equation)            
            test,_,message = function.get_simple_result(equation)
            self.assertEqual(test, True,\
                "input: " + input + " output: " + str(test) + " correct output: True" )
            self.assertIn(correct_message,message,\
                "input: " + input + " Error message is incorrect. It should have: " + correct_message)                

        false_example_list = [
            ['1.0','=','2.0'],  ['1.0','=','-1.0']
        ]
        correct_message = "Both sides aren't equal:"
        for equation in false_example_list:
            input = str(equation)            
            test,_,message = function.get_simple_result(equation)
            self.assertEqual(test, False,\
                "input: " + input + " output: " + str(test) + " correct output: True" )
            self.assertIn(correct_message,message,\
                "input: " + input + " Error message is incorrect. It should have: " + correct_message)                

        correct_example_list = [
            ['1.0'],            '1.0',
            ['0.12'],           '0.12',
            ['-1.0'],           '-1.0',
        ]
        correct_message = "Answer:"
        aux_index = [i*2 for i in range(int(len(correct_example_list)/2))]
        for i in aux_index:
            input  = str(correct_example_list[i])
            output = str(correct_example_list[i+1])
            _,test,message = function.get_simple_result(correct_example_list[i])
            self.assertEqual(test,correct_example_list[i+1],\
                "input: " + input + " output: " + str(test) + " correct output: " +  output)   
            self.assertIn(correct_message,message,\
                "input: " + input + " Error message is incorrect. It should have: " + correct_message)                                

if __name__ == '__main__':
    unittest.main()
