# The libraries we'll need
import sys, cgi, redirect, session, MySQLdb
from common import *

# Get the session and check if logged in
sess = session.Session(expires=60*20, cookie_path='/')
#loggedIn = sess.data.get('loggedIn')
form = cgi.FieldStorage()
db = MySQLdb.connect("info20003db.eng.unimelb.edu.au", "info20003g29", "enigma29", "info20003g29", 3306)
c=db.cursor()
# ---------------------------------------------------------------------------------------------------------------------
username = form.getvalue("username")
query = "SELECT * FROM Player WHERE UserName=%s"
try:
    c.execute(query,(username,))
    rows = results_as_dicts(c)
    assert(len(rows) == 1)
    info = rows[0]
    query_success = True
except AssertionError, e:
    query_success = False
    message = """
    <p id='select_error' class='error'>
    An incorrect number of results ({}) were returned for the given username.
    </p>
    """.format(len(rows))
except Exception, e:
    query_success = False
    message = """
    <p id='select_error' class='error'>
    Database error : {}
    </p>
    """.format(repr(e))

if not query_success:
    body = message
else:
    body = """
    <table>
        <tr id='name'>
            <td>Name:</td>
            <td>{} (a.k.a {})</td>
        </tr>
        <tr id='role'>
            <td>Role:</td>
            <td>{}</td>
        </tr>
        <tr id='email'>
            <td>Email:</td>
            <td><a href='mailto:{}>
                {}
                </a>
            </td>
        </tr>
        <tr id='description'>
            <td colspan='2'>{}</td>
        </tr>
     </table>
     """.format(info["FirstName"]+' '+info["LastName"], info["UserName"], info["Role"],\
                info["Email"], info["Email"], info["ProfileDescription"])
    
# send session cookie
print "%s\nContent-Type: text/html\n" % (sess.cookie)

if not username:
    username = "None"

print make_head(title = "WWAG Player: "+username, css_file = "player_info.css")
print make_navbar()

if query_success:
    print body
else:
    print message

print end_html
