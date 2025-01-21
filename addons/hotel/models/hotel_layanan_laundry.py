from odoo import fields, models, api

class HotelLayananLaundry(models.Model):
    _name = "hotel.layanan.laundry"  # Mengganti nama model untuk layanan laundry
    _description = "Layanan Laundry"

    # Informasi tentang layanan Laundry
    nama_layanan = fields.Char("Nama Layanan", required=True)  # Nama layanan laundry

    deskripsi_layanan = fields.Text("Deskripsi Layanan")  # Deskripsi tambahan tentang layanan
    
    biaya_layanan = fields.Integer("Biaya layanan", required=True)