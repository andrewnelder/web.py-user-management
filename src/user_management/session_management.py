'''
The session_management module is responsible for managing a user's active
enrollment on the site.  If they are logged in or out, the session will reflect
their status.

TODO:
    - Session variables should hold time-stamps, so the user account may 
      timeout if left unattended for too long.
    - Convert the username parameter to a user-id, so the user's information
      can be accessed across multiple tables; should they exist.

Created on Nov 8, 2011
@author: andrewnelder
'''

from logging import getLogger
from util.config import USER_TYPES
from web.session import Session
import web

LOGGER = getLogger(__name__)
SESSION_EXPIRATION_TIME = 1*60*60

class UserSession(Session):
    
    def __init__(self, *args, **kwargs):
        web.config.session_parameters['timeout'] = SESSION_EXPIRATION_TIME
        super(UserSession, self).__init__(*args, **kwargs)
        
    def attempt_login(self, username, user_type):
        '''
        Attempts to build an active session for the user.  Someone else may choose
        to replace this with the unique id, so user information can be easily
        accessed later.  However, since this is merely a demo -- I would like to
        avoid the excess database query all together.
        
        @param session:
            The session variable.
        @type session:
            web.Session
        
        @param username:
            A username to store in the session variable.  
        @type username:
            String
        
        @param user_type:
            The user-type of the user attempting to login.
        @type user_type:
            Integer (util.config.USER_TYPES)
        
        @return:
            The updated user session.
        @rtype:
            web.Session
        '''

        if user_type in USER_TYPES.values():
            self.login = 1
            self.username = username
            self.user_type = user_type
    
    def logout(self):
        '''
        Logs a user account out, regardless of it's activity.
        
        @param session:
            The session variable.
        @type session:
            web.Session
        
        @return session:
            The updated user session.
        @rtype:
            web.Session
        '''
        
        self.login = 0
        self.username = ''
        self.user_type = 0
    
    def is_expired(self):
        '''
        Determines if the session has been expired.
        '''
        expired_status = False
        if self.session_id and self.session_id not in self.store:
            expired_status = True
        return expired_status
    
    def is_admin(self):
        '''
        Quick check to see if a user is an administrator.
        
        @param session:
            The session variable.
        @type session:
            web.Session
        '''
        
        return (USER_TYPES['admin'] == self.user_type)
    
    def is_logged(self):
        '''
        Quick check to see if the user is actively logged in.
        
        @param session:
            The session variable.
        @type session:
            web.Session
        '''
        
        return bool(self.login)