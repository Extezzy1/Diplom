import os

from dotenv import load_dotenv

load_dotenv()

bot_token = str(os.getenv(("TOKEN_BOT")))

postgresIP = str(os.getenv(("IP")))
postgresUSER = str(os.getenv(("PGUSER")))
postgresPSW = str(os.getenv(("PGPASSWORD")))
postgresDB = str(os.getenv(("DATABASE")))


ADMINS = [537373044]