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

api = Blueprint('api', __name__)

#set up OAuth2.0
oauth = OAuth()
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

#steamOAuth setup

#blizzardOAuth setup
blizzardBaseApiUrl = 'https://oauth.battle.net'
blizzardClientId = os.getenv("BLIZZARD_CLIENT_ID")
blizzardClientSecret = os.getenv("BLIZZARD_CLIENT_SECRET")
blizzardRedirectUri='https://localhost:3001/api/blizzardAuthorization'
blizzardScope = ['wow.profile', 'sc2.profile', 'd3.profile']
blizzardTokenUrl = 'https://oauth.battle.net/token'
blizzardAuthorizeUrl = 'https://oauth.battle.net/authorize'


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route('/steamId', methods=['GET'])
def steamId():

    id = request.args.get("id")

    response_body = {

        "message": steamHours(id)
    }

    return jsonify(response_body), 200

@api.route('/blizzardLogin')
def blizzardLogin():
    oauth = OAuth2Session(blizzardClientId, redirect_uri=blizzardRedirectUri, scope=blizzardScope)
    login_url, state = oauth.authorization_url(blizzardAuthorizeUrl)
    session['state'] = state
    print("Login url: %s" % login_url)
    return '<a href="' + login_url + '">Login with Blizzard</a>'

@api.route('/blizzardAuthorization')
def blizzardAuthorization():
    blizzard = OAuth2Session(blizzardClientId, redirect_uri=blizzardRedirectUri, state=session['state'], scope=blizzardScope)
    token = blizzard.fetch_token(
        blizzardTokenUrl,
        client_secret=blizzardClientSecret,
        scope=blizzardScope,
        authorization_response=request.url
    )
    session['blizzardToken'] = token
    print(token)
    return 'Thanks for granting us authorization. We are logging you in! You can now visit <a href="/profile">/profile</a>'