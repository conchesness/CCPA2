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


@app.route('/setroles')
@require_role('admin')
def setroles():
    users = User.objects()
    return render_template('user-roles.html',users=users)


@app.route('/addrole/<roleName>')
@login_required
@require_role(role='admin')
def addrole(roleName):
    role(
        name=rolename
    ).save()
    flash (f"{roleName} role created.")
    roles = Role.objects()
    roleNames=[]
    for role in roles:
        roleNames.append(role.name)
    flash(f"Roles are: {roleNames}")
    return redirect('/')


@app.route('/makeadmin/<email>')
@login_required
@require_role(role='admin')
def makeadmin(email):
    adminRole = Role.objects.get(name='admin')
    try:
        newAdmin = User.objects.get(email=email)
    except:
        flash("That user doesn't exist")
    else:
        newAdmin.roles.append(adminRole)
        newAdmin.save()
        flash(f"{newAdmin.fname} {newAdmin.lname} is now admin.")
    return redirect("/")

@app.route('/removerolefrom/<email>/<roleName>')
@login_required
@require_role(role='admin')
def removeRoleFrom(email,roleName):
 
    try:
        user = User.objects.get(email=email)
    except mongoengine.errors.DoesNotExist:
        flash(f'User with email {email} does not exist.')
        return redirect('/')

    try:
        role = Role.objects.get(name=roleName)
    except mongoengine.errors.DoesNotExist:
        flash(f'User role "{roleName}" does not exist')
        return redirect('/')

    for i,role in enumerate(user.roles):
        if role.name == roleName:
            user.roles.pop(i)
            user.save()
            flash(f'Role, {roleName}, has been removed from {user.fname} {user.lname}.')

    flash(f"{user.fname} {user.lname}'s roles are...")
    for role in user.roles:
        flash(role.name)

    return redirect('/')
    
@app.route('/addroleto/<email>/<roleName>')
@login_required
@require_role(role='admin')
def addRoleTo(email,roleName):

 
    try:
        user = User.objects.get(email=email)
    except mongoengine.errors.DoesNotExist:
        flash(f'User with email {email} does not exist.')
        return redirect('/')

    try:
        roleObjToAdd = Role.objects.get(name=roleName)
    except mongoengine.errors.DoesNotExist:
        flash(f'User role "{roleName}" does not exist')
        return redirect('/')

    roleExists = False
    for i,roleObj in enumerate(user.roles):
        if roleObj.name == roleName:
            roleExists = True
    if not roleExists:
        user.roles.append(roleObjToAdd)
        user.save()
        flash(f'Role, {roleObjToAdd.name}, has been added to {user.fname} {user.lname}.')

    roles=[]
    for role in user.roles:
        roles.append(role.name)

    flash(f"{user.fname} {user.lname}'s roles are {roles}")

    return redirect('/')

@app.route('/makeconfidential/<email>')
@login_required
@require_role(role='admin')
def makeconfidential(email):
    confidentialRole = Role.objects.get(name='confidential')
    try:
        newConf = User.objects.get(email=email)
    except:
        flash("That user doesn't exist")
    else:
        newConf.roles.append(confidentialRole)
        newConf.save()
        flash(f"{newConf.fname} {newConf.lname} is now confidential.")
    return redirect("/")