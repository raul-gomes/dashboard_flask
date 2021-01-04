import os


class Config():
    CSRF_ENABLE = True
    SECRET = '#789123#&123654&@'
    TEMPLATE_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    APP = None


class DevelopmentConfig(Config):
    DEBUG = True
    IP_HOST = 'localhost'
    PORT_HOST = 8000
    URL_MAIN = 'http://%s/%s' % (IP_HOST, PORT_HOST)
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:q1w2e3r4@localhost:3306/dashboard'


app_config = {
    'development': DevelopmentConfig()
}

app_active = os.getenv('FLASK_ENV')
if app_active is None:
    app_active = 'development'
