<h1>Web.py User Management System</h1>

Soooooo, this whole idea erupted when I realized that I love web.py, but have no good way of managing user accounts.  Granted,
I've never made a user-management system before, so this probably isn't gold.  However, it's also probably not the
worst thing out there (of that I can guarantee).

<h3>Requirements</h3>
- [web.py](http://www.webpy.org/) - A very lightweight hosting platform for Python.
- [Python 2.6/2.7](http://www.python.org/) - The python programming language interpreter.

<h3>Questions you probably have...</h3>

<h4>What the hell can it do?</h4>

Not a whole lot.  It gives a basic outline of how to add/delete/login/logout (of) user accounts.  The demo is written
for SQLite; but it's simply a matter of rewriting the table creation code to get it to function with any other
SQL driven database system supported by the web.db module.

<h4>Do you feel dirty for doing this?</h4>

A little, yes.

<h4>How secure is this?</h4>

To be completely honest, I'm not really sure.  The passwords are salted and are hashed using SHA256 (which sounds
secure enough, imho).  Though -- I'd probably investigate a bit further before deploying this and accepting 
credit-cards or something equally stupid.  As one of the motivating factors for me was to add user-management to 
an in-house intranet, *I make no guarantees of this products security*.

<h4>Can I help "fix" this code?  It makes me sad.</h4>

Please do!  Just keep your code tidy and documented.

//list