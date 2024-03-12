# This file is where data entry forms are created. Forms are placed on templates 
# and users fill them out.  Each form is an instance of a class. Forms are managed by the 
# Flask-WTForms library.

from flask_wtf import FlaskForm
import mongoengine.errors
from wtforms.validators import URL, Email, DataRequired, Optional, InputRequired
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, SelectField, FileField
from wtforms import BooleanField, URLField, ColorField, IntegerRangeField, DateTimeLocalField

class QRForm(FlaskForm):
    QRText = StringField()
    size = SelectField(choices=[(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10)])
    borderSize = SelectField(choices=[(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10)])
    colorDark = ColorField()
    colorLight = ColorField()
    colorDataDark = ColorField()
    colorDataLight = ColorField()
    submit = SubmitField("Enter")

class SpotifySearchForm(FlaskForm):
    track = StringField()
    artist = StringField()
    submit = SubmitField("Search")

class WCloudForm(FlaskForm):
    text = TextAreaField()
    stopwords = TextAreaField()
    submit = SubmitField('Submit')

class ProfileForm(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()]) 
    image = FileField("Image") 
    submit = SubmitField('Post')

class BlogForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    content = TextAreaField('Blog', validators=[DataRequired()])
    tag = StringField('Tag', validators=[DataRequired()])
    submit = SubmitField('Blog')

class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Comment')

class ClinicForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    streetAddress = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zipcode = StringField('Zipcode',validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

departments = [("",""),("Mathmatics","Mathmatics"),("Science", "Science"),("English", "English"),("Visual and Performing Arts", "Visual and Performing Arts"),("Humanities", "Humanities"),("PE", "Physical Education (PE)"), ("World Languages", "World Languages"), ("CompSci", "Computer Science"),("Other Elective","Other Elective")]

class CourseFilterForm(FlaskForm):
    department = SelectField('Department',choices = departments)
    name = StringField('Course Name')
    incomplete = BooleanField('Incomplete')
    submit = SubmitField("Search")

class ProfileForm(FlaskForm):
    pronouns = StringField('Pronouns')
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()]) 
    image = FileField("Image") 
    submit = SubmitField('Post')

onetoten = [(0,"---"),(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10)]
class TeacherForm(FlaskForm):
    pronouns = StringField('Pronouns')
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()]) 
    troom_number = StringField('Room Number')
    tdivision = SelectField('Division', choices=[("",""),('D1','D1'),("D2","D2"),("D3","D3")])
    tdescription = TextAreaField('Description')
    tdepartment = SelectField('Department',choices=departments)
    troom_phone = StringField('Phone Number', validators=[Optional()])
    image = FileField("Image") 
    late_work = IntegerRangeField('Late Work')
    late_work_policy = TextAreaField('Late Work Policy', render_kw={"placeholder": "Late Work Policy (optional)"})
    feedback = IntegerRangeField('Openness to Feedback')
    feedback_policy = TextAreaField('Feedback Policy')
    classcontrol = IntegerRangeField('Classroom Environment')
    classcontrol_policy = TextAreaField('Class Control Policy')
    grading_policy = TextAreaField('Grading Policy')
    classroom = TextAreaField('Tell us about your classroom.')
    submit = SubmitField('Submit')

class CoursesForm(FlaskForm):
    course_number = StringField('Course Number')
    course_title = StringField('Course Title')
    course_name = StringField('Course Name', validators=[DataRequired()])
    course_ag_requirement = SelectField('Courses A-G Requirement',choices=[("",""),("A-History","A-History"),("B-English", "B-English"), ("C-Mathematics","C-Mathematics"), ("D-Science","D-Science"), ("E-Language Other Than English","E-Language Other Than English"), ("F-Visual And Performing Arts","F-Visual And Performing Arts"), ("G-College-Preparatory Elective","G- College-Preparatory Elective")])
    course_difficulty = SelectField('Course Difficulty',choices=[("",""),("AP","Advanced Placement (AP)"),("HP", "Honors (HP)"),("CP","College Prep (CP)")])
    course_difficulty = SelectField('Course Difficulty',choices=[("",""),("AP","Advanced Placement (AP)"),("HP", "Honors (HP)"),("CP","College Prep (CP)")])
    course_department = SelectField('Course Department',choices=departments)
    course_gradelevel = SelectField('Grade Level', choices=[("",""),("9th","9th"),("10th","10th"),("11th","11th"),("12th","12th"),("Any","Any")])
    submit = SubmitField('Add Course')

class TeacherCourseForm(FlaskForm):
    teacher = SelectField('Teacher',choices=[],validate_choice=False)
    course = SelectField('Course',choices=[],validate_choice=False)
    course_description = TextAreaField('Course Description')
    course_link = URLField("Link to syllabus",validators=[(Optional()),URL()], render_kw={"placeholder": "https://..."})
    submit = SubmitField('Submit')

class StudentReviewForm(FlaskForm):
    year_taken = IntegerField("Year You Took the Course",validators=[(InputRequired())])
    late_work = IntegerRangeField("Late Work",validators=[(InputRequired())])
    feedback = IntegerRangeField("Feedback",validators=[(InputRequired())])
    classcontrol = IntegerRangeField("Class Control",validators=[(InputRequired())])
    grading_policy = IntegerRangeField("Grading Policy",validators=[(InputRequired())])
    classroom_environment = IntegerRangeField("Classroom Environment",validators=[(InputRequired())])
    submit = SubmitField('Submit')

class ProjectForm(FlaskForm):
    name = StringField('Name')
    #desc = TextAreaField('Description')
    product = TextAreaField('What do you think you will make?')
    status = SelectField('Status',choices=[('In Progress','In Progress'),('Done','Done')])
    submit = SubmitField('Enter')

class MilestoneForm(FlaskForm):
    status = SelectField('Status',choices=[('In Progress','In Progress'),('Done','Done'),('Delete','Delete')])
    name = StringField('Name')
    desc = TextAreaField('Description')
    submit = SubmitField('Save')

class ProjPostForm(FlaskForm):
    post_type = SelectField("Type", choices=[('','---'),('Intention','Intention'),('Reflection','Reflection')], validators=[DataRequired()])
    confidence = SelectField("Confidence",choices=[(0,'---'),(3,"Very"),(2,'Sorta'),(1,'Not')])
    satisfaction = SelectField("Satisfaction",choices=[(0,'---'),(3,"Very"),(2,'Sorta'),(1,'Not')])
    reflection = TextAreaField("Reflection")
    intention = TextAreaField("Intention")
    milestone = SelectField("Milestone",choices=[],validate_choice=False)
    image_reflection = FileField("Image")
    submit = SubmitField("Save")

class ObstacleForm(FlaskForm):
    name = StringField('Name')
    desc = TextAreaField('Why is this an obstacle?')
    submit = SubmitField('Save')

class TxtAreaForm(FlaskForm):
    ta = StringField()
    submit = SubmitField('Save')

class AddressForm(FlaskForm):
    name = StringField()
    streetAddress = StringField()
    city = StringField()
    state = StringField()
    zipcode = IntegerField()
    description = TextAreaField()
    addresstype = SelectField(choices=[('','---'),('Work','Work'),('Residence','Residence')])
    submit = SubmitField('Save')

class CollegeForm(FlaskForm):
    name = StringField("Name")
    gradyear = IntegerField("Graduation Year")
    submit = SubmitField("Save")