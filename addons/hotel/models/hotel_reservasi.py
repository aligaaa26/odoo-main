from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HotelReservasi(models.Model):
    _name = "hotel.reservasi"
    _description = "Reservasi Hotel"

    def action_check_in(self):
        for record in self:
            record.state = 'check_in'

    def action_check_out(self):
        for record in self:
            record.state = 'check_out'

    def action_cancel(self):
        for record in self:
            record.state = 'canceled'

    @api.depends('nomor_reservasi')
    def _compute_display_name(self):
        for record in self:
            record.display_name = record.nomor_reservasi or "Unnamed"

    @api.constrains('phone')
    def _check_phone(self):
        for record in self:
            if record.phone and not record.phone.isdigit():
                raise ValidationError("Phone number must contain only digits.")

    def _generate_nomor_reservasi(self):
        last_record = self.search([], order='id desc', limit=1)
        if last_record and last_record.nomor_reservasi:
            last_number = last_record.nomor_reservasi
            if last_number.startswith('HR-2024-'):
                last_seq = int(last_number.split('-')[-1]) + 1
            else:
                last_seq = 1
        else:
            last_seq = 1
        return f'HR-2024-{str(last_seq).zfill(5)}'

    @api.model
    def create(self, vals):
        if 'nomor_reservasi' not in vals or not vals['nomor_reservasi']:
            vals['nomor_reservasi'] = self._generate_nomor_reservasi()
        record = super(HotelReservasi, self).create(vals)
        # Update display name after creation
        record.display_name = record.nomor_reservasi
        return record

    def name_get(self):
        result = []
        for record in self:
            name = record.display_name
            result.append((record.id, name))
        return result

    # Data Pelanggan
    nomor_reservasi = fields.Char(string="Nomor Reservasi", readonly=True)
    display_name = fields.Char(string="Display Name", compute="_compute_display_name", store=True)
    nama = fields.Many2one(
        "res.partner", 
        string="Nama", 
        required=True, 
        ondelete='cascade', 
        domain=[('category_id.name', '=', 'Customer')]  # Filter partner dengan tag 'Customer'
    )
    alamat = fields.Char(related="nama.street", string="Alamat", readonly=True)
    gender = fields.Selection(
        selection=[("Laki-Laki", "Laki-Laki"), ("Perempuan", "Perempuan")],
        string="Gender",
        required=True,
    )
    umur = fields.Char(string="Umur", required=True)
    phone = fields.Char(related='nama.phone', string="Phone", readonly=True)
    email = fields.Char(related='nama.email', string="Email", readonly=True)
    dokumen_id = fields.Selection(
        selection=[("KTP", "KTP"), ("Pasport", "Pasport")],
        string="Dokumen ID",
        required=True,
    )
    nomor_id = fields.Char(string="Nomor ID", required=True)

    # Data Reservasi
    tanggal_reservasi = fields.Datetime(required=True)
    checkin = fields.Datetime(required=True)
    checkout = fields.Datetime(required=True)

    # Notes
    note = fields.Text()

    # Status Bar
    state = fields.Selection([
        ('reservasi', 'Reservasi'),
        ('check_in', 'Check In'),
        ('check_out', 'Check Out'),
        ('canceled', 'Dibatalkan'),
    ], string='Status', default='reservasi')