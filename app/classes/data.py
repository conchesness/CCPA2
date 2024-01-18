# This is where all the database collections are defined. A collection is a place to hold a defined 
# set of data like Users, Blogs, Comments. Collections are defined below as classes. Each class name is 
# the name of the data collection and each item is a data 'field' that stores a piece of data.  Data 
# fields have types like IntField, StringField etc.  This uses the Mongoengine Python Library. When 
# you interact with the data you are creating an onject that is an instance of the class.

from sys import getprofile
from tokenize import String
from typing import KeysView
from xmlrpc.client import Boolean

from setuptools import SetuptoolsDeprecationWarning
from app import app
from flask import flash, redirect
from flask_login import UserMixin, current_user
from mongoengine import Document, ListField, FileField, EmailField, StringField, IntField, DictField, EmbeddedDocumentListField, EmbeddedDocument
from mongoengine import ReferenceField, DateTimeField, BooleanField, FloatField, ObjectIdField,CASCADE
import datetime as dt
#import jwt
from time import time
from bson.objectid import ObjectId
from flask_security import RoleMixin
from functools import wraps

class User(UserMixin, Document):
    createdate = DateTimeField(default=dt.datetime.utcnow())
    gid = StringField(sparse=True, unique=True)
    gname = StringField()
    gprofile_pic = StringField()
    username = StringField()
    fname = StringField()
    lname = StringField()
    email = EmailField()
    image = FileField()
    prononuns = StringField()
    roles = ListField(ReferenceField("Role"))

    tdivision = StringField()
    school = StringField()
    pronouns = StringField()
    
    # Below Is teacher only data
    teacher_number = IntField(sparse=True,unique=True)
    troom_number = StringField()
    tdescription = StringField()
    tdivision = StringField()
    tdepartment = StringField()
    troom_phone = IntField()

    # Self-rating
    late_work = IntField()
    late_work_policy = StringField()
    feedback = IntField()
    feedback_policy = StringField()
    classcontrol = IntField()
    classcontrol_policy = StringField()
    grading_policy = StringField()
    classroom = StringField()

    meta = {
        'ordering': ['lname','fname'],
        'strict':False
    }

    def has_role(self, name):
        """Does this user have this permission?"""
        try:
            chk_role = Role.objects.get(name=name)
        except:
            flash(f"{name} is not a valid role.")
            return False
        if chk_role in self.roles:
            return True
        else:
            flash(f"That page requires the {name} role.")
            return False

class Role(RoleMixin, Document):
    # The RoleMixin requires this field to be named "name"
    name = StringField()

# To require a role for a specific route use this decorator
# @require_role(role="student")

def require_role(role):
    """make sure user has this role"""
    def decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            if not current_user.has_role(role):
                return redirect("/")
            else:
                return func(*args, **kwargs)
        return wrapped_function
    return decorator

class Playlist(Document):
    track_id = StringField(unique = True)
    track_dict = DictField(required = True)
    users = ListField(ReferenceField("User"))
    num_users = IntField()

    meta = {
        'ordering': ['num_users']
    }

class Obstacle(EmbeddedDocument):
    obstacle = StringField()
    desc = StringField()

class Milestone(EmbeddedDocument):
    oid = ObjectIdField(default=ObjectId(), sparse=True, required=True, unique=True, primary_key=True)    
    status = StringField(default="In Progress")
    name = StringField()
    number = IntField()
    desc = StringField()
    reflection = StringField()

class Project(Document):
    owner = ReferenceField('User')
    status = StringField(default='In Progress')
    createDateTime = DateTimeField(default=dt.datetime.utcnow())
    name = StringField()
    desc = StringField()
    product = StringField()
    obstacles = EmbeddedDocumentListField('Obstacle')
    milestones = EmbeddedDocumentListField('Milestone')

class Blog(Document):
    author = ReferenceField('User',reverse_delete_rule=CASCADE) 
    subject = StringField()
    content = StringField()
    tag = StringField()
    create_date = DateTimeField(default=dt.datetime.utcnow())
    modify_date = DateTimeField()

    meta = {
        'ordering': ['-createdate']
    }

class Comment(Document):
    # Line 63 is a way to access all the information in Course and Teacher w/o storing it in this class
    author = ReferenceField('User',reverse_delete_rule=CASCADE) 
    blog = ReferenceField('Blog',reverse_delete_rule=CASCADE)
    # This could be used to allow comments on comments
    comment = ReferenceField('Comment',reverse_delete_rule=CASCADE)
    # Line 68 is where you store all the info you need but won't find in the Course and Teacher Object
    content = StringField()
    create_date = DateTimeField(default=dt.datetime.utcnow())
    modify_date = DateTimeField()

    meta = {
        'ordering': ['-createdate']
    }

class Clinic(Document):
    author = ReferenceField('User',reverse_delete_rule=CASCADE) 
    createdate = DateTimeField(default=dt.datetime.utcnow())
    modifydate = DateTimeField()
    name = StringField()
    streetAddress = StringField()
    city = StringField()
    state = StringField()
    zipcode = StringField()
    description = StringField()
    lat = FloatField()
    lon = FloatField()
    
    meta = {
        'ordering': ['-createdate']
    }

# _____________________ iRate

class Courses(Document): 
    course_number = StringField(required=True,unique=True)
    course_title = StringField()
    course_name = StringField()
    course_ag_requirement = StringField()
    course_difficulty = StringField()
    course_department = StringField()
    course_pathway = StringField()
    course_gradelevel = StringField()
    create_date = DateTimeField(default=dt.datetime.utcnow())
    modify_date = DateTimeField()

    meta = {
        'ordering': ['-createdate'],
        'indexes':
            [
                {
                    'fields': ['course_name','course_title'],
                    'collation' : {'locale': 'en', 'strength': 2} 
                }   
            ]
        }

class TeacherCourse(Document):
    teachercourseid = StringField(sparse=True, required=True,unique=True)
    teacher = ReferenceField('User',reverse_delete_rule=CASCADE, required=True) 
    course = ReferenceField('Courses',reverse_delete_rule=CASCADE,required=True)
    course_description = StringField()
    course_files = FileField()
    course_link = StringField()
    create_date = DateTimeField(default=dt.datetime.utcnow())
    modify_date = DateTimeField()

    meta = {
        'ordering': ['-createdate']
    }

class StudentReview(Document):
    teacher_course = ReferenceField('TeacherCourse')
    student = ReferenceField('User')
    year_taken = IntField()
    late_work = IntField()
    feedback = IntField()
    classcontrol = IntField()
    grading_policy = IntField()
    classroom_environment = IntField()
    create_date = DateTimeField(default=dt.datetime.utcnow())
    modify_date = DateTimeField()

class Comment(Document):
    author = ReferenceField('User',reverse_delete_rule=CASCADE) 
    course = ReferenceField('Courses',reverse_delete_rule=CASCADE)
    content = StringField()
    create_date = DateTimeField(default=dt.datetime.utcnow())
    modify_date = DateTimeField()
    role = StringField("Role")

    meta = {
        'ordering': ['-createdate']
    }