from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Jurusan(models.Model):
    _name = 'jurusan'
    _description = 'Data Jurusan'

    name = fields.Char(string="Nama Jurusan")
    siswa_ids= fields.One2many('sekolah', 'jurusan_id', string="Daftar Siswa")
