# Ourtube

Final project for Harvard's Web50.

Ourtube is a webapp that allows it's users to create custom youtube feeds.
Users can choose to follow feeds others have created as well. They can also search for youtube channels from the website. 

Inspired by discord servers or slack channels behavior. 

This project helped me become more deeply familiar with Django's "batteries included" characteristics:
- User authentication and built in authentication views
- Form validation and built in forms
- Template class based views 
- Django messages
- Create a many to many model relationship that is more precisely controlled with a custom through table.

On the front end:
- Used BEM naming convention alongside SASS.
- Built views that can respond to both sync and async post requests. 

## Tree structure of files that were created or edited by me.

```
.
├── README.md
├── capstone
│   ├── settings.py
│   ├── urls.py
├── ourtube
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── static
│   │   └── ourtube
│   │       ├── feedPage.js
│   │       ├── my_sass
│   │       │   ├── _base.scss
│   │       │   ├── _content.scss
│   │       │   ├── _messages.scss
│   │       │   ├── _mixins.scss
│   │       │   ├── _sidebar.scss
│   │       │   └── style.scss
│   │       ├── searchPage.js
│   │       ├── style.css
│   │       └── style.css.map
│   ├── templates
│   │   ├── ourtube
│   │   │   ├── base.html
│   │   │   ├── feed.html
│   │   │   ├── index.html
│   │   │   └── search.html
│   │   └── registration
│   │       ├── login.html
│   │       └── signup.html
│   ├── urls.py
│   ├── views.py
│   └── youtube_api_helper.py
└── requirements.txt
```

## How to run the app :runner:

- Get an [api key](https://developers.google.com/youtube/registering_an_application)  
    - Create `config.py` file at the root of the project and store the key inside as a `youtube_key` variable.
- Install dependencies
```
pip install -r requirements.txt
```

- Make migrations
```
python manage.py makemigrations ourtube
python manage.py migrate
```

- Runserver
```
python manage.py runserver
```
