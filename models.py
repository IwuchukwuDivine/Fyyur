from flask_sqlalchemy import SQLAlchemy
import datetime
from datetime import date

db = SQLAlchemy()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    website_link = db.Column(db.String(300), nullable=False)
    seeking_talent = db.Column(db.Boolean, nullable=False, default=True)
    seeking_description = db.Column(db.String(300), nullable=False)
    shows = db.relationship('Shows', backref='Venue', lazy=True)

    def __repr__(self):
      return f'<Venue: id={self.id} name={self.name} city={self.city} state={self.state}>'

    @property
    def num_upcoming_shows_count(self) ->int:
      return Shows.query.filter(Shows.artist_id == self.id, Shows.start_time >= date.today()).count()

    @property
    def num_past_shows_count(self) ->int:
      return Shows.query.filter(Shows.artist_id == self.id, Shows.start_time < date.today()).count()

    @property
    def num_upcoming_shows(self) ->int:
      return Shows.query.filter(Shows.artist_id == self.id, Shows.start_time >= date.today()).all()

    @property
    def num_past_shows(self) ->int:
      return Shows.query.filter(Shows.artist_id == self.id, Shows.start_time < date.today()).all()

  

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(300), nullable=False)
    seeking_venue = db.Column(db.Boolean, nullable=False, default=True)
    seeking_description = db.Column(db.String(300), nullable=False)
    shows = db.relationship('Shows', backref='artist', lazy=True)

    def __repr__(self):
      return f'<Artist: {self.id} '

    @property
    def num_upcoming_shows_count(self) ->int:
      return Shows.query.filter(Shows.artist_id == self.id, Shows.start_time >= date.today()).count()

    @property
    def num_past_shows_count(self) ->int:
      return Shows.query.filter(Shows.artist_id == self.id, Shows.start_time < date.today()).count()

    @property
    def num_upcoming_shows(self) ->int:
      return Shows.query.filter(Shows.artist_id == self.id, Shows.start_time >= date.today()).all()

    @property
    def num_past_shows(self) ->int:
      return Shows.query.filter(Shows.artist_id == self.id, Shows.start_time < date.today()).all()


# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Shows(db.Model):
     __tablename__ = 'shows'
     id = db.Column(db.Integer, primary_key=True)
     artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
     venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
     start_time = db.Column(db.DateTime(), nullable=False)

     def __repr__(self):
      return f'<Shows: id={self.id} start_time={self.start_time} artist_id={self.artist_id} venue_id{self.venue_id}>'   