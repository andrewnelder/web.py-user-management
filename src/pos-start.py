'''
This is the main routine of the web-app.  It is responsible for addressing,
session construction/storage, and basic page logic. 

Created on Nov 8, 2011
@author: andrewnelder
'''

import web
import database
import session_management
from logging import getLogger, basicConfig, DEBUG

LOGGER = getLogger(__name__)

web.config.debug = False                            # Required for sessions

urls = (
    '/',                    'index',
    '/user/login',          'login',
    '/user/logout',         'logout',
    '/user/create',         'create_user',
    '/user/delete',         'delete_user',
)
app     = web.application(urls, globals())
store   = web.session.DiskStore('sessions')
session = web.session.Session(app, store, initializer = \
                              {'login': 0, 'username': '', 'user_type': 0})

class index:
    
    def GET(self, name=''):
        render = get_render()
        return '%s'%render.index()

class create_user:

    def GET(self):
        '''
        Create User Form
        '''
        
        render = get_render()
        return '%s'%render.user.create()
    
    def POST(self):
        '''
        The login form targets itself.
        '''
        
        username = web.input().username
        password = web.input().password
        email    = web.input().email
        
        create_success = \
            database.create_user(username, password, email)

        # if successful then login_ok.html else login_error.html 
        render = get_render()
        if create_success:
            page = web.seeother('/user/login')
        else:
            page = '%s'%render.user.create_error()
        
        return page

class delete_user:
    
    def GET(self):
        '''
        Delete user form.
        '''
        render = get_render()
        return '%s'%render.user.delete()
    
    def POST(self):
        
        username = web.input().username
        password = web.input().password
        
        success = database.delete_user(username, password)
        
        if success:
            page = web.seeother('/user/logout')
        else:
            page = web.seeother('/user/delete')

class login:

    def GET(self):
        '''
        The login form.
        '''
        
        render = get_render()
        return '%s'%render.user.login()
    
    def POST(self):
        '''
        The login form targets itself.
        '''
        
        global session
        
        username = web.input().username
        password = web.input().password
        
        # determine if username and password are correct
        session_out = None
        user_type = database.attempt_login(username, password)
        if user_type:
            session_out = session_management.attempt_login(session, 
                                                           username, 
                                                           user_type)
        
        # if successful then login_ok.html else login_error.html 
        render = get_render()
        if session_out:
            session = session_out
            page = web.seeother('/')
        else:
            page = '%s'%render.user.login_error()
        
        return page

class logout:
    
    def GET(self):
        
        global session
        
        session = session_management.logout(session)
        
        return web.seeother('/')

def get_render(template='common'):
    render = web.template.render('templates/common', \
                                 globals={'context': session})
    if template is 'admin':
        render = web.template.render('templates/admin', globals={'context': session})
    return render

if __name__ == "__main__":
    basicConfig(level=DEBUG)
    database.setup_database()
    app.run()