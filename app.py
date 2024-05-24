from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# Import routes after creating app and db instances to avoid circular imports
from routes import *

if __name__ == '__main__':
    app.run(debug=True)
