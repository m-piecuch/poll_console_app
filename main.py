import psycopg2
from time import sleep
from psycopg2.errors import DivisionByZero
import os
from dotenv import load_dotenv

import database

# DATABASE_PROMPT = "Enter custom DATABASE_URI value  or leave empty to load from .env file:  "

DATABASE_PROMPT = """ --- SELECT DB: --- 
1) Provide custom database URI or
2) Select PRODUCTION DATABASE or
or skip selection and press enter for using TEST database (recommended)"""

DATABASE_URI_PROMPT = "Provide database URI: "

MENU_PROMPT = """ 

--- Menu --- 

1)  Create new poll
2)  List open polls
3)  Vote on open poll
4)  Show poll votes
5)  Select a random winner from a poll
6)  Exit

Enter your choice:  """

NEW_OPTION_PROMPT = "Enter new option text (or leave empty to stop adding options): "


def prompt_create_poll(connection):
    poll_name = input("Enter the name of the poll: ")
    poll_owner = input("Enter the name of the poll owner: ")
    options = []

    while option := input(NEW_OPTION_PROMPT):
        options.append(option)

    database.create_poll(connection, poll_name, poll_owner, options)


def list_open_polls(connection):
    polls = database.get_polls(connection)

    for _id, title, owner in polls:
        print(f"{_id}: {title} (created by {owner})")


def prompt_vote_poll(connection):
    poll_id = int(input("Enter poll would you like to vote on:"))

    poll_options = database.get_poll_details(connection, poll_id)
    _print_poll_options(poll_options)

    option_id = int(input("Enter option id you'd like to vote on: "))
    username = input("Enter your username: ")

    database.add_poll_vote(connection, username, option_id)


def _print_poll_options(poll_options: list[database.PollWithOption]):
    for option in poll_options:
        print(f"{option[3]} : {option[4]}")


def show_poll_votes(connection):
    poll_id = int(input("Enter poll you would like do see votes for: "))
    try:
        poll_and_votes = database.get_poll_and_vote_results(connection, poll_id)
    except DivisionByZero:
        print("No votes yet cast for this poll.")
    else:
        for _id, option_text, count, percentage in poll_and_votes:
            print(f" - {option_text} got {count} votes ({percentage:.2f}% of total.)")


def randomize_poll_winner(connection):
    poll_id = int(input("Enter poll you'd like to pick a winner for: "))
    poll_options = database.get_poll_details(connection, poll_id)
    _print_poll_options(poll_options)

    option_id = int(input("Enter the winning option, we'll pick a random winner from voters."))
    winner = database.get_random_poll_vote(connection, option_id)
    print(f"The randomly selected winner is: {winner[0]}")


MENU_OPTIONS = {
    "1": prompt_create_poll,
    "2": list_open_polls,
    "3": prompt_vote_poll,
    "4": show_poll_votes,
    "5": randomize_poll_winner,
}


def menu():

    db_selection = input(DATABASE_PROMPT)

    if not db_selection or db_selection == "2":
        load_dotenv()
        if not db_selection:
            database_url = os.environ["TEST_DATABASE_URL"]
        else:
            database_url = os.environ["DATABASE_URL"]
    elif db_selection == "1":
        database_url = input(DATABASE_URI_PROMPT)
    else:
        print("Connection refused. Try again >>")
        sleep(1)
        menu()

    connection = psycopg2.connect(database_url)
    database.create_tables(connection)

    while (selection := input(MENU_PROMPT)) != "6":
        try:
            MENU_OPTIONS[selection](connection)
        except KeyError:
            print("Invalid input selected. Please try again.")


menu()
