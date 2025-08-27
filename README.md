# Odoo_Developer, Oakland Odoo ( OdooERP.ae )
 
# Working flow of an Odoo module
### 1. Module Structure
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

# 2. MVC (Model-View-Controller)
### Models (M) (Business Logic)
- Represents business logic and database structure.
- Defined in Python classes. Extend models.Model.
- Define fields, methods, constraints.
### Workflow:
- ORM maps the class to a database table.
- CRUD operations (Create, Read, Update, Delete) can be performed via models.
- Methods handle business logic and automated actions.

### Views (V) (User Interface)
- Represents business logic and database structure.
- Defined in XML files inside the views/ folder. Linked to models.
- **Types of views:-** Form (data entry),  Tree (list view), Kanban (card view), Search (filters)
### Workflow:
- User interacts with the form/list → sends requests to Controller → Model updates DB.
- Users interact with data through the UI.
- UI sends requests to ORM to fetch or update data.
- ORM updates the database automatically.

### Controller (C)
- Connects View and Model.
- Standard ORM Controllers → Automatic handling for forms, lists.
- Custom Web Controllers → For website, APIs, or custom endpoints.

### MVC Workflow in Odoo
```
User Action → View (XML) → Controller (Python) → Model (ORM) → Database
                             ↑                            ↓
                          Response <--- Updated Data <--- Database
```
### Summary Table

| MVC Component  | Odoo Implementation          | Files Location |
| -------------- | ---------------------------- | -------------- |
| Model (M)      | Python Classes (ORM)         | models/        |
| View (V)       | XML Files (Forms, Lists, UI) | views/         |
| Controller (C) | Python Methods / Web Routes  | controllers/   |

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

