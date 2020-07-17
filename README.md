A software that logs answer to 3 questions regarding current mood.

Results are logged to the current directory as a YAML file.

## Dependencies 

Developed and tested on Xubuntu 18.04, but should work on any Linux.
You will need the following components:
   
   - Python 3.x
   - The requests Python module
   - The yaml Python module
  
On Ubuntu or Debian: 
  
   `sudo apt install python3-requests python3-yaml`

## Installation

   1. Create a Telegram bot, using "botFather"
   2. Edit the bot to 'privacy off'
   3. Configure the token: 
      Copy the token code to a file named 'token', at the current directory.
      If you execute 'ls -l token', you should see something like this:

        `user@host:~/mood_tracker_telegram_bot$ ls -l token`
        `-rw-rw-r-- 1 user user 47 Jul 13 22:24 token`
        `user@host:~/mood_tracker_telegram_bot$ cat token`
        `1????????1:AC???????????????????????????????l4`
        `user@host:~/mood_tracker_telegram_bot$`

   4. From your Telegram client, open a conversation with the bot and send it a message. the content of the message does not matter.
   5. Sanity test that the token is OK:
      Run `./get_updates`. This should display the message you just sent.
   6. Configure the id:
      The id might be an id of a chat, or of a group.
      Look at the text produced by 'get_updates'. Extract the id from a string like 

      `... "chat":{"id":-456789012, ...`

      In the example above, the id is '-456789012'. Put the id into a file named 'id'
   7. OPTIONAL: limiting the bot to process messages only from you:
      From the information displayed by get_updates, copy your user id.
      For example, if get_updates displayed the following:
           ` ... "from":{"id":123456789,"is_bot":false,"first_name" ...`
      The user is '123456789'. 
      Create a file in this directory named 'user' with the content of the user id.

   8. Make the script run every day at 8PM, but adding a line to crontab:
      Using "crontab -e", add the line:
      `0 20 * * * /usr/bin/python3 /home/<user name>/mood_tracker_telegram_bot/bot.py`
## Author

**Shalom Mitz** - [shalommmitz](https://github.com/shalommmitz)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE ) file for details.


