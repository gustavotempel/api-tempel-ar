from tempel.app import custom_response, add_single_quotes_to_str


def test_health():
    assert True


def test_response():
    response = custom_response(body="response_ok")
    expected_response = ("response_ok", 200, {"Access-Control-Allow-Origin": "*"})
    assert response == expected_response


def test_add_single_quotes_to_str():
    assert add_single_quotes_to_str("string_value") == "'string_value'"
    assert add_single_quotes_to_str("") == "''"
    assert add_single_quotes_to_str(123) == 123
    assert add_single_quotes_to_str(123.0) == 123.0
    assert add_single_quotes_to_str(True) == True
    assert add_single_quotes_to_str(None) == None