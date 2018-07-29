from pasien.models.table import Pasien, PasienRujukan, RawatInap, RawatJalan, Regular
from flask import render_template, redirect , url_for, flash, request
from flask_login import login_required
@login_required
def history_pasien(id):
    pasien = Pasien.query.get(id)
    if request.method == 'GET':
        return render_template("admin/pasien/pasien_history.html",
                    pasien=pasien,
                    page_title="Riwayat Pelayanan",
                    sub_title="Daftar riwayat pelayanan pasien",
                    icon="history")

@login_required
def riwayat_rawat_inap(id):
    if request.method == 'GET':
        rawat_inap = RawatInap.query.filter(RawatInap.pasien_id==id).all()
        return render_template("admin/pasien/riwayat_rawat_inap.html",
                    rawat_inap=rawat_inap,
                    page_title="Riwayat Rawat Inap",
                    sub_title="Daftar riwayat pasien rawat inap",
                    icon_img="/static/img/rawat_inap.png")

@login_required
def riwayat_rawat_jalan(id):
    if request.method == 'GET':
        rawat_jalan = RawatJalan.query.filter(RawatJalan.pasien_id==id).all()
        return render_template("admin/pasien/riwayat_rawat_jalan.html",
                    rawat_jalan=rawat_jalan,
                    page_title="Riwayat Pelayanan",
                    sub_title="Daftar riwayat pasien rawat jalan",
                    icon_img="/static/img/rawat_jalan.png")

@login_required
def riwayat_rawat_rujukan(id):
    if request.method == 'GET':
        rawat_rujukan = PasienRujukan.query.filter(PasienRujukan.pasien_id==id).all()
        return render_template("admin/pasien/riwayat_rawat_rujukan.html",
                    rawat_rujukan=rawat_rujukan,
                    page_title="Riwayat Pelayanan",
                    sub_title="Daftar riwayat pasien rujukan",
                    icon_img="/static/img/rujukan.png")

@login_required
def riwayat_regular(id):
    if request.method == 'GET':
        regular = Regular.query.filter(Regular.pasien_id==id).all()
        return render_template("admin/pasien/riwayat_regular.html",
                    regular=regular,
                    page_title="Riwayat Pelayanan",
                    sub_title="Daftar riwayat pasien regular",
                    icon_img="/static/img/regular.png")
