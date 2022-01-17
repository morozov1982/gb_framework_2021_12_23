from os import path
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_URL = '/static/'
STATIC_ROOT = path.join(BASE_DIR, 'static')
