"""
This is the short_link module and supports all the REST actions for the
people data
"""

from flask import make_response, abort, redirect
from config import db
from models import ShortLink, ShortLinkSchema
from datetime import datetime, timedelta





class Helpers:

    SLUG_LENGTH = 7
    DEFAULT_EXPIRATION_DAYS = 90
    
    @classmethod
    def _calculate_slug(cls, num):
        # Map to store 62 possible characters
        map = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        slug = ""
          
        # for each digit find the base 62
        while(num > 0):
            slug += map[num % 62]
            num //= 62
  
        # make sure slug has correct length
        if len(slug) < cls.SLUG_LENGTH:
            slug = slug.ljust(cls.SLUG_LENGTH, 'a')


        # reversing the shortURL
        return slug[len(slug): : -1]


    @classmethod
    def _get_dummy_ShortLink(cls):
        expiration = datetime.utcnow() + timedelta(days=cls.DEFAULT_EXPIRATION_DAYS)
        new_link = ShortLink(slug='aaaaaaa', destination=None, expiration=expiration)
        return new_link


    @classmethod
    def generate_slug(cls):
        last_entry = db.session.query(ShortLink).order_by(ShortLink.shortLink_id.desc()).first()
        next_id = last_entry.shortLink_id + 1


        while(True):
            proposed_slug = cls._calculate_slug(next_id)

            existing_slug = (
                ShortLink.query.filter(ShortLink.slug == proposed_slug)
                .one_or_none()
            )

            if existing_slug is None:
                return proposed_slug

            # slug is present but not at its correct id
            # therefore the slug was user-geenrated already
            new_link = cls._get_dummy_ShortLink()
            db.session.add(new_link)
            db.session.commit()

            next_id += 1


    @staticmethod
    def is_slug_acceptable(slug):
        if len(slug) != 7 or slug.isalnum() is False:
            return False
        return True
    
    
    @staticmethod
    def add_https(destination):
        if destination.find("http://") != 0 and destination.find("https://") != 0:
            destination = "http://" + destination
        return destination


    @staticmethod
    def is_destination_acceptable(destination):
        #TODO - How do we accept more domaigns (e.g. .uk)?
        if destination.find('www.') == -1 or (destination.find('.com') == -1 and destination.find('.org') == -1):
                return False
        return True

