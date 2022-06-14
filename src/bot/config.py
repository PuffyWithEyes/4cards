import os
from dotenv import load_dotenv

load_dotenv('../con_db/.env')

TOKEN = os.environ['TOKEN']
HOST = os.environ['HOST']
DB_NAME = os.environ['DB_NAME']
PORT = os.environ['PORT']
PASSWORD = os.environ['PASSWORD']
USER = os.environ['USER']
RED_ADMIN = os.environ['RED_ADMIN']
RED_ADMIN_PASSWORD = os.environ['RED_ADMIN_PASSWORD']
