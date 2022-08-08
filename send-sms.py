# Download the helper library from https://www.twilio.com/docs/python/install
import os
import csv
import copy
from datetime import timedelta, datetime
from twilio.rest import Client
from dotenv import load_dotenv


load_dotenv()

birthdays = { "Christopher": "June 1, 1995", "Test": "July 2, 1998" }
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
from_number = os.getenv("TWILIO_FROM_NUMBER")
to_number = os.getenv("TWILIO_TO_NUMBER")

default_year = "1900"
client = Client(account_sid, auth_token)

people = []

def load_birthdays_from_CSV():
    with open('birthdays.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for person in reader:
            people.append({"name": person[0], "birthday": datetime.strptime(person[1], "%m/%d/%Y")})
        #print(people)


def create_birthday_message(name, birthdays):
    birthday_message = ""
    for birthday in birthdays: 
        if (birthday.year = 1900):
            birthday_message = birthday_message + f"{name}'s birthday is tomorrow\n"
        else:
            return f"{name}'s birthday is tomorrow and will be {birthday.year - datetime.now().year} years old"




def main():
    # for name, birthday in birthdays.items():
    #     send_sms(name, birthday)
    load_birthdays_from_CSV()
    birthdays_to_send = []
    for person in people:
        birthday_with_current_year = copy.copy(person["birthday"])
        birthday_with_current_year = birthday_with_current_year.replace(year = datetime.now().year)
        tomorrow_datetime = datetime.now().replace(hour=0, minute = 0, second = 0, microsecond = 0) + timedelta(days=1)
        day_after_tomorrow_datetime = tomorrow_datetime + timedelta(days=1)
        if(birthday_with_current_year >= tomorrow_datetime and birthday_with_current_year <= day_after_tomorrow_datetime):
            birthdays_to_send.append(person)
        if(len(birthdays_to_send) > 0):
            send_sms(birthdays_to_send)

def send_sms(name, birthday):
    message = client.messages \
        .create(
            body=f"{name}'s birthday is on {birthday}",
            from_=from_number,
            to=to_number
        )

    print(message.sid)

main()