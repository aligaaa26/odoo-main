from odoo import models, fields, api

class HotelPegawai(models.Model):
    _name = 'hotel.pegawai'
    _description = 'Model untuk Pegawai Hotel'

    @api.depends('nama_pegawai')
    def _compute_name(self):
        for record in self:
            if record.nama_pegawai:
                record.name = f"{record.nama_pegawai.name}"
            else:
                record.name = "Unnamed"

    def name_get(self):
        result = []
        for record in self:
            # Nama yang ditampilkan lebih jelas
            name = f"{record.nama_pegawai.name} ({record.jenis_pegawai or 'Jenis Tidak Ditentukan'})"
            result.append((record.id, name))
        return result

    @api.model
    def create(self, vals):
        # Cek apakah 'nama_pegawai' ada dalam vals dan tidak kosong
        if not vals.get('nama_pegawai'):
            raise UserError("Nama Pegawai harus diisi sebelum menyimpan.")
        return super(HotelPegawai, self).create(vals)

    # Mengubah nama_pasien menjadi nama_pegawai
    nama_pegawai = fields.Many2one(
        "res.partner", 
        string="Nama Pegawai", 
        required=True, 
        ondelete='cascade', 
        domain=[('category_id.name', '=', 'Pegawai')]  # Filter partner dengan tag 'Employee'
    )
    alamat = fields.Char(related="nama_pegawai.street", string="Alamat", readonly=True)
    gender = fields.Selection(
        selection=[("Laki-Laki", "Laki-Laki"), ("Perempuan", "Perempuan")],
        string="Gender",
        required=True,
    )
    phone = fields.Char(related='nama_pegawai.phone', string="Phone", readonly=True)
    email = fields.Char(related='nama_pegawai.email', string="Email", readonly=True)
    jenis_pegawai = fields.Selection(
        selection=[("Customer Service", "Customer Service"), ("Cleaning Service", "Cleaning Service"), ("Koki", "Koki"), ("Pelayan Hotel", "Pelayan Hotel")],
        string="Jenis Pegawai",
        required=True,
    )
    name = fields.Char("Nama Pegawai", compute="_compute_name", store=True)
    note = fields.Text()