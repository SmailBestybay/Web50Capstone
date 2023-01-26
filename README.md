# Ourtube

## Distinctiveness and Complexity 

Ourtube is a website that allows it's users to create custom youtube feeds.
Users can choose to follow feeds others have created as well. They can also search for youtube channels from the website. 

I drew inspiration from discord servers or slack channels behavior. 
Although the premise is simple, the execution holds many complexities such as:
- Access youtube data through google's python api client. 
- Create a many to many model relationship that is more precisely controlled with a custom through table.
- Build views that can respond to both sync and async post requests. 

In addition, I used this project to become more deeply familiar with Django's "batteries included" characteristic. I made sure to use and extend Django's built in features such as:
- User authentication and built in authentication views
- Form validation and built in forms
- Template class based views 
- Django messages


On the front end side I made sure to have a structural approach to the styling of the website. I used BEM naming convention alongside SASS, a CSS preprocesor, to assist me with the styling. 

I used JavaScript for minimal DOM manipulation and to make async requests by using the fetch api. 

## What’s contained in each file I created :file_folder:

### Tree structure of files that I created or edited.

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

### Description of each file

- README.md
    - this file. Contains infromation about this project
- capstone/settings.py
    - configuration file 
    - added the ourtube app
    - added django debug toolbar
    - added youtube api info 
    - added Auth views overrides
    - changed auth user model
        - Although the default is all that is needed at this point, I wanted to use my model in case there is a need for more user model features.
- capstone/urls.py
    - included ourtube urls
    - included django debug toolbar urls
    - included django auth urls
    - added an empty path to direct to ourtube app
- ourtube/admin.py
    - registered ourtube model
    - added model admins to customize the admin page
- ourtube/forms.py
    - created custom forms by extending django built in forms
- ourtube/models.py
    - contains django models
    - User model
    - YoutubeChannel model
    - Feed model
    - Membership model, this is a through table for feed users
- ourtube/static/
    - static files such as:
        - scss style files that are semantically split for better organization
        - compiled css file
        - JavaScript files:
            - feedPage.js handles feed page interactivity
            - searchPage.js handles search page interactivity
- ourtube/template/
    - ourtube/
        - html files, also semantically split 
        - base.html is the base html that other files extend
    - registration/
        - html files for Django's built in auth views
- ourtube/urls.py
    - url configuration for the ourtube app
- ourtube/views.py
    - On this project I wanted to learn to use the class based views. 
    - Made use of inheritance to leverage template views
- ourtube/youtube_api_helper.py
    - module that contains you tube api helper functions 


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