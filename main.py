import psycopg2
from psycopg2.errors import DivisionByZero
import os
from dotenv import load_dotenv

import database

load_dotenv()
connection = psycopg2.connect(os.environ["DATABASE_URL"])

