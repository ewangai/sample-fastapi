import pytest
from app.calculations import add, subtract, multiply, divide, BankAccount,InsufficientFunds

#creating fixtures
@pytest.fixture
def zero_bank_account():
    print("Creating empty bank account")
    return BankAccount()

@pytest.fixture
def bank_account():
    print("Creating bank account with 50")
    return BankAccount(50)

# have the funcitons reference the fixture
#  
#simpler way of tesring with parameterise
#special decorator from pytest
# Provide  alist of numbers wiht expected results
# these will be treated as variables
#then a list of tuples with each test case
@pytest.mark.parametrize("num1, num2, expected", [
    (3,2,5),
    (7,1,8),
    (12,4,16)                                             
]) 

def test_add(num1, num2, expected): #function to test and fail if errors are passed.
    print("Testing add function") # match with decorator vars
    assert add(num1, num2) == expected  # False #Assets evaluates a test when Assert= True nothing happens, otherwise error.

def test_subtract():
    assert subtract(9, 4) == 5


def test_multiply():
    assert multiply(4, 3) == 12


def test_divde():
    assert divide(20, 5) == 4




def test_bank_set_initial_amount(bank_account): # Make tests descriptive
    #bank_account = BankAccount(50) # instance of the class
    assert bank_account.balance == 50

def test_bank_default_amount(zero_bank_account): # Make tests descriptive
    print("testing my bank account")
    #bank_account = BankAccount() # instance of the class
    assert zero_bank_account.balance == 0

def test_withdraw(bank_account): # Make tests descriptive
    # replaced with fixture bank_account = BankAccount(bank_account) # instance of the class
    bank_account.withdraw(30) # call withdraw methos
    assert bank_account.balance == 20


def test_deposit(bank_account):
    #bank_account = BankAccount(bank_account) # instance of the class
    bank_account.deposit(30) # call withdraw methos
    assert bank_account.balance == 80


def test_collect_interest(bank_account):
    #bank_account = BankAccount(50) # instance of the class
    bank_account.collect_interest() # call withdraw methos
    #assert bank_account.balance == 55 #assert 55.00000000000001 == 55
    assert round(bank_account.balance,6) == 55 # comparing int and float


def test_bank_transaction(zero_bank_account): # can parameterise and create complex scenarios
    print("testing my bank account transaction")
    zero_bank_account.deposit(200)
    zero_bank_account.withdraw(100)
    assert zero_bank_account.balance == 100
    
@pytest.mark.parametrize("deposited, withdrew, expected", [
    (200,100,100),
    (1200,200,1000),
    (50,10,40)                                            

])

#fixture first params second
def test_bank_transaction(zero_bank_account, deposited, withdrew, expected): # can parameterise and create complex scenarios
    print("testing my bank account transaction with parameters")
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected

#if you expect an error, create different test case

def test_insufficient_funds(bank_account): # can parameterise and create complex scenarios
    print("testing insufficient funds")
    with pytest.raises(InsufficientFunds): # pass in this instance detects the exception
        bank_account.withdraw(200)
    #assert bank_account.balance == expected