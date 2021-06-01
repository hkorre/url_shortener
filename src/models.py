from datetime import datetime
from config import db, ma


class ShortLink(db.Model):
    __tablename__ = 'short_link'
    shortLink_id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(32), index=True)
    destination = db.Column(db.String(32))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    expiration = db.Column(db.DateTime, default=datetime.utcnow)

class ShortLinkSchema(ma.SQLAlchemyAutoSchema):
      class Meta:
            model = ShortLink
            load_instance = True
