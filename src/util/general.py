'''
Created on Nov 11, 2011
@author: andrewnelder
'''
from util.config import SALT
import hashlib

def hash(input_string):
    '''
    Encrypts a string (by adding salt and hashing it) so it is no longer human
    readable.
    
    @param input_string:
        The string to encrypt.
    @type input_string:
        String
    
    @return:
        The encrypted version of the input (currently SHA256).
    @rtype:
        String
    
    @see: Salting Passwords - http://bit.ly/bebHPm
    '''
    
    input_length    = len(input_string)
    salt_length     = len(SALT)
    
    salted_string = "%s%s%s"%(SALT[:(input_length%salt_length)],
                              input_string,
                              SALT[((input_length+1)%salt_length):])
    
    return hashlib.sha256(salted_string).hexdigest()

def sanitize(input_string):
    '''
    Sanitizes a string so it cannot contaminate the database.
    
    @todo:
        Compare strings after the sanitization process to prior; if they don't
        match -- throw an error.
    
    @param input_string:
        The string that requires sanitization (typically usernames).
    @type input_string:
        String
    
    @return:
        The sanitized string.
    @rtype:
        String
    '''
    
    return str(input_string).strip().lower()

def validate_email(email_address):
    '''
    TODO: Write this function.
    '''
    pass