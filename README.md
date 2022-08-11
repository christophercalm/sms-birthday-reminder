# sms-birthday-reminder

### Motivation: 
I wanted an easy way to receive notifications about upcoming birthdays without having to check a social media site. With this script, I can host it cheaply and use free twilio credits to always be reminded of a birthday that is important to me. 

### How to setup

- Rename `example.env` to `.env`
- Add your twilio credentials and desired phone numbers.
- rename `example.birthdays.csv` to `birthdays.csv` and change data.

- Run script:
    - Docker Method:
        - `docker build --tag python-sms-docker .`
        - `docker run python-sms-docker`
    - Manual Method:
        - Install Python 3
        - `pip3 install -r requirements.txt`
        - `python3 send-birthday-sms {days in advance to receive text}`