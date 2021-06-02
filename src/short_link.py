"""
This is the short_link module and supports all the REST actions for the
people data
"""

from flask import make_response, abort, redirect
from config import db
from models import ShortLink, ShortLinkSchema
from datetime import datetime, timedelta
import helpers



#DEFAULT_EXPIRATION_DAYS = 90

##TODO
#def _generate_slug():
#    return 1111111
#
##TODO
#def _is_slug_acceptable(slug):
#    return True
#
#
#
#def _add_https(destination):
#    if destination.find("http://") != 0 and destination.find("https://") != 0:
#        destination = "http://" + destination
#    return destination
#
#def _is_destination_acceptable(destination):
#    print(destination)
#    if destination.find('www.') == -1 or destination.find('.com') == -1:
#            return False
#    return True




def read_all():
    """
    This function responds to a request for /api/shortlinks
    with the complete lists of shortlinks

    :return:        json string of list of shortlinks
    """
    # Create the list of people from our data
    link = ShortLink.query.order_by(ShortLink.shortLink_id).all()

    # Serialize the data for the response
    schema = ShortLinkSchema(many=True)
    data = schema.dump(link)

    print(db.session.query(ShortLink).count())

    return data


def create(link):
    """
    This function creates a new shortlink based on the passed in destination

    :param link:    holds info needed to create shortlink
    :return:        201 on success, 406 on person exists
    """
    destination = link.get("destination")
    if Helpers.is_destination_acceptable(destination) is False:
        abort(
            409,
            "Destination {destination} is malformed".format(
                destination=destination
            ),
        )
    destination = _add_https(destination)

    existing_link = (
        ShortLink.query.filter(ShortLink.destination == destination)
        .one_or_none()
    )

    # Can we insert this shortlink?
    if existing_link is None:

        # Create a shortlink instance using the schema and the passed in person
        slug = Helpers.generate_slug()
        expiration = datetime.utcnow() + timedelta(days=Helpers.DEFAULT_EXPIRATION_DAYS)
        new_link = ShortLink(slug=slug, destination=destination, expiration=expiration)

        # Add the shortlink to the database
        db.session.add(new_link)
        db.session.commit()

        # Serialize and return the newly created link in the response
        schema = ShortLinkSchema()
        data = schema.dump(new_link)

        return data, 201

    # Otherwise, nope, person exists already
    else:
        abort(
            409,
            "ShortLink {destination} exists already".format(
                destination=destination
            ),
        )

def create_custom(slug, link):
    """
    This function creates a new shortlink to a custom slug based on the passed in destination

    :param slug:    custom url ending
    :param link:    holds info needed to create shortlink
    :return:        201 on success, 406 on person exists
    """
    destination = link.get("destination")
    if Helpers.is_destination_acceptable(destination) is False:
        abort(
            409,
            "Destination {destination} is malformed".format(
                destination=destination
            ),
        )
    destination = Helpers.add_https(destination)

    existing_slug = (
        ShortLink.query.filter(ShortLink.slug == slug)
        .one_or_none()
    )
    if existing_slug is not None:
        abort(
            409,
            "ShortLink for {slug} exists already".format(
                slug=slug
            ),
        )

    existing_destination = (
        ShortLink.query.filter(ShortLink.destination == destination)
        .one_or_none()
    )
    if existing_destination is not None:
        abort(
            409,
            "ShortLink for {destination} exists already".format(
                destination=destination
            ),
        )

    if Helpers.is_slug_acceptable(slug) == False:
        abort(
            409,
            "Slug {slug} is not acceptable. Please choose 7 characts made of A-Z, a-z, 0-9".format(
                slug=slug
            ),
        )
        
    ## if we can create the link...
    # Create a shortlink instance using the schema and the passed in person
    expiration = datetime.utcnow() + timedelta(days=Helpers.DEFAULT_EXPIRATION_DAYS)
    new_link = ShortLink(slug=slug, destination=destination, expiration=expiration)

    # Add the shortlink to the database
    db.session.add(new_link)
    db.session.commit()

    # Serialize and return the newly created link in the response
    schema = ShortLinkSchema()
    data = schema.dump(new_link)

    return data, 201


def redirect(slug):
    """
    This function redirects the custom url to the destination stored in the database

    :param slug:    custom url ending
    :return:        201 on success, 406 on person exists
    """

    existing_link = (
        ShortLink.query.filter(ShortLink.slug == slug)
        .one_or_none()
    )
    if existing_link is None:
        abort(
            404,
            "ShortLink {slug} does not exist".format(
                slug=slug
            ),
        )

    headers = {'Location': existing_link.destination}
    return None, 302, headers
    #return redirect(existing_link.destination)





def clean_up():
    """
    This function removes links that are beyond their expiration date

    :return:            200 on successful clean-up
    """
    # Find all the old links
    links = ShortLink.query.filter(ShortLink.expiration < datetime.utcnow()).all()

    # Did we find a person?
    if links is not None:
        for link in links:
            db.session.delete(link)
            db.session.commit()
    return make_response(
        "Cleaned up stale links", 200
    )

