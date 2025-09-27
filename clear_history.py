from app import app, db
from models import History

with app.app_context():
    History.query.delete()
    db.session.commit()
    print("История очищена!")
