class Config:
    # Setup a Sectet Key
    SECRET_KEY='dadc98d2ce2925035ffc2bdc6ce3c190'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    # Email Address
    MAIL_USERNAME = 'NTU.ReID@gmail.com'
    # Email Password
    MAIL_PASSWORD = 'ROSE_ReID_Team_2019'

    FLASK_ADMIN_SWATCH = 'cerulean'

    BASIC_AUTH_USERNAME = 'ROSE-ReID'
    BASIC_AUTH_PASSWORD = 'ROSE_ReID_Team_2019'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
