"""Models and database functions for Sasha's Unnamed Project."""

from flask_sqlalchemy import flask_sqlalchemy

db = SQLAlchemy()


###############################################################################
# Model Definitions


class Location(db.Model):
    """U.S. locations matched by state ID, congressional district, & state name."""

    __tablename__ = "locations"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    district_id = db.Column(db.Integer, nullable=True)
    state_id = db.Column(db.Integer, nullable=False)
    state_name = db.Column(db.String(15), nullable=False)
    citizens = relationship("Citizen", secondary="location_citizens_link")
    elected_reps = relationship("ElectedRep")

    def __repr__(self):
        return "<Location: Type things here later.>"


class Citizen(db.Model):
    """Employed U.S. citizens grouped by male/female & all jobs/management jobs."""

    __tablename__ = "citizens"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    female = db.Column(db.Boolean, nullable=False)
    manager = db.Column(db.Boolean, nullable=False)
    population = db.Column(db.Integer, nullable=True)
    location_id = db.Column(db.Integer, ForeignKey("locations.id"), nullable=False)
    locations = relationship("Location", secondary="location_citizens_link")

    def __repr__(self):
        return "<Citizen: Type things here later.>"


class LocationCitizenLink(db.Model):

    __tablename__ = "location_citizens_link"

    location_id = db.Column(db.Integer, ForeignKey("locations.id"), primary_key=True)
    citizen_id = db.Column(db.Integer, ForeignKey("citizens.id"), primary_key=True)

    def __repr__(self):
        return "<LocationCitizenLink: Type things here later.>"


class ElectedRep(db.Model):

    __tablename__ = "elected_reps"

    official_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    location_id = db.Column(db.Integer, ForeignKey("locations.id"), nullable=False)
    rep_type = db.Column(db.String(10), nullable=False)
    female = db.Column(db.Boolean, nullable=False)
    state_name = db.Column(db.String(15), nullable=False)
    year = db.Column(db.Integer)

    def __repr__(self):
        return "<ElectedRep: Type things here later.>"


class Zipcode(db.Model):

    __tablename__ = "zipcodes"

    zipcode = db.Column(db.Integer, nullable=False, primary_key=True)
    location_id = db.Column(db.Integer, ForeignKey("locations.id"), nullable=False)


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use PostgreSQL database
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///jobs"
    app.config["SQLALCHEMY_ECHO"] = True
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."