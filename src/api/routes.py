"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, redirect, Blueprint
from flask_oauthlib.client import OAuth
from api.models import db, User
from api.utils import generate_sitemap, APIException
from api.steamHours import steamHours

api = Blueprint('api', __name__)

#set up OAuth2.0
oauth = OAuth()

#steamOAuth setup

#blizzardOAuth setup
blizzardClientId = os.getenv("BLIZZARD_CLIENT_ID")
blizzardClientSecret = os.getenv("BLIZZARD_CLIENT_SECRET")


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