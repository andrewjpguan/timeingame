"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, redirect, Blueprint, session
from flask_oauthlib.client import OAuth
from requests_oauthlib import OAuth2Session
from api.models import db, User
from api.utils import generate_sitemap, APIException
from api.steamHours import steamHours
from json import dumps
from urllib.parse import urlencode

api = Blueprint('api', __name__)

#set up OAuth2.0
oauth = OAuth()
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

#steam OpenID setup
steamOpenidUrl = 'https://steamcommunity.com/openid/login'
steamOpenidNs = 'http://specs.openid.net/auth/2.0'
steamOpenidIdentity= 'http://specs.openid.net/auth/2.0/identifier_select' #wtf is this
steamOpenidClaimedId= 'http://specs.openid.net/auth/2.0/identifier_select'
steamOpenidReturn = 'http://localhost:3001/api/steamAuthorization'
steamOpenidRealm = 'http://localhost:3001'

#blizzard OAuth setup
blizzardClientId = os.getenv("BLIZZARD_CLIENT_ID")
blizzardClientSecret = os.getenv("BLIZZARD_CLIENT_SECRET")
blizzardRedirectUri='http://localhost:3001/api/blizzardAuthorization'
blizzardScope = ['wow.profile', 'sc2.profile', 'd3.profile']
blizzardTokenUrl = 'https://oauth.battle.net/token'
blizzardAuthorizeUrl = 'https://oauth.battle.net/authorize'

#epic OAuth setup
epicClientId = os.getenv("EPIC_CLIENT_ID")
epicClientSecret = os.getenv("EPIC_CLIENT_SECRET")
epicRedirectUri='http://localhost:3001/api/epicAuthorization'
epicScope = ['basic_profile']
epicTokenUrl = 'https://api.epicgames.dev/epic/oauth/v1/token'
epicAuthorizeUrl = 'https://www.epicgames.com/id/authorize'


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route('/profile', methods=['GET'])
def profile():

    response_body = {

        "message": 'WIP'
    }

    return jsonify(response_body), 200

@api.route("/steamLogin")
def steamLogin():

    params = {
    'openid.ns': steamOpenidNs,
    'openid.identity': steamOpenidIdentity,
    'openid.claimed_id': steamOpenidClaimedId, #steamid
    'openid.mode': 'checkid_setup',
    'openid.return_to': steamOpenidReturn,
    'openid.realm': steamOpenidRealm
    }

    query_string = urlencode(params)
    login_url = steamOpenidUrl + "?" + query_string
    return '<a href="' + login_url + '">Login with steam</a>'

@api.route("/steamAuthorization")
def steamAuthorization():
    steamid = request.args['openid.claimed_id'].split('/')[5]
    session['steamid'] = steamid
    return steamHours(steamid)

@api.route('/blizzardLogin')
def blizzardLogin():
    oauth = OAuth2Session(blizzardClientId, redirect_uri=blizzardRedirectUri, scope=blizzardScope)
    login_url, state = oauth.authorization_url(blizzardAuthorizeUrl)
    session['blizzardState'] = state
    print("Login url: %s" % login_url)
    return '<a href="' + login_url + '">Login with Blizzard</a>'

@api.route('/blizzardAuthorization')
def blizzardAuthorization():
    blizzard = OAuth2Session(blizzardClientId, redirect_uri=blizzardRedirectUri, state=session['blizzardState'], scope=blizzardScope)
    token = blizzard.fetch_token(
        blizzardTokenUrl,
        client_secret=blizzardClientSecret,
        scope=blizzardScope,
        authorization_response=request.url,
        code=request.url.split('code=')[1].split('&')[0]
    )
    session['blizzardToken'] = token
    print(token)
    return 'Thanks for granting us authorization. We are logging you in! You can now visit <a href="/api/profile">/api/profile</a>'

@api.route('/epicLogin')
def epicLogin():
    oauth = OAuth2Session(epicClientId, redirect_uri=epicRedirectUri, scope=epicScope)
    login_url, state = oauth.authorization_url(epicAuthorizeUrl)
    session['epicState'] = state
    print("Login url: %s" % login_url)
    return '<a href="' + login_url + '">Login with Epic</a>'

@api.route('/epicAuthorization')
def epicAuthorization():
    epic = OAuth2Session(epicClientId, redirect_uri=epicRedirectUri, state=session['epicState'], scope=epicScope)

    token = epic.fetch_token(
        epicTokenUrl,
        content_type='application/x-www-form-urlencoded',
        Authorization='Basic ' + epicClientId + epicClientSecret,
        authorization_response=request.url,
        code=request.url.split('code=')[1].split('&')[0]
    )
    session['epicToken'] = token
    print(token)
    return 'Thanks for granting us authorization. We are logging you in! You can now visit <a href="/api/profile">/api/profile</a>'
