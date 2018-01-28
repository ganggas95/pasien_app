from flask import render_template, redirect, url_for, request
from flask_login import login_required
from pasien.models.table import Regular, Pasien, RawatJalan


@login_required
def form_regular(no_pasien):
    pasien = Pasien.query.filter(Pasien.no_pasien == no_pasien).first()
    if request.method == 'GET':
        return render_template("admin/pasien/form_regular.html", \
                    pasien=pasien,
                    page_title="Form Pelayanan Regular",
                    icon_img="/static/img/regular.png",
                    sub_title='Form pengisian pelayanan regular')
    if request.method == 'POST':
        if request.form['status'] == 'sembuh':
            regular = Regular()
            regular.keluhan = request.form['keluhan']
            regular.tindakan = request.form['tindakan']
            regular.status = request.form['status']
            regular.pasien_id = pasien.id
            try:
                regular.save()
                return redirect(url_for('register_pasien'))
            except Exception as e:
                flash("Terjadi kesalahan ketika menyimpan data", category='message')
                return redirect(url_for('form_regular', no_pasien=no_pasien))
        if request.form['status'] == 'rawat_jalan':
            rawat_jalan = RawatJalan()
            rawat_jalan.keluhan = request.form['keluhan']
            rawat_jalan.tindakan = request.form['tindakan']
            rawat_jalan.diagnosa = request.form['diagnosa']
            rawat_jalan.status = request.form['status']
            try:
                rawat_jalan.save()
                return redirect(url_for('register_pasien'))
            except Exception as e:
                flash("Terjadi kesalahan ketika menyimpan data", category='message')
                return redirect(url_for('form_regular', no_pasien=no_pasien))
