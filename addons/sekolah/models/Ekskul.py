from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Ekskul(models.Model):
    _name = 'ekskul'
    _description = 'Data Ekskul'

    name = fields.Char(string="Nama Ekskul")
    siswa_ids= fields.Many2many('sekolah', string="Daftar Siswa")
