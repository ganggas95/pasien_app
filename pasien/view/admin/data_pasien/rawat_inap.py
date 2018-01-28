from pasien.models.table import RawatInap, Pasien
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_required
@login_required
def form_rawat_inap(no_pasien):
    pasien = Pasien.query.filter(Pasien.no_pasien == no_pasien).first()
    if request.method == 'GET':
        return render_template("admin/pasien/form_rawat_inap.html", \
                    pasien=pasien,
                    page_title="Form Rawat Inap",
                    icon_img="/static/img/rawat_inap.png",
                    sub_title='Form pengisian pelayanan rawat inap')
    if request.method == 'POST':
        rawat_inap = RawatInap()
        rawat_inap.tanggal_masuk = request.form['tanggal_masuk']
        rawat_inap.tanggal_keluar = request.form['tanggal_keluar']
        rawat_inap.keluhan = request.form['keluhan']
        rawat_inap.tindakan = request.form['tindakan']
        rawat_inap.diagnosa = request.form['diagnosa']
        rawat_inap.status = request.form['status']
        rawat_inap.pasien_id = pasien.id
        try:
            rawat_inap.save()
            return redirect(url_for('register_pasien'))
        except Exception as e:
            flash("Terjadi kesalahan ketika menyimpan data", category='message')
            return redirect(url_for('form_rawat_inap', no_pasien=no_pasien))
