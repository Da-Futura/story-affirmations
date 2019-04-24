# == Intention ==

"""
The base routes for the application will be defined here.
This includes the route which serves the single page react app,
as well as all the appropriate api routing.
"""


from flask import Blueprint, render_template
from api.story_generator import create_demo_story

bp = Blueprint('root', __name__, '/') 
# Flask uses the [Blueprint object](http://flask.pocoo.org/docs/1.0/blueprints/) in order to structure the routing. _\"A Blueprint object works similarly to a Flask application object, but it is not actually an application. Rather it is a blueprint of how to construct or extend an application.\"_


@bp.route('/')
def load_react_app():
    """The Single Page React app is served at the root url, ie. http://tinystory.me/"""
    return render_template('index.html')

# == API Route Pattern ==

"""
We want a consistent pattern for our frontend to make api calls
to our backend. Because we're unsure what this application will
ultimately look like, the routes will be very generic following 
the pattern: 

***/api / class / action***
"""

@bp.route('/api/story/demo')
def demo():
    """The root route will return a string with a demo story"""    
    story = create_demo_story()
    return story

@bp.route('/api/character/create')    
def create_character():
        return "Call made"


