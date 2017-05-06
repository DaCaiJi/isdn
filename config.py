import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '30cbf7006ff9489c4e7b89075ece3913'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASKY_ADMIN = 'admin'
    FLASKY_POSTS_PER_PAGE = 20

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


config = {
    'development': DevelopmentConfig,

    'default': DevelopmentConfig
}
