from pasien.models.table import Users
from flask import flash, render_template, redirect, url_for, request
from flask_login import login_required
import hashlib
@login_required
def users():
    if request.method == 'GET':
        users = Users.query.all()
        return render_template("admin/user/users.html", users=users, page_title="Data User", icon="users")
    if request.method == 'POST':
        user = Users()
        user.username = request.form['username']
        user.email = request.form['email']
        user.password = hashlib.md5(str(hashlib.sha256(str(request.form['password']).encode('utf-8')).hexdigest()).encode('utf-8')).hexdigest()
        try:
            user.save()
            flash("Berhasil menambah user", category="success")
            return redirect(url_for('users'))
        except Exception as e:
            flash("Terjadi error ketika menambah user", category='error')
            return redirect(url_for('users'))
@login_required
def user_edit(id):
    if request.method == 'POST':
        user = Users.query.get(id)
        user.username = request.form['username']
        user.email = request.form['email']
        try:
            user.save()
            flash("Berhasil menyimpan data", category='success')
            return redirect(url_for('users'))
        except Exception as e:
            flash("Terjadi kesalahan menyimpan data", category='error')
            return redirect(url_for('users'))

@login_required
def user_edit_password(id):
    if request.method == 'POST':
        user = Users.query.get(id)
        user.password = hashlib.md5(str(hashlib.sha256(str(request.form['new_password']).encode('utf-8')).hexdigest()).encode('utf-8')).hexdigest()
        try:
            user.save()
            flash("Berhasil menyimpan data", category='success')
            return redirect(url_for('users'))
        except Exception as e:
            flash("Terjadi kesalahan menyimpan data", category='error')
            return redirect(url_for('users'))

@login_required
def user_delete():
    if request.method == 'POST':
        user = Users.query.get(request.form['id'])
        try:
            user.delete()
            flash("Berhasil menghapus data", category='success')
            return redirect(url_for('users'))
        except Exception as e:
            flash("Terjadi kesalahan menghapus data", category='error')
            return redirect(url_for('users'))
