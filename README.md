# Django Blog App

## Features

    1. View Blogs
    2. create a blog with the use of CKEditor
    3. CRUD methods, Filter, Search, Comments on Blogs
    3. View, Update, Edit your Profiles
    4. User Password Reset & Password change Feature

### Home View

![Home image](/screenshots/home.png)

### User view

![User Image](/screenshots/user.png)

### Create View

![Blog Create Image](/screenshots/create.png)

---

### **Environment Setup**

`git clone https://github.com/madhumallesh/django-blog-app.git`

` cd django-blog`

_create a virual environment_

`Pip install virtualenv`

` virtualenv env`

_Activate the env (windows)_

`env\Script\activate`

_install the requirements_

`pip install -r requirements.txt`

Run the Migrations for database

` cd website `

` python manage.py makemigrations`

` python manage.py migrate`

_All set_

**Run this command to start the server**

`python manage.py runserver`

---

### to Create a Fake data in database run the following commands..

_to create Users_

` python manage.py createdata --user --n 5`

_to create Tags_

`python manage.py createdata --tags`

_to create Post_

`python manage.py createdata --post --n 30`

_to create Comments (On published posts)_

`python manage.py createdata --comment --n 15`

---

# **Thank You**
