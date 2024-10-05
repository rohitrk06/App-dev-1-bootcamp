class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///grocery_store.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'personal_protected_key'