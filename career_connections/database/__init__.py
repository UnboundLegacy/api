import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

Base = declarative_base()


def init_app_db(app):
    import career_connections.database.models

    if 'SQLALCHEMY_ENGINE' not in app.config:
        app.config['SQLALCHEMY_ENGINE'] = sqlalchemy.create_engine(app.config['DB_CONNECTION_STRING'], echo=False)
    if 'SESSION' not in app.config:
        engine = app.config['SQLALCHEMY_ENGINE']
        session_factory = sessionmaker(bind=engine)
        app.config['SESSION'] = scoped_session(session_factory)

        Base.metadata.create_all(engine)
