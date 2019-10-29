from app import app, db
from auth import *
from api import api
from models import *
from views import *

api.setup()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
