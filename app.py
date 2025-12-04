from app.models import db
from app import create_app

apps = create_app("DevelopmentConfig")
with apps.app_context():
    # db.drop_all()
    db.create_all()

if __name__ == "__main__":
    apps.run()
