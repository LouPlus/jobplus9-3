from flask import Blueprint, render_template


company = Blueprint('company', __name__, url_prefix='/company')

@company.route('/')
def index():
    return render_template('company/index.html')
