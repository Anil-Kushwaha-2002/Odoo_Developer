{
    'name': 'Custom Sales Order Report',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Custom PDF report for Sales Orders with UOM and Invoicing details',
    'description': """
        This module customizes the Sales Order PDF report by adding a UOM column 
        and Invoicing/Shipping address details.
    """,
    'author': 'Aleeza Anjum',
    'website': 'https://www.example.com',
    'depends': ['sale'],
    'data': [
        'views/templates.xml',  # Your custom XML file for the PDF report
    ],
    'installable': True,
    'application': False,
}
