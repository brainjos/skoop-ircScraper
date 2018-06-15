### Skoop v1.0: an IRC scraper bot to maintain a record of tech-related inquirues and their answers

No external plugins required, just python 3.x and included libraries. Uses multithreading. Saves message chains in `chainlog.json`.

#### Instructions:

Clone respository. Touch `config.py` and format as such:

```
#!/usr/bin/python3
server = "irc.example.net"
channel = "#channel"
botnick = "skoop"
chain_duration = 3600 #seconds before message chain considered 'closed' i.e. ready to archive 
archive_check_delay = 600 #time between 'checks' -- where all currently open chains are archived if closed
keywords = ["network", "helpername1"]
helpers = ["helpername1", "helpername2", "helpername3"]
blockwords = ["channelSpecificCommand"]
blockusers = ["channelBot1"]
```

Then just run `python skoop.py`!
