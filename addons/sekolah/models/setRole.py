from odoo import models, api

class ResUsers(models.Model):
    _inherit = "res.users"

    @api.model
    def create(self,values):

        user = super(ResUsers,self).create(values)

        group_guru_sekolah = self.env.ref("tes_ubig.group_guru_sekolah")


        if group_guru_sekolah:
            user.write({'groups_id':[(4,group_guru_sekolah.id)]})

        return user