
## What the script do

The script will do the following

* listen for any command send by the admin and run it as a shell command

    * Only admin can send command. Verification is done by checking sender username, user id and a simple password.
    
    * Any message received by unknown sender will be ignored.
    
    * syntax: "<password> <any linux command>"
        * e.g: "mypassword ifconfig -a"


* Periodically send "i am alive" message to admin.

  * Telegram Bot has no online/offline status, so i simply ask the bot to tell me if it is still alive every few minutes.


## Pre-requisites

* Register your Telegram Bot and obtain the token 

    * https://core.telegram.org/bots

* set the bot to accept inline command using "/setinline" 

* start the bot

* Install the following modules

   ```
    # pip install -r requirements.txt
   ```



## Optional Steps

To make sure the script is started during power-on and auto-restarted if it crash for any reason. One of the option is using systemd

### Using systemd

* copy the same unit file

   ```
   $ cp serverbot.service /etc/systemd/system/serverbot.service
   ```

* adjust the unit file

* enable and start the bot

	```
	# systemctl enable serverbot
	# systemctl start serverbot
	```




## Limitation

* The script currently only support direct chat.
    * It can be improved to have a callback mechanism so multiple user can interact with the bot at the same time, and we can include the bot into a telegram group.
* The security is very minimum right now, it only check if the sender ID and username match to a specific value and the passcode (which is the first word of the received message) is matched.
    * Potential improvement:
        * hash the password value
        * support multiple admin
        * ...



## resources:

* https://core.telegram.org/bots
* https://github.com/nickoala/telepot
* http://telepot.readthedocs.io/en/latest/
* https://serversforhackers.com/monitoring-processes-with-supervisord
