### Python Sportmonks API > MySQL / MariaDB Script
---
- [Sportmonks.com](https://sportmonks.com) Football-API sync
- Real-time Scores, Leagues, Seasons, Players, Teams, Countries, Standings sync options
- Optional Twitter sync to local blog for selected leagues
- Logging to local files under **/logs** directory
- Compatible with **Python3.x+** and **pipenv**
- Depends on SQLAlchemy, requests, logging, phpserialize, pathlib, optional tweepy for **Twitter&reg;** syncing

**Table of Contents**


###Usage
----
1. Make sure to have pipenv installed or alternatively install all required modules with pip
2. Edit the contents of constants.py to suit your needs, note: some constants might be unnecessary leftovers from previous version. It should work without you editing the **constants.py** out of the box
3. Rename _secrets.py to secrets.py and edit contents such as your API_TOKEN, DB_USERNAME, DB_PASSWORD etc.
4. Edit main.py and comment out the operations you don't think you would need and/or change the order of which they run in.
5. There will be a DEFAULT_SLEEP_INTERVAL = 30 delay by default (can be changed in constants.py) between each operation (api_querying)

>By default program takes **DEFAULT_SLEEP_INTERVAL** amount of time (30 seconds) after each operation and it will sleep through that time.

> There is no strict scheduling in place so all delays are relative which means if a job takes 2 minutes to run in total, this will be ignored and all approximations below will be off by quite a bit.

---
### Algorithms running schedule
######*(every interval/endpoint)*
|Interval|Runs|Explanation|
| ------------ | ------------ | ------------ |
||||
|30 seconds|livescores|*self explanatory*|
|25 minutes|seasons|*seasons of all selected countries leagues*|
||standings|*standings of all leagues above*|
||twitter|*optional, syncs twitter posts and retweets*|
|24 hours|teams|*all teams stats for all selected leagues*|
||leagues|*leagues do not usually get changed but just in case*|
|6 days|players|*all players stats for all available leagues*|
||countries|*again, not going to be changed but, wth*|
---

###Iteration Logic
Altough errors are either suppressed and/or logged into log files, every now and then there may be an error which might cause the program to halt and raise an exception which poses a problem since the program would not know where it was left off, therefore an iteration logic implemented to keep track of number of loops and stores that number inside a file called **iter.txt**
This file will be updated everytime there is an algorithm is fully finished running and the number inside will be increased by one. So in case of after an error when you restart the program it will remember where it was left off and carry on going from that iteration.

##TODO:
- Need to deal with ErrorNo24 on linux systems where program hits a limit of number of open files and this causing a wasted query which returns and updates nothing.
- Need to make twitter sync optional in constants.py


##Note:
Please be nice, I am not a python magician, I only know how to solve my specific problems so if you find something odd/bad please make a pull request and I will gladly merge after I study and understand your reasons.


######And they lived happily ever after