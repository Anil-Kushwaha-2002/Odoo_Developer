{
    "name": " Purchase Order Pdf Report",

    "version": "17.0.0.4",
    "category": "Purchase Order",
    "author": "Oakland",
    "website": "https://www.odooerp.ae",
    "license": "LGPL-3",
    "summary": """This module enables users to print a Purchase Order PDF report typically includes a summary of essential information related to the purchase transactions.""",
    "description": """This module enables users to print a Purchase Order PDF report.""",
    "data": [
        "security/ir.model.access.csv",
        "report/purchase_order_pdf_report.xml",
        "report/purchase_order_pdf_report_template.xml",
        "views/purchase_order_view.xml",
        "views/mode_of_shipment_view.xml",
        "views/res_company_view.xml",
    ],
    "depends": ["purchase", "base", "stock","hr","oe_cust_vend_seq","oe_purchase_order_version"],
    "images": ["static/description/icon.png"],
    "installable": True,
    "auto_install": False,
}
