from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HotelLaundry(models.Model):
    _name = "hotel.laundry"
    _description = "Laundry Hotel"

    def action_check_in(self):
        for record in self:
            record.state = 'check_in'

    def action_check_out(self):
        for record in self:
            record.state = 'check_out'

    def action_cancel(self):
        for record in self:
            record.state = 'canceled'

    @api.depends('nomor_laundry')
    def _compute_display_name(self):
        for record in self:
            record.display_name = record.nomor_laundry or "Unnamed"

    @api.constrains('phone')
    def _check_phone(self):
        for record in self:
            if record.phone and not record.phone.isdigit():
                raise ValidationError("Phone number must contain only digits.")

    def _generate_nomor_laundry(self):
        last_record = self.search([], order='id desc', limit=1)
        if last_record and last_record.nomor_laundry:
            last_number = last_record.nomor_laundry
            if last_number.startswith('DRY-2024-'):
                last_seq = int(last_number.split('-')[-1]) + 1
            else:
                last_seq = 1
        else:
            last_seq = 1
        return f'DRY-2024-{str(last_seq).zfill(5)}'

    @api.model
    def create(self, vals):
        if 'nomor_laundry' not in vals or not vals['nomor_laundry']:
            vals['nomor_laundry'] = self._generate_nomor_laundry()
        record = super(HotelLaundry, self).create(vals)
        # Update display name after creation
        record.display_name = record.nomor_laundry
        return record

    def name_get(self):
        result = []
        for record in self:
            name = record.display_name
            result.append((record.id, name))
        return result

    # Data Pelanggan
    nomor_laundry = fields.Char(string="Nomor laundry", readonly=True)
    display_name = fields.Char(string="Display Name", compute="_compute_display_name", store=True)
    nama_pegawai = fields.Many2one("hotel.pegawai", string="Nama Pegawai")

    # Data laundry
    tanggal_laundry = fields.Datetime(required=True)
    jam_taruh = fields.Datetime(required=True)
    jam_ambil = fields.Datetime(required=True)

    # Notes
    note = fields.Text()

    # Status Bar
    state = fields.Selection([
        ('laundry', 'laundry'),
        ('taruh', 'Taruh'),
        ('ambil', 'Ambil'),
        ('canceled', 'Dibatalkan'),
    ], string='Status', default='laundry')

    # Deskripsi
    deskripsi = fields.Text(String="Deskripsi Layanan")

    # Nama Pelanggan
    nama_pelanggan = fields.Many2one(
        "hotel.reservasi", 
        string="Nama Pelanggan", 
        required=True, 
        ondelete='cascade',
        domain=[('nama', '!=', False)]  # Filter: hanya yang memiliki nama pelanggan
    )

    layanan_laundry_ids = fields.Many2many("hotel.layanan.laundry")