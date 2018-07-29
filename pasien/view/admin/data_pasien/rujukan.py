from pasien.models.table import RawatInap, PasienRujukan, Pasien
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_required

@login_required
def form_rujukan(no_pasien):
    pasien = Pasien.query.filter(Pasien.no_pasien == no_pasien).first()
    if request.method == 'GET':
        return render_template("admin/pasien/form_rujukan.html", \
                    pasien=pasien,
                    page_title="Form Pasien Rujukan",
                    icon_img="/static/img/rujukan.png",
                    sub_title='Form pengisian pelayanan pasien rujukan')
    if request.method == 'POST':
        rawat_inap = RawatInap()
        rujukan = PasienRujukan()
        rujukan.asal = request.form['asal']
        rujukan.keterangan = request.form['keterangan']
        rawat_inap.tanggal_masuk = request.form['tanggal_masuk']
        rawat_inap.tanggal_keluar = request.form['tanggal_keluar']
        rawat_inap.diagnosa = request.form['diagnosa']
        rawat_inap.status = request.form['status']
        rawat_inap.pasien_id = pasien.id
        rujukan.pasien_id = pasien.id
        rujukan.rawat_inap = rawat_inap
        try:
            rawat_inap.save()
            rujukan.save()
            return redirect(url_for('register_pasien'))
        except Exception as e:
            flash("Terjadi kesalahan ketika menyimpan data", category='message')
            return redirect(url_for('form_rujukan', no_pasien=no_pasien))
