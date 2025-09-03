import pytest

def test_equal_or_not_equal():
    assert 3 == 3
    assert 3 != 1

def test_is_istance():
    assert isinstance('string', str)
    assert isinstance(10, int)

def test_boolean():
    validated = True
    assert validated is True
    assert ('hello' == 'olá') is False

def test_types():
    assert type('hello' is str)
    assert type('hello' is not int)

def test_greater_and_less_than():
    assert 7 > 2
    assert 10 < 20

def test_list():
    num_list = [1, 2, 3, 4]
    any_list = [False, False]
    assert 1 in num_list
    assert 7 not in num_list
    assert all(num_list)
    assert not any(any_list)

class User:
    def __init__(self, first_name: str, last_name: str, email: str, password: str, phone_number: str):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.phone_number = phone_number

@pytest.fixture
def default_user():
    return User('Lucas', 'Berenger', 'lucas@io.com', 'lucas123', '(21)96481-9380')

def test_user_creation(default_user):
    assert default_user.first_name == 'Lucas', 'First name should be Lucas'
    assert default_user.last_name == 'Berenger', 'Last name should be Berenger'
    assert default_user.email == 'lucas@io.com', 'email should be lucas@io.com'
    assert default_user.password == 'lucas123', 'password should be lucas123'
    assert default_user.phone_number == '(21)96481-9380', 'phone number should be (21)96481-9380'