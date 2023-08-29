# CATERING

Application for catering services. Built as a school assignment for Software engineering.

Technologies used: Django Web Framework and PostgreSQL database. For styling purposes we have used Tailwind CSS. Web application is hosted on Vercel, and database is hosted on Railway. We have built a CI/CD pipleine to deploy changes automatically on Vercel through Github actions.

Tutorials on how to run app:

* Clone the repo
* Run npm install
* Run npm run build
* Add .env file and add database credentials
* Run python manage.py runserver

Application is run on 127.0.0.1:8000.

Features:

* Login (Validations and Error Messages)
* Register (Validations and Error Messages)
* Dashboard statistics (Dummy data)
* Logout

User:

* My orders (List of my orders)
* See order details
* Track order status
* Pay order
* See order price

Admin:

* Orders (List of all orders with live search)
* Accept Order
* Decline Order
* Complete Order
* See order details
* See storage availability for order
* See Users list
* See Storage list
* Add Storage
* Edit Storage
* Delete Storage (Just to showcase delete option)