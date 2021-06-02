"""
This is the short_link module and supports all the REST actions for the
people data
"""

from flask import make_response, abort, redirect
from config import db
from models import ShortLink, ShortLinkSchema
from datetime import datetime, timedelta





class Helpers:

    DEFAULT_EXPIRATION_DAYS = 90
    
    @staticmethod
    def _calculate_slug(num):
        map = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        slug = ""
          
        # for each digit find the base 62
        while(num > 0):
            slug += map[num % 62]
            num //= 62
  
        # reversing the shortURL
        return slug[len(slug): : -1]

    def _get_invalid_ShortLink():
        expiration = datetime.utcnow() + timedelta(days=DEFAULT_EXPIRATION_DAYS)
        new_link = ShortLink(slug='0000000', destination=None, expiration=expiration)
        return new_link


    @classmethod
    def generate_slug(cls):
        #db_entry_cnt = db.session.query(ShortLink).count()
        #proposed_slug = cls.calculate_slug(db_entry_cnt+1)

        last_entry = db.session.query(ShortLink).order_by(ShortLink.id.desc()).first()
        proposed_slug = cls.calculate_slug(db_entry_cnt+1)


        while(True):
            existing_slug = (
                ShortLink.query.filter(ShortLink.slug == proposed_slug)
                .one_or_none()
            )

            if existing_slug is None:
                return proposed_slug

            # slug is present but not at its correct id
            # therefore the slug was user-geenrated already
            db.session.add(new_link)


    #TODO
    @staticmethod
    def is_slug_acceptable(slug):
        return True
    
    
    @staticmethod
    def add_https(destination):
        if destination.find("http://") != 0 and destination.find("https://") != 0:
            destination = "http://" + destination
        return destination
    
    @staticmethod
    def is_destination_acceptable(destination):
        print(destination)
        if destination.find('www.') == -1 or destination.find('.com') == -1:
                return False
        return True





