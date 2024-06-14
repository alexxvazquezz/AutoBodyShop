import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///autobody_shop.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your_secret_key'