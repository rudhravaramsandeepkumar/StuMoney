from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(
)


def init_app(app):
    db_connection_string = ''
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_BINDS'] = {
        'db': "sqlite:///db.sqlite"
    }
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    db.init_app(app)
    app.logger.info('Initialized models')
    with app.app_context():
        from .UserCredentials import UserCredentials
        db.create_all()
        db.session.commit()
        app.logger.debug('All tables are created')

