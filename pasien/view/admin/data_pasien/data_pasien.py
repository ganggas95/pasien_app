from flask import redirect, render_template, flash, request, url_for
from pasien.models.table import Pasien, Keluarga
from flask_login import login_required

@login_required
def all_pasien():
    if request.method == 'GET':
        pasiens = Pasien.query.all()
        return render_template("admin/pasien/pasiens.html", \
                    pasiens=pasiens,
                    page_title = "Data Pasien",
                    icon="handicap",
                    sub_title = "Data semua pasien")
@login_required
def delete_pasien():
    if request.method == 'POST':
        pasien = Pasien.query.get(request.form['id'])
        try:
            pasien.delete()
            flash("Hapus data pasien berhasil", category="success")
            return redirect(url_for('all_pasien'))
        except Exception as e:
            flash("Hapus data pasien gagal", category="error")
            return redirect(url_for('all_pasien'))

@login_required
def edit_pasien(id):
    if request.method == 'GET':
        pasien = Pasien.query.get(id)
        keluarga = Keluarga.query.all()
        return render_template("admin/pasien/edit_pasien.html", \
                    pasien=pasien,
                    page_title="Edit Pasien",
                    icon="handicap",
                    keluarga=keluarga,
                    sub_title="Form untuk edit data pasien")
    if request.method == 'POST':
        pasien = Pasien.query.get(id)
        keluarga = Keluarga.query.filter(Keluarga.no_kk==request.form['nokk']).first()
        pasien.nama = request.form['nama']
        pasien.goldar = request.form['goldar']
        pasien.jk = request.form['gender']
        pasien.usia = request.form['usia']
        pasien.no_telp = request.form['no_telp']
        pasien.keluarga_id = keluarga.id
        try:
            pasien.save()
            return redirect(url_for("all_pasien"))
        except Exception as e:
            print(e)
            flash("Error ketika menyimpan perubahan.", category='message')
            return redirect(url_for("edit_pasien", id=pasien.id))
