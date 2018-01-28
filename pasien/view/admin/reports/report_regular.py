import datetime
import pandas as pd
try:
    from io import BytesIO
except ImportError:
    from cStringIO import StringIO as BytesIO

from flask import flash, render_template, redirect, url_for, request, make_response
from flask_login import login_required
from sqlalchemy import and_, or_, cast, Date, between
from pasien import app
from pasien.models.table import Pasien, Regular


@login_required
def report_regular():
    if request.method == 'GET':
        regular = Regular.query
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        if start_date and end_date:
            regular = regular.filter(Regular.tanggal.between(start_date, end_date))
        regular = regular.all()
        return render_template("admin/report/report_regular.html",
                regular=regular,
                start_date=start_date,
                page_title="Report Data Pelayanan Regular",
                icon_img="/static/img/regular.png",
                sub_title="Report data pasien Regular",
                end_date=end_date)
@login_required
def export_regular_excel():
    if request.method == 'GET':
        regular = Regular.query
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        if start_date and end_date:
            regular = regular.filter(Regular.tanggal.between(start_date, end_date))
        workbook = create_regular_as_excel(regular.all())
        excel = make_response(workbook, 200)
        excel.mimetype = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        return excel
@login_required
def export_regular_pdf():
    if request.method == 'GET':
        regular = Regular.query
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        if start_date and end_date:
            regular = regular.filter(Regular.tanggal.between(start_date, end_date))
        pdf = render_template('admin/report/pdf/report_regular.html',
                regular=regular.all(),
                start_date=datetime.datetime.strptime(start_date, '%Y-%m-%d'),
                end_date=datetime.datetime.strptime(end_date, '%Y-%m-%d'),
                report_title="Laporan Data Pelayanan Regular")
        return pdf
#         # return pdf

def create_regular_as_excel(regular):
    nama = []
    no_pasien = []
    tanggal = []
    keluhan = []
    tindakan = []
    diagnosa = []
    sio = BytesIO()
    for p in regular:
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
