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

LOGGER = getLogger(__name__)

def attempt_login(session, username, user_type):
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

    session_out = None    
    if user_type in USER_TYPES.values():
        session.login = 1
        session.username = username
        session.user_type = user_type
        session_out = session
    
    if session_out:
        LOGGER.info('Session built successfully.')
    else:
        LOGGER.warning('Session failed to build for type <%s>.'%str(user_type))
    
    return session_out

def logout(session):
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
    
    session.login = 0
    session.username = ''
    session.user_type = 0
    return session

def is_admin(session):
    '''
    Quick check to see if a user is an administrator.
    
    @param session:
        The session variable.
    @type session:
        web.Session
    '''
    
    return (USER_TYPES['admin'] == session.user_type)

def is_logged(session):
    '''
    Quick check to see if the user is actively logged in.
    
    @param session:
        The session variable.
    @type session:
        web.Session
    '''
    
    return bool(session.login)