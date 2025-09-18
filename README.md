📦 Inventory Management System

An **Inventory Management System** built with **Django** (backend) and **HTML/CSS/JS** (frontend) to manage products, purchases, and sales with features like billing, reports, and role-based access.

Features

* 🔑 **User Authentication** (Register, Login, Logout)
* 📦 **Product Management** (Add, Update, Delete, List products)
**Sales Module**

  * Create Bill & Invoice
  * Track Sales History
**Purchase Module**

  * Record Purchases
  * Track Supplier details
**Reports**

  * Total Products, Sales, Purchases
  * Revenue & Expenses Overview
**Dashboard with Sidebar Navigation**

🛠️ Tech Stack

* **Backend**: Django (Python)
* **Frontend**: HTML, CSS, JavaScript
* **Database**: SQLite (default) 
* **Icons**: Font Awesome


## 📂 Project Structure

INVENTORY_SYSTEM/
│── inventory/                   # Main Django app
│   ├── migrations/              # Database migrations
│   ├── templates/inventory/     # HTML templates
│   │   ├── about.html
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── home.html
│   │   ├── invoice.html
│   │   ├── login.html
│   │   ├── product_confirm_delete.html
│   │   ├── product_form.html
│   │   ├── product_list.html
│   │   ├── purchase_list.html
│   │   ├── register.html
│   │   ├── reports.html
│   │   ├── sales_list.html
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│
│── inventory_system/            # Django project config
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│
│── media/                       # Uploaded files
│── static/                      # Static files (CSS, Images)
│   
│
│── db.sqlite3                   # SQLite database
│── manage.py                    # Django management script
│── README.md


## ⚙️ Installation & Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/inventory-system.git
   cd inventory-system
   ```

2. **Create and activate virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate   # For Linux/Mac
   venv\Scripts\activate      # For Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the server**

   ```bash
   python manage.py runserver
   ```

7. Open in browser:

   ```
   http://127.0.0.1:8000/
   ```


## 📸 Screenshots
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/de3efffc-65dc-43c3-9e5a-90f99bbab823" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/598808de-93d1-4baf-980b-52bf07cfe59a" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/75c0e821-a5f4-49d9-8818-695d7f4128d3" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/f7307fb0-37d7-489e-ad49-cb61a27cc080" />
<img width="452" height="808" alt="image" src="https://github.com/user-attachments/assets/f7f7f596-f8bc-467a-bb95-80bc9e986a3f" />


## ✅ Future Enhancements

* ✅ Export reports (Excel/PDF)
* ✅ Integrate barcode scanning
* ✅ Add role-based access (Admin, Staff, Viewer)
* ✅ REST API with Django REST Framework


## 🤝 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature-name`)
3. Commit changes (`git commit -m "Added feature"`)
4. Push to branch (`git push origin feature-name`)
5. Create a Pull Request


## 📜 License

This project is licensed under the **MIT License**.


