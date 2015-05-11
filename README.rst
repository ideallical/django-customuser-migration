Migrate Django 1.8 User to CustomUser with email (MySQL)
========================================================

I created this repository because I found it difficult to switch from a standard
Django User to a custom Django User. Especially when you're already using the
Django User heavily in other models.
This project is an example on how to do that with some handy migrations.

Bonus, you get a full working accounts app, with login, logout, password reset,
password forget, profile in Twitter bootstrap3 style. And a fully working admin.
Also, user now logs in with email instead of username. (Username is removed).

Just make sure you test this first locally and make a backup of your database (!)
The second migration uses raw SQL designed for MySQL. I haven't tested this for
other databases but I assume you can easily adjust that.


1. Install Python packages
--------------------------

::

    $ pip install -r requirements.txt



2. Change Django project settings
---------------------------------

::

    AUTH_USER_MODEL = 'accounts.User'
    LOGIN_URL = '/login/'
    LOGIN_REDIRECT_URL = '/profile/'
    DEFAULT_FROM_EMAIL = 'noreply@example.com'
    ACCOUNTS_REGISTRATION_OPEN = True
    ACCOUNT_ACTIVATION_DAYS = 7


    INSTALLED_APPS = (
        '...'
        'bootstrap3',
        'project',
        'accounts',
        '...',
    )

    $ python manage.py migrate accounts 0001 --fake  # this is your current Django User model
    $ python manage.py migrate accounts 0002  # change tablename auth_user to accounts_user etc.
    $ python manage.py migrate accounts 0003  # make email unique, and remove username field
    $ python manage.py migrate accounts 0004  # make registration possible


3. Copy the accounts and project folder to your Django project root
-------------------------------------------------------------------

4. Cleanup
----------
Now once you have done this in every environment.
Remove the migrations folder in accounts, and create a new initial migration:

::

    $ python manage.py makemigrations accounts


Then remove all the migrations from the databases in your env like so:

::

    DELETE FROM django_migrations WHERE app = 'accounts' AND name != '0001_initial';


There you go, you have a fresh start!
