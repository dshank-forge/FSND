#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form #,FlaskForm -- the Form module may be replaced by FlaskForm at some point.
from forms import *

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    shows = db.relationship('Show', backref='venue-br', lazy=True)    
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    shows = db.relationship('Show', backref='artist-br', lazy=True)       
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500), unique=True) 
    facebook_link = db.Column(db.String(120))

class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    venue = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)  
    artist = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False) 
    datetime = db.Column(db.DateTime, nullable=True) #datetime 
    image_link = db.Column(db.String(500), nullable=True) 


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: num_shows should be aggregated based on number of upcoming shows per venue.

  all_venues = Venue.query.group_by(Venue.id, Venue.state, Venue.city).all()
  pairs = set()
  
  #Get each unique city/state pair
  for v in all_venues:
      state = v.state
      city = v.city 
      pair = (state, city) 
      pairs.add(pair)   

  db_areas = []

  #For each pair, associate proper records(venues)
  index = 0
  for pair in pairs:
      db_areas.append({
        "city": pair[1],
        "state": pair[0],
        "venues": []  
      })
      records = Venue.query.filter_by(state=pair[0], city=pair[1])
      for record in records:
          db_areas[index]["venues"].append(record) 
      index += 1

  return render_template('pages/venues.html', areas=db_areas)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  my_search_term = request.form.get('search_term', '')
  my_venues = Venue.query.filter(Venue.name.ilike('%' + my_search_term + '%')).all()
  venue_count = Venue.query.filter(Venue.name.ilike('%' + my_search_term + '%')).count()

  my_response = {
    "count": venue_count,
    "data": my_venues
  }

  return render_template('pages/search_venues.html', results=my_response, search_term=my_search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  #TODO(?): Upcoming Shows and Past Shows.
  my_venue = Venue.query.get(venue_id)

  return render_template('pages/show_venue.html', venue=my_venue)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  print('/venues/create, methods = [\'GET\'] ')
  return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  name = request.form.get('name')
  city = request.form.get('city')
  state = request.form.get('state')
  address = request.form.get('address')
  phone = request.form.get('phone')
  genres = request.form.get('genres')
  facebook_link = request.form.get('facebook_link')
  
  new_venue = Venue(name=name,
                    city=city,
                    state=state,
                    address=address,
                    phone=phone,
                    genres=genres,
                    image_link='www.imagelink.com',
                    facebook_link=facebook_link
                    )
  
  try:
      db.session.add(new_venue)
      db.session.commit()
      flash('Venue ' + name + ' was successfully listed!')
  except:
      # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/  
      flash('An error occurred. Venue ' + name + ' could not be listed.')
  finally:
      return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  print('\n---\nIn the delete_venue controller\n---\n')
  venue = Venue.query.get(venue_id)
  print(venue)
  try:
    print('delete this venue')
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
    print('venue deleted.')
  except:
    print('exception!')
    db.session.rollback()
  finally:
    db.session.close()

  return render_template('pages/home.html')
  
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  
  # print('\n\nDelete Route\n\n')
  
  

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  all_artists = Artist.query.all()
  
  print(all_artists)

  return render_template('pages/artists.html', artists=all_artists)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  my_search_term = request.form.get('search_term', '')
  my_artists = Artist.query.filter(Artist.name.ilike('%' + my_search_term + '%')).all()
  artist_count = Artist.query.filter(Artist.name.ilike('%' + my_search_term + '%')).count()

  my_response = {
    "count": artist_count,
    "data": my_artists
  }

  return render_template('pages/search_artists.html', results=my_response, search_term=my_search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  #TODO(?): Upcoming Shows and Past Shows.
  my_artist = Artist.query.get(artist_id)

  return render_template('pages/show_artist.html', artist=my_artist)

#  Update
#  ----------------------------------------------------------------

@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  my_artist = Artist.query.get(artist_id)
  form = ArtistForm(obj=my_artist)
  return render_template('forms/edit_artist.html', form=form, artist=my_artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  try: 
    artist = Artist.query.get(artist_id)
    artist.name = request.form.get('name')
    artist.city = request.form.get('city')
    artist.state = request.form.get('state')
    artist.phone = request.form.get('phone')
    artist.genres = request.form.get('genres')
    artist.facebook_link = request.form.get('facebook_link')
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.get(venue_id)
  form = VenueForm(obj=venue)
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  try:
    venue = Venue.query.get(venue_id)
    venue.name = request.form.get('name')
    venue.city = request.form.get('city')
    venue.state = request.form.get('state')
    venue.address = request.form.get('address')
    venue.phone = request.form.get('phone')
    venue.genres = request.form.get('genres')
    venue.facebook_link = request.form.get('facebook_link')
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  name = request.form.get('name')
  city = request.form.get('city')
  state = request.form.get('state')
  phone = request.form.get('phone')
  genres = request.form.get('genres')
  facebook_link = request.form.get('facebook_link')
  
  new_artist = Artist(name=name,
                    city=city,
                    state=state,
                    phone=phone,
                    genres=genres,
                    image_link='www.imagelink.com' + request.form.get('name'),
                    facebook_link=facebook_link
                    )
  
  try:
      db.session.add(new_artist)
      db.session.commit()
      flash('Artist ' + name + ' was successfully listed!')
  except:
      # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/  
      flash('An error occurred. Artist ' + name + ' could not be listed.')
  finally:
      return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():

  my_shows = Show.query.all()
  
  show_list = []
  for show in my_shows:
      venue = Venue.query.get(show.venue)
      artist = Artist.query.get(show.artist)
      show_list.append({
        'venue_id': show.venue,
        'venue_name': venue.name,
        'artist_id': show.artist,
        'artist_name': artist.name,
        'artist_image_link': artist.image_link,
        'start_time': str(show.datetime)
      })

  return render_template('pages/shows.html', shows=show_list)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  artist_id = request.form.get('artist_id')
  venue_id = request.form.get('venue_id')
  start_time = request.form.get('start_time')

  new_show = Show(venue=venue_id,
                    artist=artist_id,
                    datetime=start_time,
                    image_link='www.imagelink.com',
                    )
  
  try:
      db.session.add(new_show)
      db.session.commit()
      flash('Show was successfully listed!')
  except:
      # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/  
      flash('An error occurred. Show could not be listed.')
  finally:
      return render_template('pages/home.html')

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
    #migrate.migrate()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
