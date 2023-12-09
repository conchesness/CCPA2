from app import app
import mongoengine.errors
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from app.classes.data import require_role,Role,User
import datetime as dt

@app.route('/admintest')
@require_role('admin')
def admintest():
    return redirect('/')

@app.route('/listroles')
def listroles():
    roles = Role.objects()
    for role in roles:
        flash(role.name)
    return render_template('index.html')

# These are commented out because they should not be generally available. Uncomment them to run them once.

# @app.route('/makeroles')
# def makeroles():
#     studentRole = Role(name="student").save()
#     teacherRole = Role(name="teacher").save()
#     adminRole = Role(name="admin").save()
#     return render_template('index.html')

# @app.route('/makeadmin/<email>')
# def makeadmin(email):
#     adminRole = Role.objects.get(name='admin')
#     try:
#         newAdmin = User.objects.get(email=email)
#     except:
#         flash("That user doesn't exist")
#     else:
#         newAdmin.roles.append(adminRole)
#         newAdmin.save()
#         flash(f"{newAdmin.fname} {newAdmin.lname} is now admin.")
#     return redirect("/")