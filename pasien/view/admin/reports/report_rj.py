from pasien import app
from pasien.models.table import Pasien, RawatInap, RawatJalan

from flask import flash, render_template, redirect, url_for, request, make_response
from flask_login import login_required
from sqlalchemy import and_, or_, cast, Date, between
import datetime
import pandas as pd


try:
    from io import BytesIO
except ImportError:
    from cStringIO import StringIO as BytesIO
@login_required
def report_rj():
    if request.method == 'GET':
        rawat_jalan = RawatJalan.query
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        if start_date and end_date:
            rawat_jalan = rawat_jalan.filter(RawatJalan.tanggal.between(start_date, end_date))
        rawat_jalan = rawat_jalan.all()
        return render_template("admin/report/report_rj.html",
                rawat_jalan=rawat_jalan,
                start_date=start_date,
                page_title="Report Data Rawat Jalan",
                icon_img="/static/img/rawat_jalan.png",
                sub_title="Report data pasien rawat jalan",
                end_date=end_date)
@login_required
def export_rj_excel():
    if request.method == 'GET':
        rawat_jalan = RawatJalan.query
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        if start_date and end_date:
            rawat_jalan = rawat_jalan.filter(RawatJalan.tanggal.between(start_date, end_date))
        workbook = create_rj_as_excel(rawat_jalan.all())
        excel = make_response(workbook, 200)
        excel.mimetype = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        return excel
@login_required
def export_rj_pdf():
    if request.method == 'GET':
        rawat_jalan = RawatJalan.query
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        if start_date and end_date:
            rawat_jalan = rawat_jalan.filter(RawatJalan.tanggal.between(start_date, end_date))
        pdf = render_template('admin/report/pdf/report_rj.html',
                rawat_jalan=rawat_jalan.all(),
                start_date=datetime.datetime.strptime(start_date, '%Y-%m-%d'),
                end_date=datetime.datetime.strptime(end_date, '%Y-%m-%d'),
                report_title="Laporan Data Rawat Jalan")
        return pdf
#         # return pdf

def create_rj_as_excel(rawat_jalan):
    nama = []
    no_pasien = []
    tanggal = []
    keluhan = []
    tindakan = []
    diagnosa = []
    sio = BytesIO()
    for p in rawat_jalan:
        nama.append(p.pasien.nama)
        no_pasien.append(p.pasien.no_pasien)
        keluhan.append(p.keluhan)
        tindakan.append(p.tindakan)
        diagnosa.append(p.diagnosa)
        tanggal.append(p.tanggal.strftime('%d-%B-%Y') if p.tanggal else "-")

    df = pd.DataFrame({
        "Nama":nama,
        "No Pasien": no_pasien,
        "Keluhan" : keluhan,
        "Tindakan" : tindakan,
        "Diagnosa" : diagnosa,
        "Tanggal Daftar": tanggal})
    writer = pd.ExcelWriter(sio, engine='xlsxwriter')
    df.to_excel(writer, sheet_name="Sheet 1")
    writer.save()
    sio.seek(0)
    print(sio)
    workbook = sio.getvalue()
    print(workbook)
    return workbook
