import sqlalchemy
from databases import Database
from dotenv import load_dotenv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

###############
# Init database
###############
db = Database(os.environ["DATABASE_URL"])
metadata = sqlalchemy.MetaData()
