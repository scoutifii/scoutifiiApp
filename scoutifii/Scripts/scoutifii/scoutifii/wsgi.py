
import os
import pathlib
import dotenv
import django

from django.core.wsgi import get_wsgi_application

# django.setup()

CURRENT_DIR = pathlib.Path(__file__).resolve().parent
BASE_DIR = CURRENT_DIR.parent
ENV_FILE_PATH = BASE_DIR /".env"

dotenv.load_dotenv(str(ENV_FILE_PATH))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scoutifii.settings')

application = get_wsgi_application()
