# These routes are an example of how to use data, forms and routes to create
# a blog where a blogs and comments on those blogs can be
# Created, Read, Updated or Deleted (CRUD)

from app import app
import mongoengine.errors
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from app.classes.data import require_role, Project, Milestone
from app.classes.forms import ProjectForm, MilestoneForm
from flask_login import login_required
import datetime as dt

@app.route('/project/list')
@login_required
def projectList():
    projects = Project.objects()
    return render_template('projects/project_list.html',projects=projects)

@app.route('/project/delete/<pid>')
@login_required
def projectDelete(pid):
    try:
        projDel = Project.objects.get(pk=pid)
    except mongoengine.errors.DoesNotExist:
        flash("That project doesn't exist")
        return render_template('index.html')

    if projDel.owner != current_user and not session['isadmin']:
        flash("You can't delete that project." )
        return render_template('index.html')
    
    if len(projDel.milestones) > 0:
        flash("You can't delete a project that has Milestones.")
        return redirect(url_for('project',pid=projDel.id))

    projDel.delete()
    flash('Project has been deleted')

    return redirect(url_for('projectList'))    

@app.route('/project/my')
@login_required
def projectMy():
    try:
        proj = Project.objects.get(owner=current_user)
    except mongoengine.errors.DoesNotExist:
        flash("You don't have a project yet. You should make one!")
        return render_template('index.html')
    except mongoengine.errors.MultipleObjectsReturned:
        flash('Hmmm, you have more than one project.  That should happen.')
        return redirect(url_for('projectList'))
    else:
        return redirect(url_for('project',pid=proj.id))

@app.route('/project/new', methods=['GET', 'POST'])
@login_required
def projectNew():
    form = ProjectForm()

    try:
        projMy = Project.objects.get(owner=current_user, status = "In Progress")
    except mongoengine.errors.DoesNotExist:
        pass
    else:
        flash('You have an active project.')
        return redirect(url_for('projectMy'))

    if form.validate_on_submit():

        newProj = Project(
            owner = current_user,
            name = form.name.data,
            status = form.status.data,
            #desc = form.desc.data,
            product = form.product.data,
            createDateTime = dt.datetime.utcnow()
        )

        newProj.save()

        return render_template('projects/project.html', proj=newProj)
    
    return render_template('projects/project_form.html', form=form)

@app.route('/project/edit/<pid>', methods=['GET', 'POST'])
@login_required
def projectEdit(pid):
    form = ProjectForm()
    try:
        projEdit = Project.objects.get(pk=pid)
    except mongoengine.errors.DoesNotExist:
        flash('That projject does not exist')
        return render_template('index.html')

    if form.validate_on_submit():

        projEdit.update(
            owner = current_user,
            name = form.name.data,
            status = form.status.data,
            #desc = form.desc.data,
            product = form.product.data,
            createDateTime = dt.datetime.utcnow()
        )

        return redirect(url_for('project',pid=pid))
    
    form.name.data = projEdit.name
    form.status.data = projEdit.status
    #form.desc.data = projEdit.desc
    form.product.process_data(projEdit.product)
    
    return render_template('projects/project_form.html', form=form)

@app.route('/project/<pid>', methods=['POST','GET'])
@login_required
def project(pid):

    try:
        proj = Project.objects.get(pk=pid)
    except mongoengine.errors.DoesNotExist:
        flash ("That project doesn't exist.")
        return render_template('index.html')

    form = MilestoneForm()

    try:
        proj = Project.objects.get(pk=pid)
    except mongoengine.errors.DoesNotExist:
        flash("That project doesn't exist")
        return redirect(url_for('project', pid=pid))
    
    if form.validate_on_submit():
        if len(proj.milestones) == 0 or proj.milestones[-1].status == "Done":
            num = len(proj.milestones)+1
            proj.milestones.create(
                number = num,
                name = form.name.data,
                desc = form.desc.data
            )
            
            proj.save()

        else:
            flash("You can't create a new milestone until the previous one is marked done.")
        
    return render_template('projects/project.html', proj=proj, form=form)

@app.route('/project/milestone/delete/<pid>/<mid>')
@login_required
def projectMsDel(pid,mid):

    proj = Project.objects.get(pk=pid)
    if proj.owner == current_user or session['isadmin']:
        if proj.milestones[-1].status == 'Delete':
            proj.milestones.filter(oid=mid).delete()
            proj.save()
        else:
            flash('you can only delete a milestone that has status marked as "Delete".')
    else:
        flash("You can't delete that milestone because you don't own.")
    
    return redirect(url_for('project',pid=pid))

@app.route('/project/milestone/edit/<pid>/<mid>', methods=['GET','POST'])
@login_required
def projectMsEdit(pid,mid):

    form = MilestoneForm()

    proj = Project.objects.get(pk=pid)

    ms = proj.milestones.get(oid=mid)

    if form.validate_on_submit():
        proj.milestones.filter(oid=mid).update(
            name = form.name.data,
            desc = form.desc.data,
            status = form.status.data
        )
        proj.save()

        return redirect(url_for('project', pid=pid))
    
    form.name.process_data(ms.name)
    form.desc.process_data(ms.desc)
    form.status.process_data(ms.status)

    return render_template('projects/project.html',proj=proj,form=form,edit=True)