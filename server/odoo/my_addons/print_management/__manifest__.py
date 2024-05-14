
{
    "name": "Print orders",
    "depends": [
        'base',

    ],
    "data": [
        "security/ir.model.access.csv",
        "data/print_management_data.xml",
        "views/print_order_views.xml",
        "views/print_product_views.xml",
        "views/print_machine_views.xml",
        "views/print_operator_views.xml",
        "views/print_menus.xml",
    ],
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
}