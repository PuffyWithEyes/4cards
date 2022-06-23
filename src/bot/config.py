import os
from dotenv import load_dotenv

load_dotenv('../con_db/.env')

TOKEN = os.environ['TOKEN']
HOST = os.environ['HOST']
DB_NAME = os.environ['DB_NAME']
PORT = os.environ['PORT']
PASSWORD = os.environ['PASSWORD']
USER = os.environ['USER']
RED_ADMIN_0 = os.environ['RED_ADMIN_0']
RED_ADMIN_PASSWORD_0 = os.environ['RED_ADMIN_PASSWORD_0']
RED_ADMIN_1 = os.environ['RED_ADMIN_1']
RED_ADMIN_PASSWORD_1 = os.environ['RED_ADMIN_PASSWORD_1']
