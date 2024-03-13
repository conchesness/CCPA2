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
from time import time
from bson.objectid import ObjectId
from flask_security import RoleMixin
from functools import wraps

class College (Document):
    unitid = IntField()
    coltype = StringField()
    name = StringField()
    street = StringField()
    city = StringField()
    state = StringField()
    zipcode = StringField()
    lat = FloatField()
    lon = FloatField()
    locale = StringField()

class CollegeEnrollment(Document):
    college = ReferenceField('College')
    student = ReferenceField('User')
    grad_year = IntField()

class Address(EmbeddedDocument):
    oid = ObjectIdField(default=ObjectId())
    createdate = DateTimeField(default=dt.datetime.utcnow())
    modifydate = DateTimeField(default=dt.datetime.utcnow())
    modifiedby = ReferenceField('User')
    name = StringField()
    streetAddress = StringField()
    city = StringField()
    state = StringField()
    zipcode = IntField()
    description = StringField()
    lat = FloatField()
    lon = FloatField()
    # College, Work, Home
    addresstype = StringField()
    iscurrent = BooleanField()
    gradyear = IntField()
    
    meta = {
        'ordering': ['-createdate']
    }

class User(UserMixin, Document):
    createdate = DateTimeField(default=dt.datetime.utcnow())
    gid = StringField(sparse=True, unique=True)
    aeriesid = IntField(sparse=True,unique=True)
    gname = StringField()
    gprofile_pic = StringField()
    username = StringField()
    fname = StringField()
    lname = StringField()
    email = EmailField(sparse=True,unique=True)
    image = FileField()
    prononuns = StringField()
    roles = ListField(ReferenceField("Role"))
    agender = StringField()
    afamkey = IntField()
    grade = IntField()

    tdivision = StringField()
    school = StringField()
    pronouns = StringField()

    addresses = (EmbeddedDocumentListField('Address'))
    
    # teacher only data
    teacher_number = IntField(sparse=True,unique=True)
    troom_number = StringField()
    tdescription = StringField()
    tdivision = StringField()
    tdepartment = StringField()
    troom_phone = IntField()

    # teacher Self-rating
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
    name = StringField(unique=True)

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
    sat = IntField()

class Project(Document):
    owner = ReferenceField('User')
    status = StringField(default='In Progress')
    createDateTime = DateTimeField(default=dt.datetime.utcnow())
    name = StringField()
    desc = StringField()
    product = StringField()
    obstacles = EmbeddedDocumentListField('Obstacle')
    milestones = EmbeddedDocumentListField('Milestone')

class ProjPost(Document):
    owner = ReferenceField('User')
    project = ReferenceField('Project')
    milestoneOID = StringField()
    createDateTime = DateTimeField(default=dt.datetime.utcnow())
    # intention, reflection
    post_type = StringField()
    # 1-3
    satisfaction = IntField()
    confidence = IntField()
    reflection = StringField()
    intention = StringField()
    image_reflection_src = StringField()

    meta = {
        'ordering': ['createDateTime']
    }


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

class Survey(Document):
    timestamp = StringField()
    email = StringField()
    grade = StringField()
    full_name = StringField()
    identity = StringField()
    identity_list = ListField(StringField())
    safety_narrative = StringField()
    adults_safety = StringField()
    adults_safety_list = ListField(StringField())
    race_narrative = StringField()
    adults_race = ListField(StringField())
    expert_narrative = StringField()
    adults_expert = ListField(StringField())
    events_narrative = StringField()
    ideas_narrative = StringField()
    other_narrative = StringField()

