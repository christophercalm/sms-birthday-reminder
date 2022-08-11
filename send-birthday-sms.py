# Download the helper library from https://www.twilio.com/docs/python/install
import os
import csv
import copy
from datetime import timedelta, datetime
from twilio.rest import Client
from dotenv import load_dotenv


load_dotenv()

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


def create_birthday_message(birthday_people):
    birthday_message = ""
    for person in birthday_people: 
        birthday = person.get("birthday")
        if (birthday.year == default_year):
            birthday_message = birthday_message + f"{person.get('name')}'s birthday is tomorrow\n"
        else:
            birthday_message = birthday_message + f"{person.get('name')}'s birthday is tomorrow and will be {datetime.now().year - birthday.year} years old\n"
    return birthday_message

def main():
    print("Starting birthday SMS script")
    print("Current Date: " + str(datetime.now()))
    load_birthdays_from_CSV()
    birthdays_to_send = []
    for person in people:
        birthday_with_current_year = copy.copy(person["birthday"])
        birthday_with_current_year = birthday_with_current_year.replace(year = datetime.now().year)
        tomorrow_datetime = datetime.now().replace(hour=0, minute = 0, second = 0, microsecond = 0) + timedelta(days=1)
        day_after_tomorrow_datetime = tomorrow_datetime + timedelta(days=1)
        birthday_tomorrow = birthday_with_current_year >= tomorrow_datetime and birthday_with_current_year <= day_after_tomorrow_datetime
        if(birthday_tomorrow):
            birthdays_to_send.append(person)
    if(len(birthdays_to_send) > 0):
        birthday_message = create_birthday_message(birthdays_to_send)
        print(birthday_message)
        send_sms(birthday_message)
    else:
        print("No birthdays to send\n")

def send_sms(message):
    message = client.messages \
        .create(
            body=message,
            from_=from_number,
            to=to_number
        )

    print(message.sid)

main()