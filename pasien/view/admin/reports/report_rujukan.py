from pasien import app
from pasien.models.table import Pasien, RawatInap, PasienRujukan

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
def report_rujukan():
    if request.method == 'GET':
        rujukan = PasienRujukan.query.join(RawatInap)
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        if start_date and end_date:
            rujukan = rujukan.filter(RawatInap.tanggal_masuk.between(start_date, end_date))
        rujukan = rujukan.all()
        return render_template("admin/report/report_rujukan.html",
                rujukan=rujukan,
                page_title="Report Data Pasien Rujukan",
                icon_img="/static/img/rujukan.png",
                sub_title="Report data pasien rujukan",
                start_date=start_date,
                end_date=end_date)
@login_required
def export_rujukan_excel():
    if request.method == 'GET':
        rujukan = PasienRujukan.query.join(RawatInap)
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        if start_date and end_date:
            rujukan = rujukan.filter(RawatInap.tanggal_masuk.between(start_date, end_date))
        workbook = create_rujukan_as_excel(rujukan.all())
        excel = make_response(workbook, 200)
        excel.mimetype = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        return excel

@login_required
def export_rujukan_pdf():
    if request.method == 'GET':
        rujukan = PasienRujukan.query.join(RawatInap)
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        if start_date and end_date:
            rujukan = rujukan.filter(RawatInap.tanggal_masuk.between(start_date, end_date))
        return render_template('admin/report/pdf/report_rujukan.html',
                rujukan=rujukan.all(),
                start_date=datetime.datetime.strptime(start_date, '%Y-%m-%d'),
                end_date=datetime.datetime.strptime(end_date, '%Y-%m-%d'),
                report_title="Laporan Data Pasien Rujukan")
#         return render_pdf(HTML(string=pdf), stylesheets=None)
#         # return pdf

def create_rujukan_as_excel(rujukan):
    nama = []
    no_pasien = []
    asal = []
    keterangan = []
    tanggal_masuk = []
    tanggal_keluar = []
    diagnosa = []
    sio = BytesIO()
    for p in rujukan:
        nama.append(p.pasien.nama)
        no_pasien.append(p.pasien.no_pasien)
        tanggal_masuk.append(p.rawat_inap.tanggal_masuk.strftime('%d-%B-%Y') if p.tanggal_masuk else "-")
        tanggal_keluar.append(p.rawat_inap.tanggal_keluar.strftime('%d-%B-%Y') if p.tanggal_keluar else "-")
        diagnosa.append(p.diagnosa)
        asal.append(p.asal)
        keterangan.append(p.keterangan)
    df = pd.DataFrame({
        "Nama":nama,
        "No Pasien": no_pasien,
        "Asal" : asal,
        "Keterangan" : keterangan,
        "Tanggal Masuk" : tanggal_masuk,
        "Tanggal Keluar" : tanggal_keluar,
        "Diagnosa" : diagnosa})
    writer = pd.ExcelWriter(sio, engine='xlsxwriter')
    df.to_excel(writer, sheet_name="Sheet 1")
    writer.save()
    sio.seek(0)
    workbook = sio.getvalue()
    return workbook
