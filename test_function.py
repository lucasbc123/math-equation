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
        for equation in type_list:
            input = str(equation)
            test = function.simple_character_check(equation)
            self.assertEqual(test, False,\
                "input: " + input + " output: " + str(test) + " correct output: False" )

        wrong_example_list = [
            '',
            '  ',
            '         '
        ]

        for equation in wrong_example_list:
            input = str(equation)
            test = function.simple_character_check(equation)
            self.assertEqual(test, False,\
                "input: " + input + " output: " + str(test) + " correct output: False" )

        wrong_example_list = [
            '1==1', '2=2=2'
        ]
        for equation in wrong_example_list:
            input = str(equation)
            test = function.simple_character_check(equation)
            self.assertEqual(test, False,\
                "input: " + input + " output: " + str(test) + " correct output: False" )

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
        aux_index = [i*2 for i in range(int(len(correct_example_list)/2))]
        for i in aux_index:
            test = function.simple_character_check(correct_example_list[i])
            self.assertEqual(test,correct_example_list[i+1],\
                "input: " + str(correct_example_list[i]) + " output: " + str(test) + " correct output: " + str(correct_example_list[i+1]))

        

        
    def test_validate_groupers(self):
        wrong_example_list = [
            '1+2+(3',   '1+2)+3',   '1+2+[3',   '1+2]+3',   '1+2+{3',   '1+2}+3',   '(1+2]',
            '(1+2}',    '[1+2)',    '[1+2}',    '{1+2)',    '{1+2]',    '(1+2[1+2)]'
        ]

        for equation in wrong_example_list:
            input = str(equation)
            test = function.validate_groupers(equation)
            self.assertEqual(test, False,\
                "input: " + input + " output: " + str(test) + " correct output: False" )    

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

        aux_index = [i*2 for i in range(int(len(correct_example_list)/2))]
        for i in aux_index:
            input  = str(correct_example_list[i])
            output = str(correct_example_list[i+1])
            test = function.validate_groupers(correct_example_list[i])
            self.assertEqual(test,correct_example_list[i+1],\
                "input: " + input + " output: " + str(test) + " correct output: " +  output)

    def test_list_transform(self):
        wrong_example_list = [
            '1.1.*1',
            '.1.*1',
            '..1*1',
            '1*.*1',
        ]

        for equation in wrong_example_list:
            input = str(equation)
            test = function.list_transform(equation)
            self.assertEqual(test, False,\
                "input: " + input + " output: " + str(test) + " correct output: False" )    

        correct_example_list = [
            '12',                   ['12'],
            '12.12',                ['12.12'],
            '.12',                  ['0.12'],
            '12.',                  ['12'],
            'abc',                  ['a','b','c'],
            '(1+1.-.1*1.1/a^b)',    ['(','1','+','1','-','0.1','*','1.1','/','a','^','b',')']
        ]

        aux_index = [i*2 for i in range(int(len(correct_example_list)/2))]
        for i in aux_index:
            input  = str(correct_example_list[i])
            output = str(correct_example_list[i+1])
            test = function.list_transform(correct_example_list[i])
            self.assertEqual(test,correct_example_list[i+1],\
                "input: " + input + " output: " + str(test) + " correct output: " +  output)
                
    def test_insert_multiplication_symbol(self):
        correct_example_list = [
            ['2'],                                                          ['2'],
            ['a'],                                                          ['a'],
            ['a','b'],                                                      ['a','*','b'],
            ['a','*','b'],                                                  ['a','*','b'],
            ['a','+','b'],                                                  ['a','+','b'],
            ['(','2',')','2'],                                              ['(','2',')','*','2'],
            ['2','(','2',')'],                                              ['2','*','(','2',')'],
            ['a','2','+','(','a','b',')','a'],                              ['a','*','2','+','(','a','*','b',')','*','a'],
            ['1.0','-2.0','*','3.0','^','4.0'],                             ['1.0','-2.0','*','3.0','^','4.0'],
            ['1','a','(','2','b',')','(','2','(','(','a',')','a',')',')'],  ['1','*','a','*','(','2','*','b',')','*','(','2','*','(','(','a',')','*','a',')',')']
        ]

        aux_index = [i*2 for i in range(int(len(correct_example_list)/2))]
        for i in aux_index:
            input  = str(correct_example_list[i])
            output = str(correct_example_list[i+1])
            test = function.insert_multiplication_symbol(correct_example_list[i])
            self.assertEqual(test,correct_example_list[i+1],\
                "input: " + input + " output: " + str(test) + " correct output: " +  output)

    def test_simplify_plus_minus(self):
        correct_example_list = [
            ['2'],                                              ['2'],
            ['2','+','2'],                                      ['2','+','2'],
            ['2','-','2'],                                      ['2','-','2'],
            ['2','+','-','2'],                                  ['2','-','2'],
            ['2','-','+','2'],                                  ['2','-','2'],
            ['-','+','2','+','-','+','2','+','+','-','-','2'],  ['-','2','-','2','+','2'],
            
        ]
        aux_index = [i*2 for i in range(int(len(correct_example_list)/2))]
        for i in aux_index:
            input  = str(correct_example_list[i])
            output = str(correct_example_list[i+1])
            test = function.simplify_plus_minus(correct_example_list[i])
            self.assertEqual(test,correct_example_list[i+1],\
                "input: " + input + " output: " + str(test) + " correct output: " +  output)

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
            ['1','/','0'],  ['1','/','0','*','2'],  ['1','*','*','2'],  ['1','/','/','2'],
            ['1','^','^','2']
        ]

        for equation in wrong_example_list:
            input = str(equation)   
            test = function.simple_solve(equation)
            self.assertEqual(test, False,\
                "input: " + input + " output: " + str(test) + " correct output: False" )   

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

        aux_index = [i*2 for i in range(int(len(correct_example_list)/2))]
        for i in aux_index:
            input  = str(correct_example_list[i])
            output = str(correct_example_list[i+1])
            test = function.simple_solve(correct_example_list[i])
            self.assertEqual(test,correct_example_list[i+1],\
                "input: " + input + " output: " + str(test) + " correct output: " +  output)
        
    def test_bracket_solve(self):
        wrong_example_list = [
            ['0','/','0'],  ['1','/','0'],  ['1','/','0','*','2'],  ['1','*','*','2'],  ['1','/','/','2'],
            ['1','^','^','2'],  ['1','/','(','1','-','1',')'],  ['2','+','*','2'],  ['2','-','/','2'],
            ['2','+','^','2']

        ]

        for equation in wrong_example_list:
            input = str(equation)            
            test = function.bracket_solve(equation)
            self.assertEqual(test, False,\
                "input: " + input + " output: " + str(test) + " correct output: False" )

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

        aux_index = [i*2 for i in range(int(len(correct_example_list)/2))]
        for i in aux_index:
            input  = str(correct_example_list[i])
            output = str(correct_example_list[i+1])
            test = function.bracket_solve(correct_example_list[i])
            self.assertEqual(test,correct_example_list[i+1],\
                "input: " + input + " output: " + str(test) + " correct output: " +  output)           

    def test_get_simple_result(self):
        true_example_list = [
            ['1.0','=','1.0'],  ['-1.0','=','-1.0']
        ]

        for equation in true_example_list:
            input = str(equation)            
            test = function.get_simple_result(equation)
            self.assertEqual(test, True,\
                "input: " + input + " output: " + str(test) + " correct output: True" )

        false_example_list = [
            ['1.0','=','2.0'],  ['1.0','=','-1.0']
        ]

        for equation in false_example_list:
            input = str(equation)            
            test = function.get_simple_result(equation)
            self.assertEqual(test, False,\
                "input: " + input + " output: " + str(test) + " correct output: True" )

        correct_example_list = [
            ['1.0'],            '1.0',
            ['0.12'],           '0.12',
            ['-1.0'],           '-1.0',
        ]

        aux_index = [i*2 for i in range(int(len(correct_example_list)/2))]
        for i in aux_index:
            input  = str(correct_example_list[i])
            output = str(correct_example_list[i+1])
            test = function.get_simple_result(correct_example_list[i])
            self.assertEqual(test,correct_example_list[i+1],\
                "input: " + input + " output: " + str(test) + " correct output: " +  output)   

if __name__ == '__main__':
    unittest.main()