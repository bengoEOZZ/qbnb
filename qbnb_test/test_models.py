from qbnb.models import login, update_user, db, User
# from qbnb.models import register, login


# def test_r1_7_user_register():
#     '''
#     Testing R1-7: If the email has been used, the operation failed.
#     '''

#     assert register('user0', 'test0@test.com', '123aB!') is True
#     assert register('user0', 'test1@test.com', '456ZxY?') is True
#     assert register('user1', 'test0@test.com', '123456') is False

# test users for login because i dont have register function
db.session.add(User(email="test0@test.com", password="123aB!", 
                    username="user0", billing_address="000", 
                    postal_code="", balance="000"))
db.session.add(User(email="test1@test.com", password="456ZxY?", 
                    username="user1", billing_address="111", 
                    postal_code="", balance="000"))
db.session.commit()


def test_r2_1_login():
    '''
    Testing R2-1: A user can log in using her/his email address 
      and the password.
    (will be tested after the previous test, so we already have user0, 
      user1 in database)
    '''

    # good login
    user = login('test0@test.com', "123aB!")
    assert user is not None
    assert user.username == 'user0'

    # wrong password
    user = login('test0@test.com', "123aB!c")
    assert user is None


def test_r2_2_login():
    '''
    Testing R2-2: The login function should check if the supplied 
    inputs meet the same email/password requirements as above, 
    before checking the database.
    (will be tested after the previous test, so we already have user0, 
      user1 in database)
    '''
    # invalid email
    user = login('test0@testcom', "123aB!")
    assert user is None

    # invalid password
    user = login('test0@test.com', "1234567")
    assert user is None


def test_r3_1_update():
    '''
    Testing R3-1: A user is only able to update his/her user name, 
    user email, billing address, and postal code.
    (will be tested after the previous test, so we already have user0, 
      user1 in database)
    '''
    # update username
    user = update_user('test0@test.com', "user00", "", "", "A1A1A1")
    assert user is not None
    assert user.username == 'user00'
    # revert to old username for testing purposes
    user = update_user('test0@test.com', "user0", "", "", "A1A1A1")

    # update email
    user = update_user('test0@test.com', "", "test00@test.com", "", "A1A1A1")
    assert user is not None
    assert user.username == 'user0'
    assert user.email == 'test00@test.com'
    # revert to old email for testing purposes
    user = update_user('test00@test.com', "", "test0@test.com", "", "A1A1A1")

    # update billing address
    user = update_user('test0@test.com', "", "", "77 Long Road", "A1A1A1")
    assert user is not None
    assert user.username == 'user0'
    assert user.billing_address == "77 Long Road"

    # update postal code
    user = update_user('test0@test.com', "", "", "", "K2C4V1")
    assert user is not None
    assert user.username == 'user0'
    assert user.postal_code == 'K2C4V1'

    # update all
    user = update_user('test0@test.com', "user123", 
                       "test123@test.com", "88 My House", "C2C3B2")
    assert user is not None
    assert user.username == 'user123'
    assert user.email == 'test123@test.com'
    assert user.billing_address == '88 My House'
    assert user.postal_code == "C2C3B2"
    # revert to old username and email for testing purposes
    user = update_user('test123@test.com', "user0", 
                       "test0@test.com", "", "A1A1A1")


def test_r3_2_update():
    '''
    Testing R3-2: postal code should be non-empty, alphanumeric-only, 
    and no special characters such as !.
    (will be tested after the previous test, so we already have user0, 
      user1 in database)
    '''
    # non-empty, alphanumeric only postal code
    user = update_user('test0@test.com', "", "", "", "A2A2A2")
    assert user is not None
    assert user.username == 'user0'
    assert user.postal_code == 'A2A2A2'

    # empty postal code
    user = update_user('test0@test.com', "", "", "", "")
    assert user is None

    # non-alphanumeric-only postal code
    user = update_user('test0@test.com', "", "", "", "A!A1A1")
    assert user is None


def test_r3_3_update():
    '''
    Testing R3-3: Postal code has to be a valid Canadian postal code.
    (will be tested after the previous test, so we already have user0, 
      user1 in database)
    '''

    # valid postal code
    user = update_user('test0@test.com', "", "", "", "K2B2C4")
    assert user is not None
    assert user.username == 'user0'
    assert user.postal_code == "K2B2C4"

    # invalid postal code
    user = update_user('test0@test.com', "", "", "", "2B2C4")
    assert user is None

    # invalid postal code
    user = update_user('test0@test.com', "", "", "", "1234566")
    assert user is None


def test_r3_4_update():
    '''
    Testing R3-4: User name is alphanumeric-only, and space 
    allowed only if it is not as the prefix or suffix.
    (will be tested after the previous test, so we already have user0, 
      user1 in database)
    '''

    # User name is alphanumeric-only
    user = update_user('test0@test.com', "123123test123", "", "", "A1A1A1")
    assert user is not None
    assert user.username == "123123test123"
    # # revert to old username for testing purposes
    # user = update_user('test0@test.com', "user0", "", "", "A1A1A1")

    # User name is alphanumeric-only, space not prefix or sufix
    user = update_user('test0@test.com', "123 123 test123", "", "", "A1A1A1")
    assert user is not None
    assert user.username == '123 123 test123'

    # User name is not alphanumeric-only
    user = update_user('test0@test.com', "123!123!test@123", "", "", "A1A1A1")
    assert user is None

    # User name is has space at the prefix
    user = update_user('test0@test.com', " 123123test123", "", "", "A1A1A1")
    assert user is None
    
    # User name is has space at the suffix
    user = update_user('test0@test.com', " 123123test123 ", "", "", "A1A1A1")
    assert user is None
    # revert to old username for testing purposes
    # user = update_user('test0@test.com', "user0", "", "", "A1A1A1")