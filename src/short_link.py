"""
This is the short_link module and supports all the REST actions for the
people data
"""

from flask import make_response, abort
from config import db
from models import ShortLink, ShortLinkSchema
from datetime import datetime, timedelta



DEFAULT_EXPIRATION_DAYS = 90

#TODO
def _generate_slug():
    return 1111111

#TODO
def _is_slug_acceptable(slug):
    return True



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
    return data


def create(link):
    """
    This function creates a new shortlink based on the passed in destination

    :param link:    holds info needed to create shortlink
    :return:        201 on success, 406 on person exists
    """
    destination = link.get("destination")

    existing_link = (
        ShortLink.query.filter(ShortLink.destination == destination)
        .one_or_none()
    )

    # Can we insert this shortlink?
    if existing_link is None:

        # Create a shortlink instance using the schema and the passed in person
        slug = _generate_slug()
        expiration = datetime.utcnow() + timedelta(days=DEFAULT_EXPIRATION_DAYS)
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

    if _is_slug_acceptable(slug) == False:
        abort(
            409,
            "Slug {slug} is not acceptable. Please choose 7 characts made of A-Z, a-z, 0-9".format(
                slug=slug
            ),
        )
        
    ## if we can create the link...
    # Create a shortlink instance using the schema and the passed in person
    expiration = datetime.utcnow() + timedelta(days=DEFAULT_EXPIRATION_DAYS)
    new_link = ShortLink(slug=slug, destination=destination, expiration=expiration)

    # Add the shortlink to the database
    db.session.add(new_link)
    db.session.commit()

    # Serialize and return the newly created link in the response
    schema = ShortLinkSchema()
    data = schema.dump(new_link)

    return data, 201



#def update(person_id, person):
#    """
#    This function updates an existing person in the people structure
#    Throws an error if a person with the name we want to update to
#    already exists in the database.
#
#    :param person_id:   Id of the person to update in the people structure
#    :param person:      person to update
#    :return:            updated person structure
#    """
#    # Get the person requested from the db into session
#    update_person = Person.query.filter(
#        Person.person_id == person_id
#    ).one_or_none()
#
#    # Try to find an existing person with the same name as the update
#    fname = person.get("fname")
#    lname = person.get("lname")
#
#    existing_person = (
#        Person.query.filter(Person.fname == fname)
#        .filter(Person.lname == lname)
#        .one_or_none()
#    )
#
#    # Are we trying to find a person that does not exist?
#    if update_person is None:
#        abort(
#            404,
#            "Person not found for Id: {person_id}".format(person_id=person_id),
#        )
#
#    # Would our update create a duplicate of another person already existing?
#    elif (
#        existing_person is not None and existing_person.person_id != person_id
#    ):
#        abort(
#            409,
#            "Person {fname} {lname} exists already".format(
#                fname=fname, lname=lname
#            ),
#        )
#
#    # Otherwise go ahead and update!
#    else:
#
#        # turn the passed in person into a db object
#        schema = PersonSchema()
#        update = schema.load(person, session=db.session)
#
#        # Set the id to the person we want to update
#        update.person_id = update_person.person_id
#
#        # merge the new object into the old and commit it to the db
#        db.session.merge(update)
#        db.session.commit()
#
#        # return updated person in the response
#        data = schema.dump(update_person)
#
#        return data, 200


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

