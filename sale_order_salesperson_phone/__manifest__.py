# -*- coding: utf-8 -*-
{
    'name': "sale order salesperson phone",

    'summary': """
	Add salesperson phone number to the sales order document""",

    'description': """
	Add the salesperson phone number to the printed sales order document.
    """,

    'author': "zvERP",
    'website': "https://www.zverp.com",

    'category': 'Uncategorized',
    'version': '16.0.1.0',
    'license': 'AGPL-3',

    'depends': ['base', 'hr', 'sale'],

    'data': [
        'views/views.xml',
    ],
}
