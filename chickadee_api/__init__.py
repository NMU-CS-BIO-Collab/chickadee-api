from flask import Flask, request, current_app
import flask.logging
from flask_cors import CORS

import json
import logging
import os
from time import strftime

from .db.database import chickadeeDatabase
from .chickadee_api import main
from .views.birds import birds
from .views.visits import visits
from .views.feeders import feeders
from .views.users import users

from config import config
from .util import CustomJSONEncoder

def create_app(config_name=None):	
	app = Flask(__name__)
	CORS(app)

	if not config_name:
		config_name = os.environ.get('CHICK_CONFIG', 'development')
	app.config.from_object(config[config_name])

	app.config['DATABASE'] = chickadeeDatabase()
	with app.app_context():
		app.config['DATABASE'].mysql.init_app(app)

	app.json_encoder = CustomJSONEncoder

	if config_name is not 'production':
		logger = logging.getLogger(__name__)
		handler = logging.FileHandler('log')
		handler.setLevel(logging.INFO)
		logger.addHandler(handler)
		logger.setLevel(logging.INFO)

		app.config["LOGGER"] = logger

	app.register_blueprint(main)
	app.register_blueprint(birds, url_prefix='/api/birds')
	app.register_blueprint(visits, url_prefix='/api/visits')
	app.register_blueprint(feeders, url_prefix='/api/feeders')
	app.register_blueprint(users, url_prefix='/api/users')

	return app