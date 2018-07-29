from flask import render_template, url_for, redirect, request, flash
from pasien.models.table import Pasien, Keluarga
from pasien.core import create_no_pasien
# from flask_weasyprint import HTML, render_pdf
from flask_login import login_required

@login_required
def register_pasien():
    if request.method=='GET':
        visible = False
        cek = False
        visible_old = False
        cek_old = False
        nik = None
        no_pasien = None
        page_title="Register Pasien"
        sub_title="Register pasien baru/Pelayanan Pasien Lama"
        icon="add user"
        pasien = None
        if request.args.get('nik'):
            pasien = Pasien.query.filter(Pasien.nik==request.args.get('nik')).first()
            visible = True if pasien else False
            cek = True
            nik = request.args.get('nik') if not pasien else None
            if pasien:
                flash("Nik yang anda masukkan telah digunakan.", category='warning')
        if request.args.get('no_pasien'):
            pasien = Pasien.query.filter(Pasien.no_pasien==request.args.get('no_pasien')).first()
            visible_old = True if pasien else False
            visible = False if pasien else True
            cek = True
            icon="browser"
            page_title="Pelayanan Pasien"
            sub_title="Daftar Pelayanan Untuk Pasien"
            no_pasien = request.args.get('no_pasien') if pasien else None
            if pasien:
                flash("Silahkan pilih layanan yang ada.", category='success')
            else:
                flash("Pasien dengan no reg. {} kosong.".format(request.args.get('no_pasien')), category='warning')
        keluarga = Keluarga.query.all()

        return render_template("admin/pasien/register_pasien.html", \
                        page_title=page_title,
                        visible=visible,
                        cek=cek,
                        nik=nik,
                        cek_old=cek_old,
                        visible_old = visible_old,
                        no_pasien=no_pasien,
                        sub_title=sub_title,
                        icon=icon,
                        pasien=pasien,
                        keluarga=keluarga)

    if request.method == 'POST':
        pasien = Pasien()
        keluarga = Keluarga.query.filter(Keluarga.no_kk==request.form['nokk']).first()
        pasien.no_pasien = create_no_pasien()
        pasien.nama = request.form['nama']
        pasien.nik = request.args.get('nik')
        pasien.jk = request.form['gender']
        pasien.goldar = request.form['goldar']
        pasien.no_telp = request.form['no_telp']
        pasien.usia = request.form['usia']
        pasien.keluarga = keluarga
        try:
            pasien.save()
            return redirect(url_for('detail_pasien', no_pasien=pasien.no_pasien))
        except Exception as e:
            logging.warning(e)
            flash("Terjadi Kesalahan ketika menyimpan data", category='message')
            return redirect(url_for('register_pasien'))

@login_required
def detail_pasien(no_pasien):
    if request.method == 'GET':
        pasien = Pasien.query.filter(Pasien.no_pasien==no_pasien).first()
        return render_template("admin/pasien/detail_pasien.html", \
                        pasien=pasien,
                        page_title="Detail Pasien : {}".format(pasien.nama),
                        sub_title="No. Reg {}".format(pasien.no_pasien),
                        icon="grid layout")

@login_required
def pdf_pasien(no_pasien):
    if request.method == 'GET':
        pasien = Pasien.query.filter(Pasien.no_pasien==no_pasien).first()
        pdf = render_template("admin/pasien/pdf.html", pasien=pasien, page_title="Print Kartu Berobat Pasien : {}".format(no_pasien))
        return pdf
