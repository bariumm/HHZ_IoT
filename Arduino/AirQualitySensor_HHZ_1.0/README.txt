1. If not already done, create a user called "hhz" on the Raspberry Pi. (sudo adduser hhz)
2. In the hhz-user's home-directory, create the folder "Scripts". (sudo mkdir Scripts)
3. Place both "airsensor" and "sendAirQ.py" into "/home/hhz/Scripts. (sudo mv [SOURCE PATH] [TARGET PATH])
4. Make sure both scripts have the privileges to be executed by the hhz-user (sudo chmod 770 [FILENAME]).
5. Adapt the crontab according to your needs (sudo crontab -e).