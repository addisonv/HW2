## SI 364
## Winter 2018
## HW 2 - Part 1

#By:Addison Viener 

## This homework has 3 parts, all of which should be completed inside this file (and a little bit inside the /templates directory).

## Add view functions and any other necessary code to this Flask application code below so that the routes 
#described in the README exist and render the templates they are supposed to (all templates provided are inside the templates/ directory, 
#where they should stay).

## As part of the homework, you may also need to add templates (new .html files) to the templates directory.

#############################
##### IMPORT STATEMENTS #####
#############################
from flask import Flask, request, render_template, url_for, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError
from wtforms.validators import Required
import requests 
import json

#####################
##### APP SETUP #####
#####################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'

####################
###### FORMS #######
####################




####################
###### ROUTES ######
####################

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user/<name>')
def hello_user(name):
    return '<h1>Hello {0}<h1>'.format(name)

@app.route('/artistform')
def artist_form():
	return render_template('artistform.html')

@app.route('/artistinfo', methods = ['GET'])
def artist_info():
	if request.method == 'GET':
		name = request.args.get('artist')
		baseurl = "https://itunes.apple.com/search?"
		artist_param_dict = {"entry":"musicArtist"}
		artist_param_dict["term"] = name
		response = requests.get(baseurl, params=artist_param_dict)
		text = response.text
		text_json = json.loads(text)
		objects = text_json['results']
		return render_template('artist_info.html', objects = objects)

@app.route('/artistlinks')
def artist_links():
	return render_template('artist_links.html', )

@app.route('/specific/song/<artist_name>')
def specific_song(artist_name):
	baseurl = "https://itunes.apple.com/search?"
	artist_param_dict = {"entry":"musicArtist"}
	artist_param_dict["term"] = artist_name
	response = requests.get(baseurl, params=artist_param_dict)
	text = response.text
	text_json = json.loads(text)
	results = text_json['results'] 
	return render_template('specific_artist.html', results = results)

class albumEntryForm(FlaskForm):
	album_name = StringField('Enter the name of an album:', validators = [ Required() ])
	radio = RadioField('How much do you like this album?', choices = [('1', '1'), ('2', '2'), ('3', '3')], validators = [ Required() ])
	submit = SubmitField('Submit')

@app.route('/album_entry')
def album_form():
	form = albumEntryForm()
	return render_template('album_entry.html', form = form)

@app.route('/album_result', methods = ['GET', 'POST'])
def album_result():
	if request.method == 'POST':
	 	form = albumEntryForm(request.form)
	 	album_title = iform.album_name.data
	 	album_score = iform.radio.data
	 	print(album_title)
	 	print(album_score)
	 	return render_template('album_data.html', album_title = album_title, album_score = album_score)
	# flash("All fields are required!")
	# return redirect(url_for('album_entry'))
 		
if __name__ == "__main__":
    app.run(use_reloader=True,debug=True)

