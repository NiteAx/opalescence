# Opalescence

Opalescence is a niche-purpose Discord bot written in Python using [discord.py](https://github.com/Rapptz/discord.py) (async branch)
For the most part, it is largely just a way for me to learn how to do things in Python during my free time. 

### Bot code structure

* [discord.py](https://github.com/Rapptz/discord.py) allows you to use [cogs](https://gist.github.com/leovoel/46cd89ed6a8f41fd09c5) to add funtionality to your bot in the form of modules. 
* The advantage of segmenting bot functionality using cogs is that you are allowed to load and unload individual cogs while the bot is operational without affecting the other ones. 
* In fact, the main python script is really just initializing, defining commands to load and unload modules and running the bot. 
* All useful functionality of the bot is available as individual scripts inside the cogs directory. 

### Requirements
    discord.py 0.16.12
    gspread
    oauth2client
    tinydb

### If you are reading this

You are likely never going to have a need to clone this project or use it as its purpose is so niche that I can't imagine what you'd even do with it. 
