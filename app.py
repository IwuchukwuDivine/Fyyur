#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from email.policy import default
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import FlaskForm
from forms import *
from flask_migrate import Migrate
import datetime
from datetime import date
from models import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#




app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)



# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------
 # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
@app.route('/venues')
def venues():
  data = []
  venues = Venue.query.distinct(Venue.city, Venue.state).all()
  for venue in venues:
    area = {
      "city": venue.city,
      "state": venue.state
    }
    venues = Venue.query.filter_by(city=venue.city, state=venue.state).all()

    new_venues = []
    for venue in venues:
      new_venues.append({
        "id": venue.id,
        "name": venue.name,
        "num_upcoming_shows":venue.num_upcoming_shows
      })
    area["venues"] = new_venues
    data.append(area)  
    
  return render_template('pages/venues.html', areas=data)

# TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term = request.form.get('search_term', '')
  venues = Venue.query.filter(Venue.name.ilike(f'%{search_term}%'))
  # if the search for venues is found
  data = []
  for i in venues:
    data.append({
      'id': i.id,
      'name': i.name
    })
  response = {
    "count": venues.count(),
    "data": data
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

# TODO: replace with real venue data from the venues table, using venue_id
@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  data = Venue.query.get(venue_id)

# to get past shows
  past_shows_query = db.session.query(Shows).join(Artist).filter(Shows.venue_id==venue_id).filter(Shows.start_time<datetime.datetime.now()).all()   
  past_shows = []
  for show in past_shows_query:
        past = {}
        past["artist_name"] = show.artist.name
        past["artist_id"] = show.artist.id
        past["artist_image_link"] = show.artist.image_link
        past["start_time"] = show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
        past_shows.append(past)

# get upcoming shows 
  upcoming_shows_query = db.session.query(Shows).join(Artist).filter(Shows.venue_id==venue_id).filter(Shows.start_time>datetime.datetime.now()).all()   
  upcoming_shows = []
  for show in upcoming_shows_query:
    upcoming = {}
    upcoming["artist_name"] = show.artist.name
    upcoming["artist_id"] = show.artist.id
    upcoming["artist_image_link"] = show.artist.image_link
    upcoming["start_time"] = show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
    upcoming_shows.append(upcoming)
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

# TODO: insert form data as a new Venue record in the db, instead
@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = VenueForm()
  if form.validate_on_submit():
   try:
     venue = Venue(name = form.name.data,
                  city = form.city.data,
                  state = form.state.data,
                  address = form.address.data,
                  phone = form.phone.data,
                  genres = form.genres.data,
                  facebook_link = form.facebook_link.data,
                  image_link = form.image_link.data,
                  website_link = form.website_link.data,
                  seeking_talent = form.seeking_talent.data,
                  seeking_description = form.seeking_description.data)
     db.session.add(venue)
     db.session.commit()
    # if the venue form was succesfully submitted 
     flash('Venue ' + request.form['name'] + ' was successfully listed!')
   except Exception:
    # if the venue form didnt submit  
    flash('An error occurred. Venue ' + request.form.get('name') + ' could not be listed')
    db.session.rollback() 
    raise 
   finally:
    db.session.close()
  else:
    flash('Fill in the form correctly')
  return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  error = False
  try:
    # filtering the venue by that particular venue id and deleting immediately 
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
  except:
    db.session.rollback()
    error = True
  finally:
    db.session.close()  

  if error:  
    flash('Could not delete ' + Venue.name + '!')
  else:
    flash(Venue.name + 'successfully deleted!')
  return redirect(url_for('index'))
 
  

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  data = Artist.query.all()
  return render_template('pages/artists.html', artists=data)

 # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term = request.form.get('search_term', '')
  artists = Artist.query.filter(Artist.name.ilike(f'%{search_term}%'))
  # if the search for artist is found 
  data = []
  for i in artists:
    data.append({
      'id': i.id,
      'name':i.name
    })
  response = {
    "count": artists.count(),
    "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

 # TODO: replace with real artist data from the artist table, using artist_id
@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    data = Artist.query.get(artist_id)

    # to get past shows
    past_shows_query = db.session.query(Shows).join(Venue).filter(Shows.artist_id==artist_id).filter(Shows.start_time<datetime.datetime.now()).all()   
    past_shows = []
    for show in past_shows_query:
        past = {}
        past["venue_name"] = show.Venue.name
        past["venue_id"] = show.Venue.id
        past["venue_image_link"] = show.Venue.image_link
        past["start_time"] = show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
        past_shows.append(past)

  # get upcoming shows 
    upcoming_shows_query = db.session.query(Shows).join(Venue).filter(Shows.artist_id==artist_id).filter(Shows.start_time>datetime.datetime.now()).all()   
    upcoming_shows = []
    for show in upcoming_shows_query:
      upcoming = {}
      upcoming["venue_name"] = show.venue.name
      upcoming["venue_id"] = show.venue.id
      upcoming["venue_image_link"] = show.venue.image_link
      upcoming["start_time"] = show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
      upcoming_shows.append(upcoming)
    return render_template('pages/show_artist.html', artist=data) 


     
 


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)
  return render_template('forms/edit_artist.html', form=form, artist=artist)
 
 

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  form = ArtistForm()
  
  try:
    artist = Artist.query.get(artist_id)

    artist.name = form.name.data,
    artist.city = form.city.data
    artist.state = form.state.data
    artist.phone = form.phone.data
    artist.image_link = form.image_link.data
    artist.genres = form.genres.data
    artist.facebook_link = form.facebook_link.data
    artist.website_link = form.website_link.data
    artist.seeking_venue = form.seeking_venue.data
    artist.seeking_description = form.seeking_description.data
  
    db.session.commit()
    flash('Artist ' + request.form['name'] + 'was successfully updated!')
  except Exception:
    flash('An error occurred. Artist ' + request.form.get('name') + ' could not be updated')
    db.session.rollback() 
    raise 
  finally:
    db.session.close()
    return redirect(url_for('show_artist', artist_id=artist_id))



@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)
  
  return render_template('forms/edit_venue.html', form=form, venue=venue)
   
 

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  form = VenueForm()

  try:
      venue = Venue.query.get(venue_id)
   
      venue.name=form.name.data
      venue.city=form.city.data
      venue.state=form.state.data
      venue.address=form.address.data
      venue.phone=form.phone.data
      venue.image_link=form.image_link.data
      venue.genres=form.genres.data
      venue.facebook_link=form.facebook_link.data
      venue.website_link=form.website_link.data
      venue.seeking_talent=form.seeking_talent.data
      venue.seeking_description=form.seeking_description.data
      db.session.commit()
      flash('The venue ' + request.form['name'] + ' was successfully updated.')
  except Exception:
    flash('The venue ' + request.form['name'] + ' could not be updated!')
    db.session.rollback()
    raise 
  finally:
    db.session.close()  
  return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

# TODO: insert form data as a new Artist record in the db, instead
@app.route('/artists/create', methods=['POST'])
def create_artists_submission():
  form = ArtistForm(request.form)
  error = False
  if form.validate_on_submit():
   try:
     artist = Artist(name = form.name.data,
                  city = form.city.data,
                  state = form.state.data,
                  phone = form.phone.data,
                  image_link = form.image_link.data,
                  genres = form.genres.data,
                  facebook_link = form.facebook_link.data,
                  website_link = form.website_link.data,
                  seeking_venue = form.seeking_venue.data,
                  seeking_description = form.seeking_description.data)
  
     db.session.add(artist)
     db.session.commit()
     # on successful db insert, flash success
     flash('Artist ' + request.form['name'] + 'was successfully listed!')
   except Exception:
      # TODO: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Artist ' + request.form.get('name') + ' could not be listed')
    db.session.rollback() 
    raise 
   finally:
    db.session.close()
  else:
    flash('Input the correct data')
  return render_template('pages/home.html')

 

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  shows = Shows.query.all()
  data=[]
  for i in shows:
    show = {}
    show["venue_id"] = i.Venue.id
    show["venue_name"] = i.Venue.name
    show["artist_id"] = i.artist.id
    show["artist_name"] = i.artist.name
    show["artist_image_link"] = i.artist.image_link
    show["start_time"] = i.start_time.strftime("%m/%d/%Y, %H:%M:%S")
    data.append(show)
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  form = ShowForm(request.form)
  error = False
  try:
    show = Shows(artist_id=form.artist_id.data,
                venue_id=form.venue_id.data,
                start_time=form.start_time.data)
    db.session.add(show)
    db.session.commit()
     # on successful db insert, flash success
    flash('Show was successfully listed!')
  except Exception:
    # on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Show could not be listed.')
    db.session.rollback() 
    raise 
  finally:
    db.session.close()
  return render_template('pages/home.html')



@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
