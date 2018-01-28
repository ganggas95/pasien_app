
from pasien.helper.url_loader import url_mapper
'''
Auth Endpoint
'''
url_mapper("/admin/login", "view.auth.auth.admin_login", methods=['GET','POST'])
url_mapper("/admin/logout", "view.auth.auth.admin_logout", methods=['GET'])

'''
END AUTH Endpoint
'''
# Dashboard page
url_mapper("/admin/dashboard", "view.admin.dashboard.admin_dashboard", methods=['GET'])

### Register Pasien Page

url_mapper("/admin/pasien/register", "view.admin.data_pasien.register_pasien.register_pasien", methods=['GET', 'POST'])

### Detail Pasien

url_mapper("/admin/pasien/<no_pasien>/detail", "view.admin.data_pasien.register_pasien.detail_pasien", methods=['GET'])

### Detail Pasien PDF

url_mapper("/admin/pasien/<no_pasien>/pdf", "view.admin.data_pasien.register_pasien.pdf_pasien", methods=['GET'])

### Table Pasiens

url_mapper("/admin/pasien/list", "view.admin.data_pasien.data_pasien.all_pasien", methods=['GET'])

### Edit Pasien

url_mapper("/admin/pasien/<id>/edit", "view.admin.data_pasien.data_pasien.edit_pasien", methods=['GET','POST'])

### Hapus Pasien
url_mapper("/admin/pasien/delete", "view.admin.data_pasien.data_pasien.delete_pasien", methods=['POST'])

### Rawat Jalan URL

url_mapper("/admin/pasien/service/<no_pasien>/rawat_jalan", "view.admin.data_pasien.rawat_jalan.form_rawat_jalan", methods=['GET','POST'])

### Rawat Inap URL

url_mapper("/admin/pasien/service/<no_pasien>/rawat_inap", "view.admin.data_pasien.rawat_inap.form_rawat_inap", methods=['GET','POST'])


### Pasien Rujukan URL

url_mapper("/admin/pasien/service/<no_pasien>/rujukan", "view.admin.data_pasien.rujukan.form_rujukan", methods=['GET','POST'])

### Pasien Rujukan URL

url_mapper("/admin/pasien/service/<no_pasien>/regular", "view.admin.data_pasien.regular.form_regular", methods=['GET','POST'])

### Riwayat Pelayanan Pasien

url_mapper("/admin/pasien/<id>/riwayat", "view.admin.data_pasien.pasien_history.history_pasien", methods=['GET','POST'])
url_mapper("/admin/pasien/<id>/riwayat_rj", "view.admin.data_pasien.pasien_history.riwayat_rawat_jalan", methods=['GET'])
url_mapper("/admin/pasien/<id>/riwayat_ri", "view.admin.data_pasien.pasien_history.riwayat_rawat_inap", methods=['GET'])
url_mapper("/admin/pasien/<id>/riwayat_rujukan", "view.admin.data_pasien.pasien_history.riwayat_rawat_rujukan", methods=['GET'])
url_mapper("/admin/pasien/<id>/regular", "view.admin.data_pasien.pasien_history.riwayat_regular", methods=['GET'])


### Report

url_mapper("/admin/report/pasien", "view.admin.reports.report_pasien.report_pasien", methods=['GET'])
url_mapper("/admin/report/rawat_jalan", "view.admin.reports.report_rj.report_rj", methods=['GET'])
url_mapper("/admin/report/rawat_inap", "view.admin.reports.report_ri.report_ri", methods=['GET'])
url_mapper("/admin/report/rujukan", "view.admin.reports.report_rujukan.report_rujukan", methods=['GET'])
url_mapper("/admin/report/regular", "view.admin.reports.report_regular.report_regular", methods=['GET'])


### Export Report

url_mapper("/admin/report/pasien.xlsx", "view.admin.reports.report_pasien.export_pasien_excel", methods=['GET'])
url_mapper("/admin/report/pasien.pdf", "view.admin.reports.report_pasien.export_pasien_pdf", methods=['GET'])

url_mapper("/admin/report/rawat_jalan.xlsx", "view.admin.reports.report_rj.export_rj_excel", methods=['GET'])
url_mapper("/admin/report/rawat_jalan.pdf", "view.admin.reports.report_rj.export_rj_pdf", methods=['GET'])

url_mapper("/admin/report/rawat_inap.xlsx", "view.admin.reports.report_ri.export_ri_excel", methods=['GET'])
url_mapper("/admin/report/rawat_inap.pdf", "view.admin.reports.report_ri.export_ri_pdf", methods=['GET'])

url_mapper("/admin/report/rujukan.xlsx", "view.admin.reports.report_rujukan.export_rujukan_excel", methods=['GET'])
url_mapper("/admin/report/rujukan.pdf", "view.admin.reports.report_rujukan.export_rujukan_pdf", methods=['GET'])

url_mapper("/admin/report/statistik_mounthly", "view.admin.dashboard.statistik_monthly", methods=['GET'])
url_mapper("/admin/report/statistik", "view.admin.dashboard.statistik_data", methods=['GET'])

url_mapper("/admin/report/regular.xlsx", "view.admin.reports.report_regular.export_regular_excel", methods=['GET'])
url_mapper("/admin/report/regular.pdf", "view.admin.reports.report_regular.export_regular_pdf", methods=['GET'])


### User Page

url_mapper("/admin/users", "view.admin.user.users.users", methods=['GET', "POST"])
url_mapper("/admin/users/<int:id>", "view.admin.user.users.user_edit", methods=["POST"])
url_mapper("/admin/users/<int:id>/change_password", "view.admin.user.users.user_edit_password", methods=["POST"])
url_mapper("/admin/users/delete", "view.admin.user.users.user_delete", methods=["POST"])

### Keluarga Page

url_mapper("/admin/keluargas", "view.admin.data_keluarga.keluarga.data_keluarga", methods=['GET', 'POST'])
url_mapper("/admin/keluargas/<int:id>", "view.admin.data_keluarga.keluarga.edit_keluarga", methods=["POST"])
url_mapper("/admin/keluargas/<int:id>/anggota", "view.admin.data_keluarga.keluarga.pasien_keluarga", methods=["GET"])
url_mapper("/admin/keluargas/delete", "view.admin.data_keluarga.keluarga.delete_keluarga", methods=["POST"])
