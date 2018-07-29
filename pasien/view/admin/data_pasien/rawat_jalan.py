from pasien.models.table import RawatJalan, Pasien
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_required


@login_required
def form_rawat_jalan(no_pasien):
    pasien = Pasien.query.filter(Pasien.no_pasien == no_pasien).first()
    if request.method == 'GET':
        return render_template("admin/pasien/form_rawat_jalan.html", \
                    pasien=pasien,
                    page_title="Form Rawat Jalan",
                    icon_img="/static/img/rawat_jalan.png",
                    sub_title='Form pengisian pelayanan rawat jalan')
    if request.method == 'POST':
        rawat_jalan = RawatJalan()
        rawat_jalan.keluhan = request.form['keluhan']
        rawat_jalan.tindakan = request.form['tindakan']
        rawat_jalan.diagnosa = request.form['diagnosa']
        rawat_jalan.status = request.form['status']
        rawat_jalan.pasien_id = pasien.id
        try:
            rawat_jalan.save()
            return redirect(url_for('register_pasien'))
        except Exception as e:
            flash("Terjadi kesalahan ketika menyimpan data", category='message')
            return redirect(url_for('form_rawat_jalan', no_pasien=no_pasien))
