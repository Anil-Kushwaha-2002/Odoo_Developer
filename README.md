# Odoo_Developer, Oakland Odoo ( OdooERP.ae )
 
# Working flow of an Odoo module
# 1. Module Structure
```
my_module/
│
├── __init__.py                  # Python package initializer; loads models, controllers, reports, etc.
├── __manifest__.py              # Module metadata: name, version, dependencies, data files to load
│
├── models/                      # Business logic & database models
│   ├── __init__.py               # Imports all Python files in models folder
│   ├── models.py                 # Main models with fields, methods, ORM logic
│   └── wizard.py                 # Transient models for wizards (temporary forms)
│
├── controllers/                  # HTTP/Web controllers for routes & custom APIs
│   ├── __init__.py               # Imports all Python files in controllers folder
│   └── main.py                   # Custom routes, portal pages, website controllers
│
├── views/                        # XML views, menus, templates, reports
│   ├── my_model_views.xml         # Form, tree, kanban views for backend models
│   ├── menus.xml                  # Main menu and submenu definitions
│   ├── templates.xml              # QWeb templates for frontend UI rendering
│   ├── wizard_views.xml           # Views for wizard popups (transient models)
│   └── report_templates.xml       # QWeb report templates for PDF/Excel printing
│
├── report/                        # Python files for reports
│   ├── __init__.py                # Imports report scripts
│   └── reports.py                 # Report classes, PDF/Excel report generation
│
├── security/                      # Access controls & security settings
│   ├── ir.model.access.csv         # Defines CRUD permissions for user groups
│   └── security.xml                # Record rules: row-level security for models
│
├── data/                          # Data loaded during installation or demo data
│   ├── data.xml                    # Default records like sequences, configs
│   └── demo.xml                    # Sample/demo data for testing
│
├── static/                         # Static assets: CSS, JS, images, OWL templates
│   ├── description/
│   │   └── icon.png                # Module icon for Odoo Apps store & Apps menu
│   │
│   ├── src/
│   │   ├── css/
│   │   │   └── style.css           # Custom CSS for backend/frontend UI
│   │   ├── js/
│   │   │   ├── main.js             # Vanilla JavaScript for UI enhancements
│   │   │   └── owl_component.js    # OWL (Odoo Web Library) JS components for modern UI
│   │   ├── xml/
│   │   │   └── owl_templates.xml   # OWL component templates in XML
│   │   └── img/
│   │       └── logo.png            # Images for use in module or templates
│   │
│   └── lib/                        # External JS libraries if needed (e.g., Chart.js)
│
├── tests/                          # Unit and integration tests
│   ├── __init__.py                 # Imports test files
│   └── test_my_module.py           # Automated test cases for module features
│
├── wizard/                         # Alternative location for transient models
│   ├── __init__.py                 # Imports wizard models
│   └── wizard.py                   # Wizard classes, transient logic for popup forms
│
├── i18n/                           # Translations for multilingual support
│   ├── en.po                       # English translation file
│   └── hi.po                       # Hindi translation file
│
└── README.md                       # Documentation for module usage & setup
```

### Important File Explanations
- **controllers/main.py** → For web routes, portals, or custom APIs.
- wizard/wizard.py → For transient models used in pop-ups/wizards.
- report/reports.py → For PDF or Excel report generation.
- static/src/css/ → Custom styling for backend/frontend.
- static/src/js/ → JavaScript, including OWL components.
- views/templates.xml → QWeb templates for frontend UI.
- i18n/ → For multilingual support.
- tests/ → For module testing using Odoo test framework.

# 2. Odoo architecture MVC (Model-View-Controller)
- **Model:-** Business logic & DB (Python)
- **View:-** UI (XML)
- **Controller:-** Handles requests, routes (Python)

### Summary Table

| MVC Component  | Odoo Implementation          | Files Location |
| -------------- | ---------------------------- | -------------- |
| Model (M)      | Python Classes (ORM)         | models/        |
| View (V)       | XML Files (Forms, Lists, UI) | views/         |
| Controller (C) | Python Methods / Web Routes  | controllers/   |

### MVC Workflow in Odoo
```
User Action → View (XML) → Controller (Python) → Model (ORM) → Database
                             ↑                            ↓
                          Response <--- Updated Data <--- Database
```
---
---
# 3. Workflow of core Odoo modules
CRM, Sales, Inventory, Purchase, and Accounting

### 1. CRM (Customer Relationship Management)
Purpose: Manage leads, opportunities, and Collect customer interactions.
- Workflow:
```
1. Lead Generation: Leads can come from website, email, phone calls, or manually entered.
   Odoo Action: Go to CRM → Leads → Create.
2. Lead Qualification: Check company info, contact details, interest; Assign salesperson; qualify lead to opportunity.
   Odoo Action: Click Mark as Qualified → Lead becomes an Opportunity.
3. Opportunity Management: Track stages (New, Qualified, Proposal, Won/Lost).
   Odoo Action: Open an opportunity → Add Activities → Move through stages in Kanban view.
4. Communication & Follow-ups: Schedule meetings, calls, emails, Log notes about every interaction.
   Odoo Actions: to remind team members of follow-ups.
5. Quotation & Negotiation: Qualified opportunity can be converted into a Sales Order in Sales module.
   Odoo Action: Click Create Quotation from opportunity → Send to customer → Wait for confirmation.
6. Closing the Deal: Finalize sale and move opportunity to completion; Won:- Opportunity converted into Sales Order → Invoice → Delivery; Lost:- Reason documented for reporting and analysis.
   Odoo Action: Click Mark as Won or Mark as Lost.
7. Reporting & Analytics: Monitor sales performance and pipeline health.
```
- Integration: 
```
CRM → Sales (when opportunity becomes order).
```
✅ **Lead → Qualification → Opportunity → Activities/Follow-ups → Quotation → Won/Lost → Reporting**

### 2. Sales
Purpose: Manage quotations, sales orders, pricing, and customer invoicing.
- Workflow:
```
1. Quotation: Create quote for customer (based on CRM opportunity or manually).
2. Order Confirmation: Customer confirms → quotation becomes Sales Order.
3. Stock Reservation: Sales Order triggers stock check in Inventory.
4. Delivery: Inventory module manages delivery/stock movement.
5. Invoicing: After delivery, Accounting generates invoice.
6. Payment: Customer pays → payment reconciled in Accounting.
```
- Integration:
```
Sales ↔ Inventory (stock availability, delivery).
Sales ↔ Accounting (invoice & payment).
```
✅ **Quotation → Sales Order → Stock check → Delivery → Invoice → Payment → Reporting**

### 3. Inventory (Stock Management)
Purpose: Manage stock levels, warehouse, incoming/outgoing shipments.
- Workflow:
```
1. Stock Tracking: Products tracked with quantity, lot, serial number.
2. Incoming Shipments: Triggered by Purchase Orders → receive goods.
3. Outgoing Shipments: Triggered by Sales Orders → deliver products.
4. Internal Transfers: Between warehouses or locations.
5. Automated Reordering: Based on minimum stock rules.
```
Integration:
```
Inventory ↔ Purchase (incoming goods).
Inventory ↔ Sales (delivery of orders).
```
✅ **Purchase/Manufacturing → Product Receipt → Stock Move → Delivery Order → Inventory Valuation → Reporting**

### 4. Purchase
Purpose: Manage procurement of goods and vendor management.
- Workflow:
```
1. Request for Quotation (RFQ): Create RFQ to vendors.
2. Vendor Confirmation: Vendor confirms → Purchase Order is created.
3. Goods Receipt: Inventory receives products → updates stock.
4. Vendor Bills: Accounting creates bills based on Purchase Order.
5. Payment: Pay vendor → reconciled in Accounting.
```
Integration:
```
Purchase ↔ Inventory (receive goods, update stock).
Purchase ↔ Accounting (vendor bills & payments).
```
✅ **Purchase Requisition → Request for Quotation (RFQ) → Purchase Order → Product Receipt → Vendor Bill → Payment → Reporting**

### 5. Accounting
Purpose: Manage invoices, bills, payments, journals, taxes, and reports.
- Workflow:
```
1. Customer Invoices: Generated from Sales Orders or manually.
2. Customer Payments: Record payments → reconcile with invoice.
3. Vendor Bills: Generated from Purchase Orders or manually.
4. Vendor Payments: Record payments to vendors.
5. Journals & Reports: Generate profit/loss, balance sheet, cash flow.
6. Tax Management: Automatically compute taxes based on transactions.
```
Integration:
```
Accounting ↔ Sales (invoice & payments).
Accounting ↔ Purchase (vendor bills & payments).
```
✅ **Invoice/Bill → Journal Entry → Payment → Reconciliation → Financial Report → Tax Filing → Reporting**

---
---

### 6. Manufacturing (MRP) Workflow
- Bill of Materials (BoM), work orders, production planning, costing.
- Product Demand (Sales Order) → Bill of Materials (BoM) → Work Order → Production → Quality Check → Finished Product → Reporting

### 7. HR Recruitment Workflow
- Recruitment (Job positions, applications, hiring)
- Job Posting → Applications → Screening → Interview → Offer → Onboarding → Reporting

### 8. Project Management Workflow
- Task management, planning, project timesheets, milestones.
- Project Creation → Task Assignment → Work Execution → Timesheets → Review → Completion → Reporting

### 9. Website & eCommerce Workflow
- Website builder, eCommerce shop, product catalog, customer portal.
- Product Publish → Customer Order → Payment → Delivery → Invoice → Feedback → Reporting

### 10. Helpdesk Workflow
- Customer support tickets, SLA policies, knowledge base.
- Ticket Creation → Assignment → Investigation → Resolution → Customer Feedback → Reporting
  
---
---
### 11. Marketing
- Email Marketing, SMS Marketing, Social Marketing, Marketing Automation, Events.

### 12. Timesheets
- Employee timesheets, project task tracking, billing.

### 13. Fleet
- Vehicle management, contracts, fuel, odometer, costs.

### 14. Documents
- Document management system (DMS), versioning, access rights.

### 15. Studio
- Low-code/no-code customization tool to create apps and automate workflows without coding.
  
### 10. Point of Sale (POS)
- Retail sales, barcodes, restaurant orders, receipts, and payments.

### Typical End-to-End Workflow
```
Lead (CRM) 
   ↓
Opportunity (CRM) 
   ↓
Quotation / Sales Order (Sales) 
   ↓
Check Stock (Inventory) → Deliver Product (Inventory)
   ↓
Invoice Customer (Accounting)
   ↓
Receive Payment (Accounting)
```
### Procurement side (if stock is insufficient):
```
Purchase Order (Purchase) 
   ↓
Receive Goods (Inventory) 
   ↓
Pay Vendor (Accounting)
```
# Interconnections Summary
| Module     | Interacts With        | Trigger / Dependency                           |
| ---------- | --------------------- | ---------------------------------------------- |
| CRM        | Sales                 | Opportunity → Sales Order                      |
| Sales      | Inventory, Accounting | Order → Check Stock, Deliver, Invoice Customer |
| Inventory  | Sales, Purchase       | Stock movements, Reorder rules                 |
| Purchase   | Inventory, Accounting | Purchase Order → Goods Receipt → Vendor Bill   |
| Accounting | Sales, Purchase       | Invoice / Payment reconciliation               |
---
---

# Basic Odoo Questions
```base
Q1. How to create a new Odoo module ?
1. Create folder structure (__init__.py, __manifest__.py, models, views).
2. Define models in Python.
3. Define views in XML.
4. Add security rules.
5. Install module via Apps.


# Models & ORM
Q3. Common Odoo ORM methods ?
A: create(), search(), write(), unlink(), browse(), read()

Q4. How to create One2many and Many2one relations?
department_id = fields.Many2one('hr.department')
employee_ids = fields.One2many('hr.employee', 'department_id')

Q5. Difference between search() and browse() ?
search() → Returns recordset IDs based on conditions.
browse() → Access records by IDs.


# Views & UI
Q6. How to add a field in a form view?
A: Add <field name="field_name"/> in XML view file.

Q7. Types of inheritance in Odoo?
1. Model: _inherit = 'model.name'
2. Classical: _name with _inherit
3. View : Using <xpath> in XML.

Q8. How to hide a field dynamically?
A: Use attrs in XML:
<field name="salary" attrs="{'invisible':[('is_manager','=',False)]}"/>


# Security & Access
Q9. How to restrict user access ?
A: Using ir.model.access.csv for CRUD rights and record rules for record-level security.

Q10. Difference between Groups and Access Control ?
Groups: Define user roles.
Access Control: CRUD permissions per model.


# Miscellaneous
Q11. What are Transient and Abstract models ?
TransientModel: Temporary data, auto-deleted (e.g., wizards).
AbstractModel: For reusable logic; not linked to DB tables.

Q12. How to improve performance in Odoo  ?
1. Use sudo() carefully.
2. Limit search() results with limit.
3. Use computed & stored fields properly.
4. Enable caching for static data.

Q13. How to debug in Odoo ?
Use pdb, print(), logger, or --dev=all mode.


# API & Controllers
Q14. How to create REST APIs in Odoo?
A: Use  @http.route() in controllers to expose endpoints.
  @http.route('/get/employees', type='json', auth='user')
  def get_employees(self):
      employees = request.env['hr.employee'].search([])
      return employees.read(['name','department_id'])


Q15. How to call Odoo API externally / API integration ?
A: APIs for external integration. JSON-RPC uses JSON, XML-RPC uses XML format.

Q16. How to integrate Odoo with third-party APIs?
A: Use Python requests or Odoo http library; process data in controllers/models.
```

---
---
# Odoo Razorpay Payment Integration
### 1. Prerequisites
```
1. Odoo Installed (v14+ recommended).
2. Razorpay Account → https://razorpay.com
  → Get Key ID & Key Secret from Dashboard → Settings → API Keys.
3. Python Library:- `pip install razorpay`
4. Create a Custom Odoo Module → We'll add Razorpay integration code inside. Like ( razorpay_integration/)
```
### 2. Overall Flow in Odoo
```
Odoo Sales Order → User Clicks "Pay Now" → Razorpay Checkout → Payment Success/Failure → Odoo Updates Invoice & Payment Status
```
### 3. Integration Steps
```
Step 1:- Store Razorpay Keys in Odoo
- Go to Settings → Technical → System Parameters
- Add:
-  razorpay_key_id 
-  razorpay_key_secret
We will fetch them from the backend using ir.config_parameter.

Step 2:- Add Payment Button on Sales Order, Backend Logic and Checkout Page
Payment Button:- views/sale_order_view.xml
Backend Logic:- models/sale_order.py
Controller:- controllers/main.py

Add a new field for storing Razorpay order id:
razorpay_order_id = fields.Char(string="Razorpay Order ID")

Step 3:- Create Payment Success Callback
Razorpay will send a payment success/failure callback to your endpoint.
- Verify signature using Razorpay SDK.
- Mark invoice as paid on success.
```
### Odoo Integration Flow
```base
Model (Python method) → requests library → Third-party API → Process response → Save in Odoo
```

---
---
# Frequently Asked Questions on Odoo API Integration
Call a third-party REST API to fetch data (e.g., weather, payment gateway, shipping info) and store it in Odoo.
## 1. Basics

**Q1. What is third-party API integration in Odoo?**  
**A:** Connecting Odoo to external services (payments, shipping, SMS, ERP, etc.) using REST, JSON-RPC, or XML-RPC.

**Q2. Which Python library is used for API calls?**  
**A:** `requests` (most common), `json` for parsing responses, `razorpay` for payment integration.

---

## 2. Payment Gateway
**Q3. How to integrate Razorpay/PayPal/Stripe?**  
**A:**  
1. Get API keys from provider.  
2. Store keys in Odoo System Parameters.  
3. Add **“Pay Now”** button on sales/invoice.  
4. Use model method + requests or SDK to create payment order.  
5. Use controller for checkout & callback.  
6. Verify payment & update invoice status.

**Q4. How to handle payment success/failure?**  
**A:** Use webhooks or controller callback; verify signature; update invoice/payment record accordingly.

---

## 3. REST API Integration

**Q5. How to expose Odoo data to external apps?**  
**A:** Use `@http.route()` with `type='json'` or `type='http'` in a controller.

**Q6. How to consume external APIs in Odoo?**  
**A:** Use Python `requests.get()` / `requests.post()` in model or controller; parse JSON/XML response; store in Odoo.

**Q7. Difference between JSON-RPC and REST API?**  
**A:** JSON-RPC is Odoo-native for ORM calls; REST is standard HTTP API for external apps.

---

## 4. Real-Time / Practical Scenarios

**Q8. How to integrate SMS or email gateway?**  
**A:** Use `requests.post()` to send payload to provider; save status in Odoo model for logging.

**Q9. How to sync products/customers with external ERP?**  
**A:**  
1. Schedule cron jobs to fetch/update data periodically.  
2. Use API endpoints with authentication.  
3. Map external fields to Odoo fields.

**Q10. How to ensure secure API integration?**  
**A:**  
1. Use API keys or OAuth.  
2. HTTPS requests only.  
3. Verify signatures/webhooks.  
4. Store sensitive data in System Parameters, not code.

---

## 5. Troubleshooting / Best Practices

**Q11. How to debug API integration issues?**  
**A:**  
1. Log request/response using `_logger.info`.  
2. Check HTTP status codes.  
3. Test in provider’s sandbox mode.

**Q12. How to improve performance?**  
**A:**  
1. Use `sudo()` carefully.  
2. Limit search results.  
3. Avoid unnecessary API calls; batch updates if possible.

---
