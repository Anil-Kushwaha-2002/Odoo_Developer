{
    'name': 'My Custom Sales Order',
    'version': '1.0',
    'summary': 'Custom module to handle partial delivery and backorder for sales orders',
    'description': """
        This module customizes the sale order functionality to automatically update 50% 
        of the quantities in the delivery order and creates a backorder for the remaining 
        quantities upon confirmation of the sale order.
    """,
    'author': 'Aleeza Anjum',
    'depends': ['sale', 'stock', 'base'],
    'data': [
        'views/sale_order_views.xml',
    ],
    'installable': True,
}
