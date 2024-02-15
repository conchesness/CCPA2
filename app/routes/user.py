from app import app
from flask_login.utils import login_required
from flask_login import current_user
from flask import render_template, redirect, flash, url_for
from app.classes.data import User, require_role, Role, CollegeEnrollment
from app.classes.forms import ProfileForm
from flask_login import current_user
import requests
# from pandas import read_csv
import mongoengine.errors

@app.route('/findstudent', methods=["GET","POST"])
@login_required
@require_role(role="teacher")
def findstudent():
    current_user
    pass

@app.route('/allstudents')
@login_required
@require_role(role="teacher")
def allstudents():
    studentObj = Role.objects.get(name="student")
    students=User.objects(roles__contains = studentObj)
    return render_template("students.html",students=students)

@app.route('/profile')
@app.route('/profile/<uid>')
@login_required
def profile(uid=None):
    adminObj = Role.objects.get(name="admin")
    if uid and adminObj in current_user.roles:
        try:
            user = User.objects.get(pk=uid)
        except mongoengine.errors.DoesNotExist:
            flash("That user doesn't exist.")
            return render_template("index.html")
    elif uid:
        flash("You can only edit your own profile.")
        return render_template("index.html")
    else:
        user = current_user
    colleges = CollegeEnrollment.objects(student=user)
    return render_template("profile.html",user=user,colleges=colleges)


@app.route('/profile/edit',methods=['GET','POST'])
@app.route('/profile/edit/<uid>', methods=['GET','POST'])
@login_required
def profileEdit(uid=None):
    adminObj = Role.objects.get(name="admin")
    form = ProfileForm()
    if uid and adminObj in current_user.roles:
        try:
            user = User.objects.get(pk=uid)
        except mongoengine.errors.DoesNotExist:
            flash("That user account doesn't exist")
            return redirect.url_for("index")
    elif uid:
        flash("You can't edit that user's profile.")
        return redirect.url_for("index")
    else:
        user = current_user
    if form.validate_on_submit():
        user.update(
            lname = form.lname.data,
            fname = form.fname.data,
        )
        if form.image.data:
            if user.image:
                user.image.delete()
            user.image.put(form.image.data, content_type = 'image/jpeg')

            user.save()
        return redirect(url_for('profile'))

    form.fname.data = user.fname
    form.lname.data = user.lname

    return render_template('profileform.html', form=form, user=user)

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