'''
Created on Nov 8, 2011
@author: andrewnelder
'''

import web
import hashlib
from logging import getLogger

LOGGER = getLogger(__name__)

DATABASE_LOCATION = './'

db = web.database(dbn='sqlite', db='./data/data.db')

def __hash(input_string):
    return hashlib.sha256(input_string).hexdigest()

def __sanitize(input_string):
    return str(input_string).strip().lower()

def setup_database():
    user_table_query = \
        '''
        CREATE TABLE IF NOT EXISTS users ( id INTEGER PRIMARY KEY,
                                           user TEXT UNIQUE NOT NULL,
                                           pass TEXT NOT NULL,
                                           email TEXT UNIQUE NOT NULL,
                                           user_type INTEGER NOT NULL );
        '''
    db.query(user_table_query)

def create_user(username, password, email, user_type=1):
    
    username = __sanitize(username)
    password = __hash(password)
    
    if 'admin' in username:
        user_type = 2
    
    add_user_query = \
        '''
        INSERT OR IGNORE INTO users (user, pass, email, user_type) 
            VALUES ("%s", "%s", "%s", %d);
        '''
    db.query(add_user_query%(username, password, email, user_type,))
    
    return True

def attempt_login(username, password):
    
    username = __sanitize(username)
    password = __hash(password)
    
    find_user_query = \
        '''
        SELECT * FROM users WHERE user = "%s" AND pass = "%s";
        '''
    records = db.query(find_user_query%(username, password,))
    
    try:
        user = records[0]
        user_type = user['user_type']
    except KeyError:
        user_type = 0
    
    return user_type