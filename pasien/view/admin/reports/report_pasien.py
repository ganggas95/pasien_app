from pasien import app
from pasien.models.table import Pasien, PasienRujukan, RawatInap, RawatJalan

from flask import flash, render_template, redirect, url_for, request, make_response
from flask_login import login_required
from sqlalchemy import and_, or_, cast, Date, between
import datetime
import pandas as pd
# from flask_weasyprint import HTML, render_pdf
try:
    from io import BytesIO
except ImportError:
    from cStringIO import StringIO as BytesIO
@login_required
def report_pasien():
    if request.method == 'GET':
        pasiens = Pasien.query
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        if start_date and end_date:
            pasiens = pasiens.filter(Pasien.create_at.between(start_date, end_date))
        pasiens = pasiens.all()
        return render_template("admin/report/report_pasien.html",
                pasiens=pasiens,
                page_title="Report Data Pasien",
                icon="handicap",
                sub_title="Report data pasien",
                start_date=start_date,
                end_date=end_date)
@login_required
def export_pasien_excel():
    if request.method == 'GET':
        pasiens = Pasien.query
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        if start_date and end_date:
            pasiens = pasiens.filter(Pasien.create_at.between(start_date, end_date))
        workbook = create_pasien_as_excel(pasiens.all())
        excel = make_response(workbook, 200)
        excel.mimetype = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        return excel
@login_required
def export_pasien_pdf():
    if request.method == 'GET':
        pasiens = Pasien.query
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        if start_date and end_date:
            pasiens = pasiens.filter(Pasien.create_at.between(start_date, end_date))
        pdf = render_template('admin/report/pdf/report_pasien.html',
                pasiens=pasiens.all(),
                start_date=datetime.datetime.strptime(start_date, '%Y-%m-%d'),
                end_date=datetime.datetime.strptime(end_date, '%Y-%m-%d'),
                report_title="Laporan Data Pasien")
        return pdf
        # return pdf

def create_pasien_as_excel(pasiens):
    nama = []
    no_pasien = []
    tanggal = []
    nik = []
    status = []
    goldar = []
    jk = []
    sio = BytesIO()
    for p in pasiens:
        nama.append(p.nama)
        no_pasien.append(p.no_pasien)
        nik.append(p.nik)
        status.append(p.status)
        goldar.append(p.goldar.value)
        jk.append(p.jk)
        tanggal.append(p.create_at.strftime('%d-%B-%Y') if p.create_at else "-")

    df = pd.DataFrame({
        "Nama":nama,
        "No Pasien": no_pasien,
        "NIK": nik,
        "Gol. Darah" : goldar,
        "J. Kelamin" : jk,
        "Status" : status,
        "Tanggal Daftar": tanggal})
    writer = pd.ExcelWriter(sio, engine='xlsxwriter')
    df.to_excel(writer, sheet_name="Sheet 1")
    writer.save()
    sio.seek(0)
    print(sio)
    workbook = sio.getvalue()
    print(workbook)
    return workbook
