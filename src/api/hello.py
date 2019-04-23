from flask import Blueprint, render_template
from api.story_generator import create_demo_story

bp = Blueprint('root', __name__, '/')

# === Initial Flask Routes ===

@bp.route('/')
def hello():
    """The root route will just return a string"""    
    story = create_demo_story()
    return story

@bp.route('/spa')
def load_spa():
    return render_template('index.html')
