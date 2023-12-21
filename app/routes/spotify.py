from app import app
from flask import redirect, render_template, request, flash, session, url_for
from flask_login import current_user, login_required
import requests
from urllib.parse import urlencode
import base64
import webbrowser
from app.utils.secrets import getSecrets
from app.classes.forms import SpotifySearchForm
from app.classes.data import Playlist
from mongoengine.errors import NotUniqueError

def spotify_redir_uri():
    if request.host_url == 'https://127.0.0.1:5000/':
        flash('local')
        return "https://127.0.0.1:5000/spotifycallback"
    elif request.host_url == "https://ccpa-2.vercel.app/":
        return "https://ccpa-2.vercel.app/spotifycallback"

@app.route('/spotify')

@login_required
def spotifyauth():
    secrets = getSecrets()

    auth_headers = {
        "client_id": secrets['SPOTIFY_CLIENT_ID'],
        "response_type": "code",
        "redirect_uri": spotify_redir_uri(),
        "scope": "user-library-read"
    }

    return redirect("https://accounts.spotify.com/authorize?" + urlencode(auth_headers))

@app.route('/spotifycallback')
@login_required
def spotifycallback():
    secrets = getSecrets()
    code=request.args['code']
    encoded_credentials = base64.b64encode(secrets['SPOTIFY_CLIENT_ID'].encode() + b':' + secrets['SPOTIFY_CLIENT_SECRET'].encode()).decode("utf-8")

    token_headers = {
        "Authorization": "Basic " + encoded_credentials,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": spotify_redir_uri()
    }

    r = requests.post("https://accounts.spotify.com/api/token", data=token_data, headers=token_headers)

    session['spotifytoken'] = r.json()["access_token"]

    return redirect(url_for('playlist'))

@app.route('/addtoplaylist/<id>')
@login_required
def addtoplaylist(id):

    numSoloTracks = Playlist.objects(users__contains = current_user.id, num_users=1)
    if len(numSoloTracks) >= 2:
        flash("You already have 2 tracks where you are the only user. Delete one or wait til some one votes one of them.")
        return redirect(url_for('playlist'))

    user_headers = {
        "Authorization": "Bearer " + session['spotifytoken'],
        "Content-Type": "application/json"
    }  

    track_info = requests.get(
        'https://api.spotify.com/v1/tracks/'+id,
        headers=user_headers,
        params = {
            'type':'track'
            }
        )
        
    if str(track_info) == "<Response [401]>":
        return redirect(url_for('spotifyauth'))

    track_info = track_info.json()

    newTrack = Playlist(
        track_id = id,
        track_dict = track_info,
        num_users = 1
    )
    newTrack.users.append(current_user.id)
    try:
        newTrack.save()
    except NotUniqueError:
        editTrack = Playlist.objects.get(track_id=id)
        if not current_user in editTrack.users:
            flash('Adding you to a track already in the playlist.')
            editTrack.users.append(current_user.id)
            editTrack.users.num_users = len(editTrack.users)
            editTrack.save()
        else:
            flash("You already added that track to the list")

    return redirect(url_for('playlist'))

@app.route('/unvotetrack/<track_id>')
@login_required
def unvotetrack(track_id):
    editTrack = Playlist.objects.get(track_id = track_id)
    for i,user in enumerate(editTrack.users):
        if current_user == user:
            editTrack.users.pop(i)
            editTrack.save()
            editTrack.reload()
            editTrack.update(num_users = len(editTrack.users))
            flash("You unvoted that track.")
            if len(editTrack.users) == 0:
                editTrack.delete()
                flash("You were only user so the track is deleted.")
            break
    
    return redirect(url_for('playlist'))

@app.route('/playlist', methods=['GET','POST'])
@login_required
def playlist():  

    form = SpotifySearchForm()

    playlist = Playlist.objects()

    if form.validate_on_submit():

        track = form.track.data

        try:
            session['spotifytoken']
        except:
            return redirect(url_for('spotifyauth'))

        user_headers = {
            "Authorization": "Bearer " + session['spotifytoken'],
            "Content-Type": "application/json"
        }  

        track_info = requests.get(
            'https://api.spotify.com/v1/search',
            headers=user_headers,
            params={ 'q': track, 'type': 'track'}
            )

        if str(track_info) == "<Response [401]>":
            return redirect(url_for('spotifyauth'))

        track_info = track_info.json()

        return render_template('spotify.html', track_info = track_info, form=form, playlist=playlist)

    return render_template('spotify.html', form=form, playlist=playlist)

    