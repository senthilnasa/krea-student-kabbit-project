
import os

class Config:
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', '333')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://kabbit:kabbit@localhost:3306/kabbit_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME',"kabbitkrea@gmail.com")
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD',"rktkonpdyjuyccxj")
