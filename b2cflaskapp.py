from flask import Flask, redirect, url_for, session, request, jsonify, render_template
from flask_oauthlib.client import OAuth, OAuthException

from jose import jws
import json
import requests

from logging import Logger
import uuid

app = Flask(__name__)
app.debug = True
app.secret_key = 'development'
oauth = OAuth(app)

# === Update these values ===========
tenant_id = 'fabrikamb2c.onmicrosoft.com'
client_id = 'fdb91ff5-5ce6-41f3-bdbd-8267c817015d'
client_secret = 'X330F3#92!z614M4'
policy_name = 'b2c_1_susi'
# ===================================

scopes = 'openid ' + client_id

core_url = 'https://login.microsoftonline.com/tfp/' + tenant_id +'/' + policy_name
token_url = core_url + '/oauth2/v2.0/token'
authorize_url = core_url + '/oauth2/v2.0/authorize'
keys_url = core_url + '/discovery/keys'

# This sample loads the keys on boot, but for production
# the keys should be refreshed either periodically or on 
# jws.verify fail to be able to handle a key rollover
keys_raw = requests.get(keys_url).text
keys = json.loads(keys_raw)	

# Put your consumer key and consumer secret into a config file
# and don't check it into github!!
microsoft = oauth.remote_app(
	'microsoft',
	consumer_key=client_id,
	consumer_secret=client_secret,
	request_token_params={'scope': scopes },
	base_url='http://ignore',  # We won't need this
	request_token_url=None,
	access_token_method='POST',
	access_token_url=token_url,
	authorize_url=authorize_url
)


@app.route('/')
def index():
	return render_template('hello.html')

@app.route('/login', methods = ['POST', 'GET'])
def login():

	if 'microsoft_token' in session:
		return redirect(url_for('me'))

	# Generate the guid to only accept initiated logins
	guid = uuid.uuid4()
	session['state'] = guid

	return microsoft.authorize(callback=url_for('authorized', _external=True), state=guid)
	
@app.route('/logout', methods = ['POST', 'GET'])
def logout():
	session.pop('microsoft_token', None)
	session.pop('claims', None)
	session.pop('state', None)
	return redirect(url_for('index'))

@app.route('/login/authorized')
def authorized():
	response = microsoft.authorized_response()

	if response is None:
		return "Access Denied: Reason=%s\nError=%s" % (
			response.get('error'), 
			request.get('error_description')
		)
		
	# Check response for state
	print("Response: " + str(response))
	if str(session['state']) != str(request.args['state']):
		raise Exception('State has been messed with, end authentication')
		
	# Okay to store this in a local variable, encrypt if it's going to client
	# machine or database. Treat as a password.
	access_token = response['access_token'] 
	session['microsoft_token'] = (access_token, '')
	session['claims'] = json.loads(jws.verify(access_token, keys, algorithms=['RS256']))

	return redirect(url_for('me')) 

@app.route('/me')
def me():
	token = session['microsoft_token'][0]
	claims = session['claims']
	return render_template('me.html', me=str(claims))

# If library is having trouble with refresh, uncomment below and implement refresh handler
# see https://github.com/lepture/flask-oauthlib/issues/160 for instructions on how to do this

# Implements refresh token logic
# @app.route('/refresh', methods=['POST'])
# def refresh():

@microsoft.tokengetter
def get_microsoft_oauth_token():
	return session.get('microsoft_token')

if __name__ == '__main__':
	app.run()
