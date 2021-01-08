import inforella


def test_is_char_in_quotes():
	assert inforella.is_char_in_quotes('=','a = 10') == True
	assert inforella.is_char_in_quotes('=','"="') == False
	assert inforella.is_char_in_quotes('=','a = "="') == True

test_is_char_in_quotes()