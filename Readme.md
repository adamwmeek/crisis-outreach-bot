# Crisis Outreach Discord Bot

The goal of ths Discord bot is to facilitate the response to a potential mental health crisis as it takes place on a Discord server. When a potential crisis is detected, the bot will take action to immediatly provide resource info as well as alerting of the potential crisis. Currentl, this bot works by watching a Discord server for keywords that indicate that a member is in a mental health crisis. The bot can then take a number of actions, including providing resources, alerting staff, and logging the incident. 

## How it works

When the bot sees a member of a discord server send a message containing a keyword from a list of defined keywords, it will automatically take a number of actions to address a potential crisis situation, such as:

* DMing the author with a pre-defined message containing crisis resources
* Alerting other members to a potential crisis 
* Other actions to come...

To prevent from spamming a user with messages, the bot also comes with a configureable timeout timer. (The default interval is 30 min.)

## Future work

Currently planned work for the future includes making the bot easier to configure from Discord commands. 
