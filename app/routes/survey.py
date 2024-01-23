# These routes are an example of how to use data, forms and routes to create
# a blog where a blogs and comments on those blogs can be
# Created, Read, Updated or Deleted (CRUD)

from app import app
import mongoengine.errors
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from app.classes.data import require_role, Survey
from flask_login import login_required
import datetime as dt
import pandas as pd

@app.route('/survey')
@login_required
@require_role(role="confidential")
def survey():
    return render_template('/survey/survey.html')

@app.route('/survey/qbyids/<iden>')
@login_required
@require_role(role="confidential")
def surveyQByIds(iden):
    entries=Survey.objects()
    elist = [['Email','Intersectionality','adults','Safety Narrative']]

    for e in entries:
        if iden in e.identity_list:
            elist.append([e.email,e.identity_list,e.adults_safety_list,e.safety_narrative])

    return render_template('survey/surveybyid.html',elist=elist,iden=iden)
    
@app.route('/survey/qbyadults/<adult>')
@login_required
@require_role(role="confidential")
def surveyQByAdults(adult):
    entries=Survey.objects()
    elist = [['Email','Other Adults','Intersectionality','Safety Narrative']]

    for e in entries:
        if adult in e.adults_safety_list:
            elist.append([e.email,e.adults_safety_list,e.identity_list,e.safety_narrative])

    return render_template('survey/surveybyadult.html',elist=elist,adult=adult)

@app.route('/survey/safety/adult/int')
@login_required
@require_role(role="confidential")
def surveyAdultInt():
    entries = Survey.objects()
    
    # Create a list of all adults
    adultsAll = []
    for e in entries:
        adultsAll = adultsAll + e.adults_safety_list

    adultsdd = set(adultsAll)
    adultsdd = list(adultsdd)

    adultsdd.sort()

    adults = {}
    for a in adultsdd:
        ids=[]
        for e in entries:
            if a in e.adults_safety_list:
                ids += e.identity_list
        ids = set(ids)
        ids = list(ids)
        adults[a] = ids

    adultsDicts=[]
    for a in adultsdd:
        x=[i for i in adultsAll if i==a] 
        adultsDicts.append([len(x),a])
    adultsDicts = sorted(adultsDicts, key=lambda x: x[0])
    adultsDicts.reverse()

    return render_template('survey/adults_ids.html',adults=adults, adultsDicts=adultsDicts)

@app.route('/survey/safety/int/adult')
@login_required
@require_role(role="confidential")
def surveyIntSafety():
    entries = Survey.objects()
    ids = []
    for e in entries:
        for i in e.identity_list:
            ids.append(i)

    idsdd = set(ids)
    idsdd = list(idsdd)
    idsdd.sort()
    
    idCounts=[]
    for id in idsdd:
        x=[i for i in ids if i==id] 

        idCounts.append([len(x),id])
    idCounts = sorted(idCounts, key=lambda x: x[0],reverse=True)



    idsDict={}
    for identity in idsdd:
        adults=[]
        for e in entries:
            if identity in e.identity_list:
                adults += e.adults_safety_list
        adults = set(adults)
        adults = list(adults)
        adults.sort()
        idsDict[identity] = adults


    return render_template('survey/intersectionality.html',ids=idCounts,idsDict=idsDict)


# @app.route('/identitytolist')
# @login_required
# @require_role(role="teacher")
# def identitytolist():
#     entries = Survey.objects()
#     for e in entries:
#         i_list = e.identity.split(',')
#         for i in i_list:
#             i = i.strip()
#             if not i in e.identity_list:
#                 e.identity_list.append(i)
#         e.save()
#     return render_template('index.html')


# @app.route('/import_survey')
# @login_required
# @require_role(role="teacher")
# def import_survey():
#     surveyDF = pd.read_csv('./app/static/survey.csv', quotechar='"')
#     surveyDict = surveyDF.to_dict('index')
#     num = len(surveyDict)
#     for i,row in enumerate(surveyDict):
#         row = surveyDict[row]
#         newEntry = Survey(
#             timestamp = str(row['timestamp']),
#             email = str(row['email']),
#             grade = str(row['grade']),
#             full_name = str(row['full_name']),
#             identity = str(row['identity']),
#             safety_narrative = str(row['safety_narrative']),
#             adults_safety = str(row['adults_safety']),
#             race_narrative = str(row['race_narrative']),
#             expert_narrative = str(row['expert_narrative']),
#             events_narrative = str(row['events_narrative']),
#             ideas_narrative = str(row['ideas_narrative']),
#             other_narrative = str(row['other_narrative'])
#         )
#         newEntry.save()
#         print(f"{i}/{num}")

#     return render_template('index.html')


# @app.route('/survey/adults_safety')
# @login_required
# @require_role(role="teacher")
# def adults_safety():
#     entries = Survey.objects()
#     adults=[]
#     adultsDicts=[]
#     for e in entries:
#         for a in e.adults_safety_list:
#             adults.append(a)
#     adultsdd = set(adults)
#     adultsdd = list(adultsdd)
#     for a in adultsdd:
#         x=[i for i in adults if i==a] 
#         adultsDicts.append([len(x),a])
#     adultsDicts = sorted(adultsDicts, key=lambda x: x[0])
#     adultsDicts.reverse()
#     return render_template('survey/surveyadults.html',adults=adultsDicts)


# @app.route('/listids')
# @login_required
# @require_role(role="teacher")
# def listids():
#     entries = Survey.objects()
#     ids=[]
#     for e in entries:
#         ids += e.identity_list

#     ids=set(ids)
#     ids=list(ids)
#     flash(ids)

#     return redirect(url_for('adults_safety'))

# @app.route('/afix')
# @login_required
# @require_role(role="teacher")
# def afix():
#     entries = Survey.objects()
#     ids=[]
#     for e in entries:
#         # idsdd = set(e.identity_list)
#         # e.identity_list = list(idsdd)
#         # e.save()
#         for n,i in enumerate(e.identity_list):
#             if 'mexicano/a' in i.lower():
#                 e.identity_list[n] = 'Mexicana(o)'
#                 flash(e.identity_list)
#                 e.save()

#     return redirect(url_for('listids'))

# @app.route('/wsstrip')
# @login_required
# @require_role(role="teacher")
# def wsstrip():
#     entries = Survey.objects()
#     save = False
#     for e in entries:
#         adults = []
#         for i,a in enumerate(e.adults_safety_list):
#             a = a.strip()
#             adults.append(a)
#         e.adults_safety_list = adults
#         e.save()
    
#     return redirect(url_for('adults_safety'))