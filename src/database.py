'''
The database management module maintains records contained in the database.
Depending on how large or complex a database becomes, this may be divided up
into sub-modules arranged by table.

TODO:
    - Instead of returning simply booleans, return messages that indicate
      how or why something failed/succeeded.
    - Add handlers for different database types (SQLite, MySQL, etc.)
        - Can SQLAlchemy be used for this task?  Is it thread-safe?
    - Sanitize strings better.

Created on Nov 8, 2011
@author: andrewnelder
'''

from logging import getLogger
from util.config import USER_TYPES
from util.general import sanitize, hash
import web

LOGGER = getLogger(__name__)

DATABASE_LOCATION = './'

db = web.database(dbn='sqlite', db='./data/data.db')

def setup_database():
    '''
    This collection of queries is responsible for constructing the tables
    that are required to store user credentials and other important information.
    
    @note: This should only be run once.
    '''
    
    user_table_query = \
        '''
        CREATE TABLE IF NOT EXISTS users ( id INTEGER PRIMARY KEY,
                                           user TEXT UNIQUE NOT NULL,
                                           pass TEXT NOT NULL,
                                           email TEXT UNIQUE NOT NULL,
                                           user_type INTEGER NOT NULL );
        '''
    db.query(user_table_query)

def delete_user(username, password='', user_type=USER_TYPES['user']):
    '''
    Called when attempting to remove a user account from the record.  For
    security and common-sense purposes; the password must also be provided.
    
    @param username:
        The username to be deleted from the records.
    @type username:
        String
    
    @param password:
        The password of the account to be deleted from the records.  This param
        is not required by administrators.  [Default == '']
    @type password:
        String
    
    @param user_type:
        The type of user making the request.  See config.USER_TYPES for more
        details.
    @type user_type:
        Integer (util.config.USER_TYPES)
    
    @return:
        The success/failure notification of the process.
    @rtype:
        Boolean
    '''
    
    username = sanitize(username)
    
    delete_user_query = \
        '''
        DELETE FROM users WHERE user = "%s";
        '''
    
    delete_success = False
    
    # If the requester is an admin or the correct user/pass is provided,
    # proceed with deleting the account.
    if (user_type is USER_TYPES['admin']) or attempt_login(username, password):
        db.query(delete_user_query%username)
        delete_success = True
    
    return delete_success

def create_user(username, password, email, user_type = USER_TYPES['user']):
    '''
    Called when a request is made to create a new user account.
    
    @param username:
        The username to associate with the new account.
    @type username:
        String
    
    @param password:
        The password to associate with the new account.
    @type password:
        String
    
    @param email:
        The email account to associate with the new account.
    @type email:
        String
    
    @param user_type:
        The user-type of the new account (admin, regular user, etc.).
        [Default == regular user]
    @type user_type:
        Integer (util.config.USER_TYPES)
    '''
    
    username = sanitize(username)
    password = hash(password)
    
    if 'admin' in username:
        user_type = USER_TYPES['admin']
    
    # TODO: Validate the email address -- util.general.validate_email()
    
    add_user_query = \
        '''
        INSERT OR IGNORE INTO users (user, pass, email, user_type) 
            VALUES ("%s", "%s", "%s", %d);
        '''
    db.query(add_user_query % (username, password, email, user_type,))
    
    return True

def attempt_login(username, password):
    '''
    Called when a user has attempted a username and password combination.  If
    the user is successfully logged in, this will return a valid user-type; 
    otherwise, it will return 0.
    
    @param username:
        The username being attempted.
    @type username:
        String
    
    @param password:
        The password that is associated with the aforementioned username.
    @type password:
        String
    
    @return:
        The user-type if the login succeeds; otherwise, returns 0.
    @rtype:
        Integer (util.config.USER_TYPES)
    '''
    
    username = sanitize(username)
    password = hash(password)
    
    find_user_query = \
        '''
        SELECT * FROM users WHERE user = "%s" AND pass = "%s";
        '''
    records = db.query(find_user_query % (username, password,))
    
    try:
        user = records[0]
        user_type = user['user_type']
    except IndexError:
        LOGGER.warning('Invalid user/pass for user <%s>.' % username)
        user_type = 0
    
    return user_type