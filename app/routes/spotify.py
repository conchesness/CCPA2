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
import json
from PIL import Image
import io

@app.route('/spotify')
@login_required
def spotifyauth():
    secrets = getSecrets()

    auth_headers = {
        "client_id": secrets['SPOTIFY_CLIENT_ID'],
        "response_type": "code",
        "redirect_uri": f"{request.host_url}spotifycallback",
        "scope": "user-library-read, playlist-modify-private, playlist-modify-public, ugc-image-upload"
    }

    f"{request.host_url}spotifycallback"

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
        "redirect_uri": f"{request.host_url}spotifycallback"
    }

    r = requests.post("https://accounts.spotify.com/api/token", data=token_data, headers=token_headers)

    session['spotifytoken'] = r.json()["access_token"] 

    spotifyMe = requests.get(url="https://api.spotify.com/v1/me", headers={"Authorization": "Bearer " + session['spotifytoken']})

    session['spotifyid'] = spotifyMe.json()['id']

    return redirect(url_for('playlist'))


@app.route('/addselftotrack/<track_id>')
@login_required
def addselftotrack(track_id):

    track = Playlist.objects.get(pk=track_id)

    if current_user.id in track.users:
        flash("you are already on this track.")
        return redirect(url_for('playlist'))

    numCollabTracks = Playlist.objects(users__contains = current_user.id, num_users__gt=1)
    if len(numCollabTracks) >= 5:
        flash("You are on 5 collab tracks. Remove yourself from one if you want to add yourself to another.")
        return redirect(url_for('playlist'))

    track.users.append(current_user).save()

    return redirect(url_for('playlist'))


@app.route('/addtoplaylist/<spotifyid>')
@login_required
def addtoplaylist(spotifyid):

    numSoloTracks = Playlist.objects(users__contains = current_user.id, num_users=1)
    if len(numSoloTracks) >= 2:
        flash("You already have 2 tracks where you are the only user. Delete one or wait til some one votes one of them.")
        return redirect(url_for('playlist'))

    user_headers = {
        "Authorization": "Bearer " + session['spotifytoken'],
        "Content-Type": "application/json"
    }  

    track_info = requests.get(
        'https://api.spotify.com/v1/tracks/'+spotifyid,
        headers=user_headers,
        params = {
            'type':'track'
            }
        )
        
    if str(track_info) == "<Response [401]>":
        return redirect(url_for('spotifyauth'))

    track_info = track_info.json()

    newTrack = Playlist(
        track_id = spotifyid,
        track_dict = track_info,
        num_users = 1
    )
    newTrack.users.append(current_user.id)
    try:
        newTrack.save()
    except NotUniqueError:
        editTrack = Playlist.objects.get(track_id=spotifyid)
        if not current_user in editTrack.users:

            numCollabTracks = Playlist.objects(users__contains = current_user.id, num_users__gt=1)
            if len(numCollabTracks) >= 5:
                flash("You are on 5 collab tracks. Remove yourself from one if you want to add yourself to another.")
                return redirect(url_for('playlist'))

            flash('Adding you to a track already in the playlist.')
            editTrack.users.append(current_user.id)
            editTrack.users.num_users = len(editTrack.users)
            editTrack.save()
        else:
            flash("You are already on that track.")

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

@app.route('/updateplaylist')
def updatePLaylist():

    endpoint_url = f"https://api.spotify.com/v1/users/{session['spotifyid']}/playlists"

    offset=0
    limit=20
    allPlaylists = []
    while True:
        playlists = requests.get(
            url = endpoint_url + f'?offset={offset}&limit={limit}',
            headers={
                "Content-Type":"application/json", 
                "Authorization": "Bearer " + session['spotifytoken']
                }
            )
        playlists = playlists.json()
        try:
            allPlaylists += playlists['items']
        except:
            flash("Needed to refresh your credentials with Spotify.  Try again.")
            return redirect(url_for('spotifyauth'))
        if len(playlists['items']) < limit:
            break
        offset = offset + limit
    
    playlists = allPlaylists

    playlistExists = False
    for playlist in playlists:
        
        if playlist['name'] == 'CCPA Community Playlist':
            playlistExists = True
            playlistid = playlist['id']
            break

    
    request_body = json.dumps({
        "name": "CCPA Community Playlist",
        "description": "Playlist made by the CCPA Community",
        "public": True
    })

    if not playlistExists:
        response = requests.post(
            url = endpoint_url, 
            data = request_body, 
            headers={
                "Content-Type":"application/json", 
                "Authorization": "Bearer " + session['spotifytoken']
                }
            )
        try:
            playlistid = response.json()['id']
        except:
            flash('had to refresh your spotify credientials. Try again!')
            return redirect(url_for('spotify'))

        im = Image.open('app/static/lion.png')
        data = io.BytesIO()
        im.save(data, "jpeg")
        encoded_img_data = base64.b64encode(data.getvalue())

        response = requests.put(
            url = f'https://api.spotify.com/v1/playlists/{playlistid}/images',
            headers = {
                "Content-Type":"image/jpeg",
                "Authorization": "Bearer " + session['spotifytoken']
                },
            data = encoded_img_data
            )

    tracks = Playlist.objects()

    uris = []

    for track in tracks:
        uris.append(track.track_dict['uri'])

    response = requests.put(
        url = f"https://api.spotify.com/v1/playlists/{playlistid}/tracks",
        headers = {
            "Content-Type":"application/json",
            "Authorization": "Bearer " + session['spotifytoken']
            },
        data = json.dumps({
                "uris": uris
            })
        )

    flash("Check your Spotify for the CCPA Community Playlist!")

    return redirect(url_for('playlist'))
