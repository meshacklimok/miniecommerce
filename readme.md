# MiniEcommerce Django Project


MiniEcommerce is a simple e-commerce web application built with **Django**, allowing users to browse products, manage orders, and make payments through **M-Pesa STK Push** integration. It also includes email notifications and media uploads via Cloudinary.




## Features

- **User Authentication**: Custom user model with registration, login, and profile management.
- **Product Catalog**: Browse products by category, with search and filter options.
- **Shopping Cart**: Add products to cart and manage quantities.
- **Order Management**: Create, view, and track orders.
- **Payment Integration**: M-Pesa STK Push for safe and instant payments.
- **Email Notifications**: Order confirmation emails via Gmail SMTP.
- **Media Management**: Product images handled with Cloudinary.
## Technologies Used

- **Backend**: Python 3.11, Django 4.x
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Database**: SQLite (default, can switch to PostgreSQL)
- **Payment Gateway**: Safaricom M-Pesa (Sandbox for testing)
- **Media Storage**: Cloudinary
- **Environment Management**: python-decouple
- **Ngrok**: To expose local server for M-Pesa callbacks during development

SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost,ngrok-url

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=youremail@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=youremail@gmail.com

# Cloudinary
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# M-Pesa Sandbox
MPESA_CONSUMER_KEY=your_consumer_key
MPESA_CONSUMER_SECRET=your_consumer_secret
MPESA_SHORTCODE=174379
MPESA_PASSKEY=your_passkey
MPESA_BASE_URL=https://sandbox.safaricom.co.ke
MPESA_CALLBACK_URL=https://your-ngrok-url/mpesa/callback/


