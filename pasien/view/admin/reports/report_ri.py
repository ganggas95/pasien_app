from pasien import app
from pasien.models.table import Pasien, RawatInap

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
def report_ri():
    if request.method == 'GET':
        rawat_inap = RawatInap.query
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        if start_date and end_date:
            rawat_inap = rawat_inap.filter(RawatInap.tanggal_masuk.between(start_date, end_date))
        rawat_inap = rawat_inap.all()
        return render_template("admin/report/report_ri.html",
                rawat_inap=rawat_inap,
                page_title="Report Data Rawat Inap",
                icon_img="/static/img/rawat_inap.png",
                sub_title="Report data pasien rawat inap",
                start_date=start_date,
                end_date=end_date)
@login_required
def export_ri_excel():
    if request.method == 'GET':
        rawat_inap = RawatInap.query
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        if start_date and end_date:
            rawat_inap = rawat_inap.filter(RawatInap.tanggal_masuk.between(start_date, end_date))
        workbook = create_ri_as_excel(rawat_inap.all())
        excel = make_response(workbook, 200)
        excel.mimetype = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        return excel
@login_required
def export_ri_pdf():
    if request.method == 'GET':
        rawat_inap = RawatInap.query
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        if start_date and end_date:
            rawat_inap = rawat_inap.filter(RawatInap.tanggal_masuk.between(start_date, end_date))
        pdf = render_template('admin/report/pdf/report_ri.html',
                rawat_inap=rawat_inap.all(),
                start_date=datetime.datetime.strptime(start_date, '%Y-%m-%d'),
                end_date=datetime.datetime.strptime(end_date, '%Y-%m-%d'),
                report_title="Laporan Data Rawat Inap")
        return pdf
#         # return pdf

def create_ri_as_excel(rawat_inap):
    nama = []
    no_pasien = []
    tanggal_masuk = []
    tanggal_keluar = []
    diagnosa = []
    sio = BytesIO()
    for p in rawat_inap:
        nama.append(p.pasien.nama)
        no_pasien.append(p.pasien.no_pasien)
        tanggal_masuk.append(p.tanggal_masuk.strftime('%d-%B-%Y') if p.tanggal_masuk else "-")
        tanggal_keluar.append(p.tanggal_keluar.strftime('%d-%B-%Y') if p.tanggal_keluar else "-")
        diagnosa.append(p.diagnosa)

    df = pd.DataFrame({
        "Nama":nama,
        "No Pasien": no_pasien,
        "Tanggal Masuk" : tanggal_masuk,
        "Tanggal Keluar" : tanggal_keluar,
        "Diagnosa" : diagnosa})
    writer = pd.ExcelWriter(sio, engine='xlsxwriter')
    df.to_excel(writer, sheet_name="Sheet 1")
    writer.save()
    sio.seek(0)
    print(sio)
    workbook = sio.getvalue()
    print(workbook)
    return workbook
