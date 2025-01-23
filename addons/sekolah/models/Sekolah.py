from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging
from datetime import datetime

_logger = logging.getLogger(__name__)

class Sekolah(models.Model):
    _name = 'sekolah'
    _description = 'Data Sekolah'


    _sql_constraints = [
        ('unique_nis', 'UNIQUE(nis)', 'Nis Tidak Boleh Sama')
    ]

    name = fields.Char(required=True, string="Nama Siswa")
    nis =  fields.Integer(required=True, string="NIS Siswa")
    kelas = fields.Char(string="Kelas")
    absen = fields.Integer(string="No Absen")
    alamat = fields.Char(string="Alamat")
    nama_ayah = fields.Char(string="Nama Ayah")
    nama_ibu = fields.Char(string="Nama Ibu")
    deskripsi = fields.Text(string="Deskripsi")
    ipa = fields.Integer(string="Nilai IPA")
    ips = fields.Integer(string="Nilai IPS")
    rata_rata = fields.Integer(string="Rata Rata", readonly=True, compute='_compute_rata_rata', store=True)

    foto = fields.Binary(string="Foto Siswa", required=True, attachment=True)
    umur = fields.Integer(string="Umur Siswa")


    parent_id= fields.Many2one('res.partner', string="Wali", required=True)
    phone = fields.Char(related='parent_id.phone', string="Nomor Telepon", readonly=True)
    
    jurusan_id= fields.Many2one('jurusan', string="Jurusan", required=True)
    ekskul_id= fields.Many2many('ekskul', string="Ekskul", required=True)

    gender = fields.Selection([
        ('laki-laki', 'Laki-Laki'),
        ('perempuan', 'Perempuan'),
    ], string="Jenis Kelamin", required=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('batal', 'Batal'),
        ('valid', 'Valid'),
    ], string="Status", default='draft', readonly=True)


    def action_valid(self):
        return self.write({'state': 'valid'})
    def action_batal(self):
        return self.write({'state': 'batal'})



    @api.depends('ipa', 'ips')
    def _compute_rata_rata(self):
        for record in self:
            if record.ipa and record.ips:
                record.rata_rata = (record.ipa + record.ips)/2
            else:
                record.rata_rata = 0.0



    @api.constrains('absen')
    def _check_absen(self):
        for record in self:
            if record.absen < 1:
                raise ValidationError('Absen Harus Lebih Besar Dari 0')

    def send_email(self):
        for record in self:
            # Membuat isi email
            subject = f"Informasi Siswa: {record.name}"
            body = f"""
            Nama Siswa: {record.name}
            NIS: {record.nis}
            Kelas: {record.kelas}
            Absen: {record.absen}
            Nilai IPA: {record.ipa}
            Nilai IPS: {record.ips}
            Rata-rata Nilai: {record.rata_rata}
            """
            
            # Menyiapkan email
            mail_values = {
                'subject': subject,
                'body_html': body,
                'email_to': "azrulaldo87@gmail.com",  # Mengirim email ke wali
            }
            
            # Mengirim email
            mail = self.env['mail.mail'].create(mail_values)
            mail.send()
            return True
        
    def auto_validate_data(self):
        records = self.search([('state', '=', 'draft')])
        for record in records:
            record.action_valid()
        _logger.info("Auto validate completed at %s" % datetime.now())




