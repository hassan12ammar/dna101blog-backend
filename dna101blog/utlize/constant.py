#Import the required dependencies
import os
from dotenv import load_dotenv

#Load environment variables from .env file
load_dotenv()

#Get specific environment variables
SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = bool(os.environ['DEBUG'])
# general constants
DESCRIPTION="Backend for Blog and Courses website using Django and Ninja"
CONTENT_PER_PAGE=8
