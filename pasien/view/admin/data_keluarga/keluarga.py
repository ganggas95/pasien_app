from pasien.models.table import Keluarga, Pasien
from flask import render_template, redirect, flash, url_for, request
from flask_login import login_required
import logging


@login_required
def data_keluarga():
    if request.method=='GET':
        keluargas = Keluarga.query.all()
        return render_template('admin/keluarga/keluargas.html', keluargas=keluargas, page_title="Data Keluarga", icon="users", sub_title="Data semua keluarga")
    if request.method == 'POST':
        keluarga = Keluarga()
        keluarga.kepala_keluarga = request.form['kepala_keluarga']
        keluarga.no_kk = request.form['no_kk']
        keluarga.alamat = request.form['alamat']
        try:
            keluarga.save()
            flash('Data berhasil di simpan.', category='success')
            return redirect(url_for('data_keluarga'))
        except Exception as identifier:
            flash('Data gagal di simpan.', category='error')
            return redirect(url_for('data_keluarga'))

def pasien_keluarga(id):
    if request.method == "GET":
        pasiens = Pasien.query.filter(Pasien.keluarga_id==id).all()
        return render_template('admin/keluarga/keluarga_pasien.html', pasiens=pasiens, page_title="Data Pasien", sub_title="Data pasien berdasarkan keluarga", icon="handicap")            

def edit_keluarga(id):
    if request.method == 'POST':
        keluarga = Keluarga.query.get(id)
        keluarga.kepala_keluarga = request.form['kepala_keluarga']
        keluarga.no_kk = request.form['no_kk']
        keluarga.alamat = request.form['alamat']
        try:
            keluarga.save()
            flash('Data berhasil di simpan.', category='success')
            return redirect(url_for('data_keluarga'))
        except Exception as identifier:
            logging.warning(identifier)
            flash('Data gagal di simpan.', category='error')
            return redirect(url_for('data_keluarga'))

def delete_keluarga():
    if request.method == 'POST':
        keluarga = Keluarga.query.get(request.form['id'])
        try:
            keluarga.delete()
            flash('Data berhasil di hapus.', category='success')
            return redirect(url_for('data_keluarga'))
        except Exception as identifier:
            logging.warning(identifier)
            flash('Data gagal di hapus.', category='error')
            return redirect(url_for('data_keluarga'))
