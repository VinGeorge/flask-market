from flask import session, redirect, Blueprint

bp = Blueprint("logout", __name__)


@bp.route('/logout/')
def logout():

    session.pop('id')
    session.pop('mail')

    return redirect('/')