from odoo import fields, models, api

class HotelGym(models.Model):
    _name = "hotel.gym"  #Mengganti nama model untuk Pusat Kebugaraan di Hotel
    _description = "Pusat Kebugaraan di Hotel"

    # Informasi tentang Pusat Kebugaraan di Hotel
    nama_gym = fields.Char("Nama Gym", required=True)  # Nama Pusat Kebugaraan di Hotel

    deskripsi_gym = fields.Text("Deskripsi Gym")  # Deskripsi tambahan tentang gym
    
    biaya_gym = fields.Integer("Biaya Gym", required=True)

    gambar_gym = fields.Binary(string="Gambar Gym")  # Field untuk gambar

    @api.model
    def default_get(self, fields):
        res = super(HotelGym, self).default_get(fields)
        # tambahkan logika lain jika perlu
        return res