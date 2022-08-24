# Download the helper library from https://www.twilio.com/docs/python/install
import os
import csv
import copy
import sys
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


def create_birthday_message(birthday_people, days_in_advance):
    birthday_message = ""
    for person in birthday_people: 
        birthday = person.get("birthday")
        if (birthday.year == default_year):
            birthday_message = birthday_message + f"{person.get('name')}'s birthday is within {days_in_advance} day(s) \n"
        else:
            birthday_message = birthday_message + f"{person.get('name')}'s birthday is within {days_in_advance} day(s) and will be {datetime.now().year - birthday.year} years old\n"
    return birthday_message

def send_sms(message):
    try: 
        message = client.messages \
        .create(
            body=message,
            from_=from_number,
            to=to_number
        )
    except:
        print("An exception occurred while trying to send message")

def check_if_birthday_in_window(person, days_in_advance):
    birthday_with_current_year = copy.copy(person["birthday"])
    birthday_with_current_year = birthday_with_current_year.replace(year = datetime.now().year)
    advance_datetime = datetime.now().replace(hour=0, minute = 0, second = 0, microsecond = 0) + timedelta(days=days_in_advance)
    day_after_advance_datetime = advance_datetime + timedelta(days=1)
    return birthday_with_current_year >= advance_datetime and birthday_with_current_year < day_after_advance_datetime

def main():
    print("Starting birthday SMS script")
    print("Current Date: " + str(datetime.now()))
    load_birthdays_from_CSV()

    days_in_advance = 1

    # get arguments from command line
    command_line_args = sys.argv[1:]
    if (command_line_args and command_line_args[0].isdigit()):
        days_in_advance = int(command_line_args[0])

    birthdays_to_send = []
    for person in people:
        birthday_within_window = check_if_birthday_in_window(person, days_in_advance)
        if(birthday_within_window):
            birthdays_to_send.append(person)

    if(len(birthdays_to_send) > 0):
        birthday_message = create_birthday_message(birthdays_to_send, days_in_advance)
        print(birthday_message)
        send_sms(birthday_message)
    else:
        print("No birthdays to send\n")    

main()