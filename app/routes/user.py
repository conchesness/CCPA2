from app import app
from flask_login.utils import login_required
from flask_login import current_user
from flask import render_template, redirect, flash, url_for
from app.classes.data import User, require_role, Role
from app.classes.forms import ProfileForm
from flask_login import current_user
import requests
# from pandas import read_csv
import mongoengine.errors

# These routes and functions are for accessing and editing user profiles.

# The first line is what listens for the user to type 'myprofile'
@app.route('/myprofile')
# This line tells the user that they cannot access this without being loggedin
@login_required
# This is the function that is run when the route is triggered
def myProfile():
    # This sends the user to their profile page which renders the 'profilemy.html' template
    return render_template('profilemy.html')

# This is the route for editing a profile
# the methods part is required if you are using a form 
@app.route('/myprofile/edit', methods=['GET','POST'])
# This requires the user to be loggedin
@login_required
# This is the function that goes with the route
def profileEdit():
    # This gets an object that is an instance of the form class from the forms.pyin classes
    form = ProfileForm()
    # This asks if the form was valid when it was submitted
    if form.validate_on_submit():
        # if the form was valid then this gets an object that represents the currUser's data
        currUser = User.objects.get(id=current_user.id)
        # This updates the data on the user record that was collected from the form
        currUser.update(
            lname = form.lname.data,
            fname = form.fname.data,
        )
        # This updates the profile image
        if form.image.data:
            if currUser.image:
                currUser.image.delete()
            currUser.image.put(form.image.data, content_type = 'image/jpeg')
            # This saves all the updates
            currUser.save()
        # Then sends the user to their profle page
        return redirect(url_for('myProfile'))

    # If the form was not submitted this prepopulates a few fields
    # then sends the user to the page with the edit profile form
    form.fname.data = current_user.fname
    form.lname.data = current_user.lname

    return render_template('profileform.html', form=form)

# @app.route("/checknames")
# def checknames():
#     stusDF = read_csv('./app/static/names.csv', quotechar='"')
#     stusDict = stusDF.to_dict('index')
#     num = len(stusDict)
#     sheet = ''
#     stuRole = Role.objects.get(name='student')
#     for i,row in enumerate(stusDict):
#         row = stusDict[row]
#         stus = User.objects(grade=row['grade'],fname__iexact=row['fname'], roles__contains=stuRole)
#         try:
#             len(stus)
#         except:
#             pass
#         else:
#             if len(stus) > 1:
#                 print(f"{row['fname']} {row['lname1']} {row['lname2']} {row['lname3']}")
#                 for stu in stus:
#                     print(f"{row['timestamp']},{stu.email}")
#                 print()

#     print(f"total checked {i}")

#     return render_template('index.html')



# @app.route("/importusers")
# def importusers():
#     stusDF = read_csv('./app/static/allStudentsCCPA.csv', quotechar='"')
#     stusDict = stusDF.to_dict('index')
#     num = len(stusDict)
#     stuRole = Role.objects.get(name='student')
#     for i,row in enumerate(stusDict):
#         row = stusDict[row]
#         try:
#             stu = User.objects.get(email = row['oemail'])
#         except mongoengine.errors.DoesNotExist:
#             print(f"{row['oemail']} does not exist")
#             stu = User(
#                 email = row['oemail'],
#                 aeriesid = row['aeriesid'],
#                 fname = row['afname'],
#                 lname = row['alname'],
#                 agender = row['agender'],
#                 afamkey = row['afamkey'],
#                 grade = row['grade']
#             )
#             stu.save()
#         except mongoengine.errors.MultipleObjectsReturned:
#             print(f"{row['oemail']} has more than one entry.")
#         else:
#             #print(f"{row['oemail']} has been updated.")
#             # stu.update(
#             #     aeriesid = row['aeriesid'],
#             #     agender = row['agender'],
#             #     afamkey = row['afamkey'],
#             #     grade = row['grade']
#             # )
#             if not stuRole in stu.roles:
#                 stu.roles.append(stuRole)
#                 stu.save()
#                 print(f"{i}/{num}")

#     return render_template("index.html")