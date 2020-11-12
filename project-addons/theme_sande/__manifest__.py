# -*- coding: utf-8 -*-

{
    'name': 'Theme Sande y Díaz',
    'version': '11.0.0.3.1',
    'summary': 'Theme customization for Sande y Díaz website',
    'description': '',
    'category': 'Theme',
    'author': 'Comunitea',
    'contributors': [
        'Rubén Seijas <ruben@comunitea.com>',
    ],
    'website': 'http://www.comunitea.com',
    "support": "info@comunitea.com",
    'license': 'AGPL-3',
    "price": 0,
    "currency": "EUR",
    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "uninstall_hook": None,
    "auto_install": True,
    'installable': True,
    'application': True,
    'qweb': [],
    "live_test_url": "",
    "demo": [],
    "demo_title": "",
    "demo_addons": [],
    "demo_addons_hidden": [],
    "demo_url": "",
    "demo_summary": "",
    "demo_images": [],
    "external_dependencies": {"python": [], "bin": []},
    'depends': [
        'breadcrumbs_base',
        'muk_website_scroll_up',
        'theme_bootswatch',
        'web_editor',
        'website_sande',
        'website_sale_affix_header',
    ],
    'data': [
        'templates/editor.xml',
        'templates/footer.xml',
        'views/assets.xml',
    ],
    'images': [
        '/static/description/icon.png',
        '/static/description/logo.jpg',
    ],
}
