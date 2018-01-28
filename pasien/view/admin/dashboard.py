
from pasien import app
from flask_login import login_required
from flask import render_template, jsonify
from sqlalchemy.sql import func
from pasien.models.table import Pasien, PasienRujukan, RawatInap, RawatJalan
import datetime
import logging


@login_required
def admin_dashboard():
    return render_template("admin/dashboard.html", 
        page_title="Dashboard Admin", 
        icon="dashboard")

def statistik_data():
    pasien = Pasien.query.all()
    rawat_jalan = RawatJalan.query.all()
    rawat_inap = RawatInap.query.all()
    rujukan = PasienRujukan.query.all()
    return jsonify({
        "pasien":len(pasien), 
        "rawat_inap" : len(rawat_inap), 
        "rawat_jalan":len(rawat_jalan),
        "rujukan" : len(rujukan)
        })

def statistik_monthly():
    pasien = Pasien.query
    rawat_jalan = RawatJalan.query
    rawat_inap = RawatInap.query
    rujukan = PasienRujukan.query.join(RawatInap)
    rujukan_mount = []
    rj_mount = []
    ri_mount = []
    pasien_mount = []
    for a in range(1,13):
        rujukan_mount.append(len(rujukan.filter(func.MONTH(RawatInap.tanggal_masuk)==a).all()))
        rj_mount.append(len(rawat_jalan.filter(func.MONTH(RawatJalan.tanggal)==a).all()))
        ri_mount.append(len(rawat_inap.filter(func.MONTH(RawatInap.tanggal_masuk)==a).all()))
        pasien_mount.append(len(pasien.filter(func.MONTH(Pasien.create_at)==a).all()))
    return jsonify({"pasien":pasien_mount, "rujukan":rujukan_mount, "rawat_inap":ri_mount, "rawat_jalan":rj_mount})
