import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class config:
        SECRET_KEY = os.getenv('SECRET_KEY', 'secret key')
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', "sqlite:///site.db")
        JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', "jwt secret key")
        JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))
       

