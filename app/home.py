from flask import (Blueprint, flash, g, redirect,
                   render_template, request, url_for, session)


bp = Blueprint('home', __name__, url_prefix='/')


@bp.route('/')
def index():
    return render_template('home/index.html')
