from flask import Flask


app = Flask(__name__)

wsgi_app = app.wsgi_app

from routes import *

if __name__ == '__main__':
  import os
  HOST = os.environ.get('SERVER_HOST', 'localhost')
  try:
    PORT = int(os.environ.get('SERVER_PORT', '5555'))
  except ValueError:
    PORT = 55555
  app.run()
