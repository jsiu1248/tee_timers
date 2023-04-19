# Tee Timers

[Tee Timers](https://teetimers.herokuapp.com/) is your one-stop website to view find potential golf partners, message them, and play a round to see if you guyys are compatible. You can find all of these features on Tee Timers. Be sure to register for an account today, and never golf with random strangers or alone again!

# Table of Contents
[Installation](#installation)

[Usage](#usage)

[Data](#data)

[Features](#features)

[Migrations](#migrations)

[Send Emails](#send-emails)

[Environment Variables](#environment-variables)

[Future Features](#future-features)

[Contributing](#contributing)




## Installation

It is  recommended to install requirements in a virtual environment (venv).
```bash
python3 -m venv venv
. venv/bin/activate
```
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Tee Timers requirements.

```bash
pip install -r requirements/common.txt
```

## Usage
To start using the app, open a ```flask shell``` session:
```bash
export FLASK_APP=golf_app.py
flask shell
```

This creates the tables and loads all of the tables. The functions loads the new data, inserts  (any new data, skips existing rows), and updates existing rows. 
```shell
>>> db.create_all()
>>> State.insert_state()
>>> City.insert_city()
>>> GolfCourse.insert_golf_course()
>>> Day.insert_day()
>>> Gender.insert_gender()
>>> TimeOfDay.insert_timeofday()
>>> RideOrWalk.insert_rideorwalk()
>>> Handicap.insert_handicap()
>>> Smoking.insert_smoking()
>>> Drinking.insert_drinking()
>>> PlayingType.insert_playingtype()
>>> Role.insert_roles()
>>> User.add_self_follows()
>>> exit()
```

First, run the program:
```bash
flask run
```
Login and make a new user. You can change the underlying admin email address in order to have an administrator. 
Then, navigate to your *register* template: __localhost:5000/auth/register__ and register your email address. Confirm yourself as a user by opening the link sent to you in an email (see [Send Emails](#send-emails)).
Now you can add as many golfers as you want. You can also search for other users and follow them. 

You can also create fake user data using the fake.py. 

## User Data
Each golfer has basic biodemo data such as name, age, city, state, bio section, gender. In addition, there are ways that enable the golfers to specify criteria of their interests in a golfing partner such as a certain day, time of day that they are avaliable, if they prefer riding or walking, a certain handicap, and playing type such as for fun or competitive.  

## Features
Golfers can follow others and be followed. There is also a forum where golfers can post last minute hangout ideas or post questions in general. The match section allows users to filter golfers according to their specifications. The messages section allows users to direct message each other to understand each other on a more direct level. 

## Migrations
To initialize the database. 
```bash
flask db init
```
Whenever a database migration needs to be made. Run the following commands:
```bash
flask db migrate
```
This will generate a new migration script. To apply the migration, run:
```bash
flask db upgrade
```
For a full migration command reference, run ```flask db --help```.

## Send Emails
For email sending to work properly with this app, including confirmation emails, you must have an email that accepts SMTP authentication. Then, you must then set the environment variables MAIL_USERNAME, MAIL_PASSWORD, and APP_ADMIN that are found in ```config.py```
You can configure those variables in a bash script:
```bash
export MAIL_USERNAME=<your_username>
export MAIL_PASSWORD=<your_password>
export APP_ADMIN=<yourusername@example.com>
```

## Environment Variables
It might be useful to save your environment variables in your project, so you do not need to set them up each time you run the app. To do so, run the following:
```bash
touch .env
```
Be sure to create it in your root directory and not to push it to GitHub or any public space where it can be viewed. Then you can add your environment variables to the file. For example:

python
# .env
FLASK_APP=golf_app.py
FLASK_ENV=development
FLASK_CONFIG=development
FLASK_DEBUG=0
FOLLOWERS_PER_PAGE=25 

## Future Features
Here are some features that will be in future releases:
Groupon API that shows current deals for golf. 
A more integrated scheduling system that allows golfers to schedule and book tee times within Tee Timers.
An option to share images, videos, and voice call other users. 
A platform that allows users to track their own statistics and compete with others. 


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.
