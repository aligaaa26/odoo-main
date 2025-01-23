import json
import requests

from odoo import http

class Sekolah(http.Controller):
    @http.route('/tes', auth="public")
    def tes(self, **kw):
        return "All Works"
    
    @http.route('/accesscheck2', auth="user")
    def checkaccess2(self, **kw):
        return "This Is Only For User"
    
    @http.route('/api', auth="public")
    def api(self, **kw):
        response = requests.get("https://catfact.ninja/fact")
        return json.dumps(response.json())