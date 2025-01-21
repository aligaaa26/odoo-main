# -*- coding: utf-8 -*-
{
    'name': "hotel",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "Liga & Aba",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'App',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        
        'views/hotel_reservasi.xml',
        'views/hotel_pegawai.xml',
        'views/hotel_layanan_laundry.xml',
        'views/hotel_laundry.xml',
        'views/hotel_gym.xml',
        'views/menu_hotel.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'hotel/static/src/js/custom_page.js',  # Path file JS yang ingin ditambahkan
        ],
    },
}

