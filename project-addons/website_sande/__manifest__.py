# -*- coding: utf-8 -*-

{
    'name': 'Website Sande y Díaz',
    'version': '11.0.6.0.2',
    'summary': 'Website Customization',
    'description': '',
    'category': 'Website',
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
    "auto_install": False,
    'installable': True,
    'application': False,
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
        'portal',
        'website',
        'website_crm',
        'website_crm_privacy_policy',
        'website_cookie_notice',
        'website_legal_page',
        'website_hr_recruitment',
        'website_hr_recruitment_legal',
        'website_menu_by_user_status',
        'website_sale',
        'website_slides',
        # Comunitea
        'seo_base',
        'follow_us_base',
        'ecommerce_base',
        'website_blog_base',
    ],
    'data': [
        'data/website_data.xml',
        'data/menu_data.xml',
        'data/page_data.xml',
        'templates/contactus.xml',
        'templates/cookies.xml',
        'templates/footer.xml',
        'templates/header.xml',
        'templates/our_company.xml',
        'templates/pumping_systems.xml',
        'templates/quality_policy.xml',
        'templates/legal_advice.xml',
        'templates/legal_terms.xml',
        'templates/legal_privacy.xml',
        'templates/work_with_us.xml',
        'templates/homepage.xml',
        'templates/recruitment.xml',
        'templates/pages.xml',
    ],
    'images': [
        '/static/description/icon.png',
    ],
}
