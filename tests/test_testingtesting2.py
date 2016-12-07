from context import multiply, divide


def test_numbers_5_8():
#    assert testingtesting.multiply(3,4) == 12 
    assert multiply(5,8) == 40 
 
def test_strings_a_3():
#    assert testingtesting.multiply('a',3) == 'aaa' 
    assert multiply('qw',3) == 'qwqwqw'

def test_numbers_div_48_6():
#    assert testingtesting.multiply(3,4) == 12 
    assert divide(48,8) == 6 
 
def test_strings_div_qw_3():
#    assert testingtesting.multiply('a',3) == 'aaa' 
    assert divide('qw',3) == 'Invalid input'


    