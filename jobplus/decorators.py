from flask import abort, current_app
from flask_login import current_user
from functools import wraps
from jobplus.models import User
import filecmp
import os

def role_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwrargs):
            if not current_user.is_authenticated or current_user.role != role:
                abort(404)
            return func(*args, **kwrargs)
        return wrapper
    return decorator

user_required = role_required(User.ROLE_JOBHUNTER)
company_required = role_required(User.ROLE_COMPANY)
admin_required = role_required(User.ROLE_ADMIN)




def get_filepath(url):
    basedir = current_app.static_folder
    path = url.split('/')[2:]
    path = os.path.sep.join(path)
    return os.path.join(basedir, path)



def check_exists(srcurl, target_urls):
    src_path = get_filepath(srcurl)
    for url in target_urls:
        dst_path = get_filepath(url)
        if filecmp.cmp(src_path, dst_path):
            return True
    return False





def remove_file(path):
    filepath = get_filepath(path)
    if os.path.exists(filepath):
        try:
            os.remove(filepath)
        except Exception as e:
            print(e)
            return False
        else:
            return True



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS']