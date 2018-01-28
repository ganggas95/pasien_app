from pasien import app
from flask import session, render_template, redirect, flash, url_for, request
from pasien.models.table import Users
from flask_login import LoginManager, login_required, login_user, logout_user
from datetime import timedelta
from sqlalchemy import or_
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'

@login_manager.user_loader
def load_user(user):
    return Users.query.get(user)

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=1)


def admin_login():
    if request.method == 'GET':
        return render_template("auth/login.html", page_title="Login User Page")
    username = request.form['username']
    password = request.form['password']
    user = Users.query.filter(or_(Users.username==username, Users.email==username)).first()
    if user:
        if user.check_password(password):
            next = request.args.get('next')
            
            session['logged_in']= True
            session['username'] = username
            login_user(user)
            flash("Selamat Datang {}".format(user.username), category='success')
            return redirect(next or url_for('admin_dashboard'))
        flash("Username dan Password salah. Coba lagi!!", category='error')
        return redirect(url_for("admin_login"))
    flash("Username dan Password salah. Coba lagi!!", category='error')
    return redirect(url_for("admin_login"))
@login_required
def admin_logout():
    session.clear()
    logout_user()
    flash("Logout Berhasil.!!!", category='success')
    return redirect(url_for("admin_login"))