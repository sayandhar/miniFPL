# miniFPL

A Fantasy Premier League API in Python 3

### Running the demo
Install the required python libraries.
```
$ python requirements.txt
```
Run the app
```
$ python app.py
---
Bottle v0.12.13 server starting up (using WSGIRefServer())...
Listening on http://127.0.0.1:8080/
Hit Ctrl-C to quit.
```

Once the bottle server starts, head over to http://localhost:8080/. Enter the Team ID and click search.

![Imgur](https://i.imgur.com/wmemD5x.png)

### Finding your Team ID & League ID

- Login to FPL website.
- Click on Points tab and check the URL.   
It'll look something like https://fantasy.premierleague.com/a/team/123456/event/3. Here, 123456 is your fantasy team ID.
- Click on the Leagues Tab and click on the required league.  
The URL will be something like https://fantasy.premierleague.com/a/leagues/standings/246824/classic. Here, 246824 is your league ID.