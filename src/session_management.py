'''
Created on Nov 8, 2011
@author: andrewnelder
'''

from logging import getLogger

LOGGER = getLogger(__name__)

USER_TYPES = {'user': 1, 'admin': 2}

def attempt_login(session, username, user_type):

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
    session.login = 0
    session.username = ''
    session.user_type = 0
    return session

def is_admin(session):
    return (USER_TYPES['admin'] == session.user_type)

def is_logged(session):
    return bool(session.login)