from psycopg2.extras import execute_values

CREATE_POLLS = """CREATE TABLE IF NOT EXISTS polls (id SERIAL PRIMARY KEY, title TEXT, owner_username TEXT);"""

CREATE_OPTIONS = """CREATE TABLE IF NOT EXISTS options 
                    (id SERIAL PRIMARY KEY, 
                    option_text TEXT, 
                    poll_id INTEGER, 
                    FOREIGN KEY(poll_id) REFERENCES polls(id));"""

CREATE_VOTES = """  CREATE TABLE IF NOT EXISTS votes 
                    (username TEXT, 
                    option_id INTEGER, 
                    FOREIGN KEY (option_id) REFERENCES options(id));"""

SELECT_ALL_POOLS = """SELECT * FROM pools;"""

SELECT_POOL_WITH_OPTIONS = """  SELECT * FROM polls
                                JOIN options
                                ON polls.id = options.poll_id
                                WHERE polls.id = %s ;"""

SELECT_LATEST_POLL = """SELECT * FROM polls
                        JOIN options 
                        ON polls.id = options.polls_id
                        WHERE polls.id = (
                        SELECT id FROM polls ORDER BY id DESC LIMIT 1
                        );"""

SELECT_POLL_VOTE_DETAILS = """  SELECT options.id, options.option_text
                                FROM options
"""

INSERT_OPTION = """ INSERT INTO options (option_text, poll_id) VALUES %s;"""

INSERT_VOTE = """ INSERT INTO votes (username, option_id) VALUES (%s, %s);"""

INSERT_POLL_ENTITY = """INSERT INTO polls (title, owner_username) VALUES (%s, %s) RETURNING id;"""

def create_tables(connection):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_POLLS)
            cursor.execute(CREATE_OPTIONS)
            cursor.execute(CREATE_VOTES)


def get_polls(connection):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_POOLS)
            return cursor.fetchall()


def get_latest_poll(connection):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_LATEST_POLL)
            return cursor.fetchall()  # not fetchone - return multiple rows because of options included


def get_poll_details(connection, poll_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_POOL_WITH_OPTIONS, (poll_id, ))
            return cursor.fetchall()


def get_poll_and_vote_results(connection, poll_id):
    with connection:
        with connection.cursor() as cursor:
            pass


def get_random_poll_vote(connection, option_id):
    with connection:
        with connection.cursor() as cursor:
            pass


def create_poll(connection, poll_name, poll_owner, options):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_POLL_ENTITY, (poll_name, poll_owner))
            poll_id = cursor.fetchone()[0]

            option_values = [(option, poll_id) for option in options]
            execute_values(cursor, INSERT_OPTION, option_values)

            # for option in options:
            #     cursor.execute(INSERT_OPTION, (option, poll_id))

def add_poll_vote(connection, username, option_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_VOTE, (username, option_id))