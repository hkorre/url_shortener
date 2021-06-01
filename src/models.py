from datetime import datetime, timedelta
from config import db, ma

DEFAULT_EXPIRATION_DAYS = 90

class ShortLink(db.Model):
    __tablename__ = 'short_link'
    shortLink_id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(32), index=True)
    destination = db.Column(db.String(32))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    expiration = db.Column(db.DateTime, default=datetime.utcnow + timedelta(days=DEFAULT_EXPIRATION_DAYS))

class ShortLinkSchema(ma.SQLAlchemyAutoSchema):
      class Meta:
            model = ShortLink
            load_instance = True
