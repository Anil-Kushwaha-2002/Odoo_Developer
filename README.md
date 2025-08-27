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

# MVC (Model-View-Controller)
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

