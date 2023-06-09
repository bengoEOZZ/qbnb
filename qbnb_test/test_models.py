from qbnb.models import create_listing, login, update_user, db, User
from qbnb.models import register, update_listing, datetime, create_booking


def test_r0_user_register():
    # test users for login
    assert register('user0', 'test0@test.com', '123aB!') is not None
    assert register('user1', 'test1@test.com', '456ZxY?') is not None


def test_r1_1_user_register():
    '''
    Testing R1-1: Email cannot be empty. password cannot be empty
    '''

    assert register('userr11a', 'testr11a@test.com', '!2ASDa') is not None
    assert register('userr11b', '', '!2ASDa') is None
    assert register('userr11c', 'testr11b@test.com', '') is None
    assert register('userr11d', '', '') is None


def test_r1_2_user_register():
    '''
    Testing R1-2: A user is uniquely identified 
    by his/her user id - automatically generated.
    '''

    register('userr12a', "testr12a@test.com", "!$weAr14")
    register('userr12b', "testr12b@test.com", "!$weAr14")
    
    user_one = User.query.filter_by(email="testr12a@test.com").first()
    user_two = User.query.filter_by(email="testr12b@test.com").first()
    
    assert (user_one.id == user_two.id) is False

    
def test_r1_3_user_register():
    '''
    Testing R1-3: The email has to follow addr-spec defined in RFC 5322
    '''

    assert register('userr13a', 'testr13acom', "AaBc!23") is None


def test_r1_4_user_register():
    '''
    Testing R1-4: Password has to meet the required
     complexity: minimum length 6, 
    at least one upper case, at least one lower case, 
    and at least one special character.
    '''

    assert register('userr14a', 'testr14a@test.com', '!2Aa') is None
    assert register('user14b', 'testr14b@test.com', 'hello123') is None
    assert register('user14c', 'testr14c@test.com', 'ASD123!!!') is None
    assert register('userr14d', 'testr14d@test.com', '123ASDads') is None


def test_r1_5_user_register():
    '''
    Testing R1-5: User name has to be non-empty, alphanumeric-only,
    and space allowed only if it is not as the prefix or suffix.
    '''

    assert register("", 'testr15a@test.com', '123!asdA') is None
    assert register('aasd@@@', 'testr15b@test.com', '123!asdA') is None
    assert register(' Hello', 'testr15c@test.com', '123!asdA') is None


def test_r1_6_user_register():
    '''
    Testing R1-6:  User name has to be longer than 2 
    characters and less than 20 characters.
    '''

    assert register('aa', "testr16a@test.com", "123!asdA") is None
    assert register('aaaaaAAAAAbbbbbBBBBBc', 
                    "testr16b@test.com", "123!asdA") is None


def test_r1_7_user_register():
    '''
    Testing R1-7: If the email has been used, the operation failed.
    '''

    assert register('userr17a', 'testr17a@test.com', '123aB!') is not None
    assert register('userr17b', 'testr17b@test.com', '456ZxY?') is not None
    assert register('userr17c', 'testr17a@test.com', '12Aac>56') is None


def test_r1_8_user_register():
    '''
    Testing R1-8: Shipping address is empty at the time of registration.
    '''

    register('userr18', "testr18@test.com", "!$weAr14")
    user = User.query.filter_by(email="testr18@test.com").first()
    assert (user.billing_address == '') is not None


def test_r1_9_user_register():
    '''
    Testing R1-9: Postal is empty at the time of registration.
    '''

    register('userr19', "testr19@test.com", "!$weAr14")
    user = User.query.filter_by(email="testr19@test.com").first()
    assert (user.postal_code == '') is not None


def test_r1_10_user_register():
    '''
    Testing R1-10: Balance should be initialized as 
    100 at the time of registration. q
    '''

    register('userr110', "testr110@test.com", "!$weAr14")
    user = User.query.filter_by(email="testr110@test.com").first()
    assert (user.balance == 100) is not None


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


def test_r4_1_create_list():
    '''
    Testing R4-1: Title of the product has to be alphanumeric-only,
                  and space allowed only if it is not as prefix and suffix. 
    '''
    description = "This is a new nice home"
    date = "2021-01-06"
    email = "test0@test.com"

    # leading space in title
    listing = create_listing(" New Home", description, 1000, date, email)
    assert listing is None

    # trailing space in title
    listing = create_listing("New Home ", description, 1000, date, email)
    assert listing is None

    # correct implementation
    listing = create_listing("New1 2Home", description, 1000, date, email)
    assert listing is not None


def test_r4_2_create_list():
    '''
    Testing R4-2: The title of the product is no longer than 80 characters.
    '''
    description = "This is a new home"
    date = "2021-01-06"
    email = "test0@test.com"

    # 81 character title
    listing = create_listing("X" * 81, description, 1000, date, email)
    assert listing is None


def test_r4_3_create_list():
    '''
    Testing R4-3: The description of the product can be arbitrary characters,
                  with a minimum length of 20 characters and a maximum of
                  2000 characters.
    '''
    description = "This is a new home"
    date = "2021-01-06"
    email = "test0@test.com"

    # length of description less than 20
    listing = create_listing("New Home", description, 1000, date, email)
    assert listing is None


def test_r4_4_create_list():
    '''
    Testing R4-4: Description has to be longer than the product's title.
    '''
    date = "2021-01-06"
    email = "test0@test.com"

    # length of description shorter than length of title
    listing = create_listing("New Home", "This", 1000, date, email)
    assert listing is None


def test_r4_5_create_list():
    '''
    Testing R4-5: Price has to be of range [10, 10000].
    '''
    description = "This is a new nice home"
    date = "2021-01-06"
    email = "test0@test.com"

    # price too low
    listing = create_listing("New Home", description, 9, date, email)
    assert listing is None

    # price too high
    listing = create_listing("New Home", description, 20000, date, email)
    assert listing is None


def test_r4_6_create_list():
    '''
    Testing R4-6: last_modified_date must be after 2021-01-02
                  and before 2025-01-02.
    '''
    description = "This is a new nice home"
    date1 = "2021-01-01"
    date2 = "2025-01-03"
    date3 = "2023-11-31"
    email = "test0@test.com"

    # date before valid date
    listing = create_listing("New Home", description, 1000, date1, email)
    assert listing is None

    # date after valid date
    listing = create_listing("New Home", description, 1000, date2, email)
    assert listing is None

    # date does not exist
    listing = create_listing("New Home", description, 1000, date3, email)
    assert listing is None


def test_r4_7_create_list():
    '''
    Testing R4-7: owner_email cannot be empty. The owner of the corresponding
                  product must exist in the database.
    '''
    # empty owner email
    description = "This is a new nice home"
    date = "2021-01-06"
    email = "test15@test.com"
    listing = create_listing("New1 2Home", description, 1000, date, " ")
    assert listing is None

    # email does not exist in the database
    listing = create_listing("New1 2Home", description, 1000, date, email)
    assert listing is None


def test_r4_8_create_list():
    '''
    Testing R4-8: A user cannot create products that have the same title.
    '''
    # title already exists in database
    description = "This is a new nice home"
    date = "2021-01-06"
    email = "test0@test.com"
    listing1 = create_listing("New1 2Home", description, 1000, date, email)
    assert listing1 is None


def test_r5_1_update_listing():
    '''
    Testing R5-1: One can update all attributes of the listing,
    except owner_id and last_modified_date.
    '''
    create_listing("New1 2Home", "This is a new nice home", 1000,
                   "2021-01-06", "test0@test.com")
    listing = update_listing("test0@test.com", "New1 3Home",
                             "This is a not nice home", 1001)
    # Shows that the listing is created
    assert listing is not None
    # Shows that the owner id is not changed
    assert listing.owner_id == "test0@test.com"
    # Shows that the title is updated
    assert listing.title == "New1 3Home"
    # Shows that the description is updated
    assert listing.description == "This is a not nice home"
    assert listing.price == 1001
    # Shows that the price is updated


def test_r5_2_update_listing():
    '''
    Testing R5-2: Price can be only increased but cannot be decreased :).
    '''
    create_listing("New1 2Home", "This is a new nice home", 1000,
                   "2021-01-06", "test0@test.com")
    listing = update_listing("test0@test.com", "N/A", "N/A", 2000)
    # Shows that the listing is created if the price updates to a higher value
    assert listing is not None
    # Shows that the listing is None if it is a lower value
    listing = update_listing("test0@test.com", "N/A", "N/A", 1999)
    assert listing is None


def test_r5_3_update_listing():
    '''
    Testing R5-3: last_modified_date should be updated when the
    update operation is successful.
    '''
    create_listing("New1 2Home", "This is a new nice home", 1000,
                   "2021-01-06", "test0@test.com")
    listing = update_listing("test0@test.com", "N/A", "N/A", 2000)
    # Shows that the listing is None if it is a lower value
    assert listing.last_modified_date == datetime.date.today()


def test_r5_4_update_listing():
    '''
    R5-4: When updating an attribute, one has to make sure
    that it follows the same requirements as above.
    '''
    create_listing("New1 2Home", "This is a new nice home",
                   1000, "2021-01-06", "test0@test.com")
    # Tests the title
    listing = update_listing("test0@test.com", "./csa.", "N/A", -1)
    assert listing is None
    # Tests the description
    listing = update_listing("test0@test.com", "N/A", "ha.", -1)
    assert listing is None
    # Tests the price
    listing = update_listing("test0@test.com", "N/A", "N/A", 3)
    assert listing is None


def test_1_create_booking():
    '''
    A user can book a listing.
    '''
    user_email = "tommy17@email.com"
    listing_title = "Big House"
    owner = register("frank0", "frank0@email.com", "abC12!")

    listing = (create_listing(listing_title, "This is a new nice big house", 
                              100, "2022-01-01", owner.email))
    user = register("tommy17", user_email, "abC12!")
    assert listing is not None
    assert user is not None

    booking = (create_booking(user.email, listing_title, 
                              "2022-01-06", "2022-01-09"))
    assert booking is not None


def test_2_create_booking():
    '''
    A user cannot book a listing for his/her listing.
    '''
    listing_title = "Large House"
    owner = register("frank1", "frank1@email.com", "abC12!")

    listing = (create_listing(listing_title, "This is a new nice big house", 
                              100, "2022-01-01", owner.email))
    assert listing is not None
    assert owner is not None

    booking = (create_booking(owner.email, listing_title, 
                              "2022-01-06", "2022-01-09"))
    assert booking is None


def test_3_create_booking():
    '''
    A user cannot book a listing that costs more than his/her balance.
    '''
    user_email = "tommy20@email.com"
    listing_title = "Giant House"
    owner = register("frank20", "frank20@email.com", "abC12!")

    listing = (create_listing(listing_title, "This is a new nice big house", 
                              200, "2022-01-01", owner.email))
    # default user balance is $100
    user = register("tommy20", user_email, "abC12!")
    assert listing is not None
    assert user is not None

    booking = (create_booking(user.email, listing_title, 
                              "2022-01-06", "2022-01-09"))
    assert booking is None


def test_4_create_booking():
    '''
    A user cannot book a listing that is 
    already booked with the overlapped dates.
    '''
    user_email = "tommy30@email.com"
    user2_email = "johnny30@email.com"
    listing_title = "Tiny House"
    owner = register("frank30", "frank30@email.com", "abC12!")

    listing = (create_listing(listing_title, "This is a new nice big house", 
                              100, "2022-01-01", owner.email))
    user = register("tommy30", user_email, "abC12!")
    user2 = register("johnny30", user2_email, "abC12!")
    assert listing is not None
    assert user is not None
    assert user2 is not None

    user_booking = (create_booking(user.email, listing_title, 
                                   "2022-01-06", "2022-01-09"))
    # this overlaps
    user2_booking = (create_booking(user2.email, listing_title, 
                                    "2022-01-05", "2022-01-08"))
    assert user2_booking is None


def test_5_create_booking():
    '''
    A user and owner balances get updated
    '''
    user_email = "tommy18@email.com"
    listing_title = "Small House"
    owner = register("frank00", "frank00@email.com", "abC12!")

    listing = (create_listing(listing_title, "This is a new nice big house", 
                              100, "2022-01-01", owner.email))
    user = register("tommy18", user_email, "abC12!")
    assert listing is not None
    assert user is not None

    booking = (create_booking(user.email, listing_title, 
                              "2022-01-06", "2022-01-09"))
    assert booking is not None
    assert user.balance == 0
    assert owner.balance == 200