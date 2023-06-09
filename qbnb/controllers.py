import email
import datetime
from flask import render_template, request, session, redirect
from qbnb.models import login, User, Listing, register, create_listing
from qbnb.models import update_listing, update_user, create_booking
from qbnb.models import Booking


from qbnb import app


def authenticate(inner_function):
    """
    :param inner_function: any python function that accepts a user object
    Wrap any python function and check the current session to see if
    the user has logged in. If login, it will call the inner_function
    with the logged in user object.
    To wrap a function, we can put a decoration on that function.
    Example:
    @authenticate
    def home_page(user):
        pass
    """

    def wrapped_inner():

        # check did we store the key in the session
        if 'logged_in' in session:
            email = session['logged_in']
            try:
                user = User.query.filter_by(email=email).one_or_none()
                if user:
                    # if the user exists, call the inner_function
                    # with user as parameter
                    return inner_function(user)
            except Exception:
                pass
        else:
            # else, redirect to the login page
            return redirect('/login')

    # return the wrapped version of the inner_function:
    return wrapped_inner


@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html', message='Please login')


@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    user = login(email, password)
    if user:
        session['logged_in'] = user.email
        """
        Session is an object that contains sharing information
        between a user's browser and the end server.
        Typically it is packed and stored in the browser cookies.
        They will be past along between every request the browser made
        to this services. Here we store the user object into the
        session, so we can tell if the client has already login
        in the following sessions.
        """
        # success! go back to the home page
        # code 303 is to force a 'GET' request
        return redirect('/', code=303)
    else:
        return render_template('login.html', message='login failed')


@app.route('/')
@authenticate
def home(user):
    # authentication is done in the wrapper function
    # see above.
    # by using @authenticate, we don't need to re-write
    # the login checking code all the time for other
    # front-end portals

    # update this and replace with real listings once 
    # create listing interface is implemented
    listings = [
        {'Title': 'Apartment 85',
            'Description': "Exteremly garbage rent out place.",
            'Price': 150,
            'Date': "2022-01-01", 'Email': 'ownerman@gmail.com'},
        {'Title': 'Apartment 68',
            'Description': "A Appartment with a 1 table and a chair.",
            'Price': 300, 'Date': "2022-02-01", 'Email': 'ownerman@gmail.com'},
        {'Title': 'Apartment 100',
            'Description': "Top tier apartment, coat hanger made of gold",
            'Price': 1000, 'Date': "2022-03-01",
            'Email': 'ownerman@gmail.com'},
        {'Title': 'John Buckle House',
            'Description': "This is just my house man, please buy.",
            'Price': 500, 'Date': "2022-02-01",
            'Email': 'johnbucklenickle@gmail.com'},
        {'Title': 'Cardboard Box',
            'Description': "It's next to the convenience store, convenient.",
            'Price': 151, 'Date': "2022-01-01",
            'Email': 'ineedatenantplease@gmail.com'},
        {'Title': 'Worn Down House',
            'Description': "Infested with squids. half-underwater.",
            'Price': 500, 'Date': "2022-02-01",
            'Email': 'pleasebymyplace@gmail.com'},
    ]
    bookings = [
        {'Email': 'poorman@gmail.com', 'ListingTitle': 'Apartment 85',
            'StartDate': '2022-01-01', 'EndDate': "2022-01-05"},
        {'Email': 'poorman@gmail.com', 'ListingTitle': 'Cardboard Box',
            'StartDate': '2022-01-05', 'EndDate': "2022-01-20"},
        {'Email': 'johnwife@gmail.com', 'ListingTitle': 'John Bubkle House',
            'StartDate': '2022-02-01', 'EndDate': "2022-03-04"},
        {'Email': 'aquamanreal@gmail.com', 'ListingTitle': 'Worn Down House',
            'StartDate': '2022-02-01', 'EndDate': "2022-03-02"},
    ]
    return render_template('index.html', user=user, listings=listings,
                           bookings=bookings)


@app.route('/register', methods=['GET'])
def register_get():
    # templates are stored in the templates folder
    return render_template('register.html', message='')


@app.route('/register', methods=['POST'])
def register_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    error_message = None

    if password != password2:
        error_message = "The passwords do not match"
    else:
        # use backend api to register the user
        success = register(name, email, password)
        if not success:
            error_message = "Registration failed."
    # if there is any error messages when registering new user
    # at the backend, go back to the register page.
    if error_message:
        return render_template('register.html', message=error_message)
    else:
        return redirect('/login')


@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in', None)
    return redirect('/')


@app.route('/create_listing', methods=['GET'])
def listing_creation_get():
    # templates are stored in the templates folder
    return render_template('create_listing.html', message='Create Listing')


@app.route('/create_listing', methods=['POST'])
def listing_creation_post():
    title = request.form.get('title')
    description = request.form.get('description')
    price_get = request.form.get('price')
    last_modified_date = request.form.get('last_modified_date')
    email = request.form.get('email')
    error_message = None

    try:
        int(price_get)

    except ValueError:
        error_message = "Please enter an integer for price."
        return render_template('create_listing.html', message=error_message)
        
    price = int(price_get)
    # use backend api to creating listing instance
    success = create_listing(title, description, 
                             price, last_modified_date, email)

    if not success:
        error_message = "Listing Creation Failed."
    # if there is any error messages when registering new user
    # at the backend, go back to the register page.
    if error_message:
        return render_template('create_listing.html', message=error_message)
    else:
        return render_template('create_listing.html', 
                               message="Listing Created.")
 

@app.route('/update_listing', methods=['GET'])
def listing_update_get():
    # templates are stored in the templates folder
    return render_template('update_listing.html', message='Update Listing')


@app.route('/update_listing', methods=['POST'])
def listing_update_post():
    email = request.form.get('email')
    title = request.form.get('title')
    description = request.form.get('description')
    price_get = request.form.get('price')
    last_modified_date = request.form.get('last_modified_date')
    error_message = None

    try:
        int(price_get)

    except ValueError:
        error_message = "Please enter an integer for price."
        return render_template('update_listing.html', message=error_message)
        
    price = int(price_get)
    # use backend api to create update listing instance
    success = update_listing(email, title, description, price)

    if not success:
        error_message = "Listing Update Failed."
    # if there is any error messages when registering new user
    # at the backend, go back to the register page.
    if error_message:
        return render_template('update_listing.html', message=error_message)
    else:
        return render_template('update_listing.html', 
                               message="Listing Updated.")


@app.route('/update_profile', methods=['GET'])
def profile_update_get():
    # templates are stored in the templates folder
    return render_template('update_profile.html', message='Update Profile')


@app.route('/update_profile', methods=['POST'])
def profile_update_post():
    old_email = request.form.get('old_email')
    new_email = request.form.get('new_email')
    username = request.form.get('username')
    billing_address = request.form.get('billing_address')
    postal_code = request.form.get('postal_code')
 
    # Use backend api to update the user
    updated_user = update_user(old_email, username, new_email,
                               billing_address, postal_code)
   
    # Return user update page
    if updated_user is not None:
        return render_template('update_profile.html',
                               message="User Profile has been updated.")
    else:
        return render_template('update_profile.html',
                               message="User Profile update has failed.")


@app.route('/create_booking', methods=['GET'])
def booking_creation_get():
    # templates are stored in the templates folder
    return render_template('create_booking.html', message='Create Booking')


@app.route('/create_booking', methods=['POST'])
def booking_creation_post():
    user_email = request.form.get('user_email')
    listing_title = request.form.get('listing_title')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    error_message = None
        
    # use backend api to create the booking instance
    success = create_booking(user_email, listing_title, 
                             start_date, end_date)

    if not success:
        error_message = "Booking Creation Failed."
    # if there is any error messages when booking listing
    # at the backend, go back to the booking page.
    if error_message:
        return render_template('create_booking.html', message=error_message)
    else:
        return render_template('create_booking.html', 
                               message="Booking Created.")