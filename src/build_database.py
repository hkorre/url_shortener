import os
from config import db
from models import ShortLink

# Data to initialize database with
LINKS = [
    {'slug': 'google0', 'destination': 'https://www.google.com/'},
    {'slug': 'cnn0000', 'destination': 'https://www.cnn.com/'},
    {'slug': 'kalepa0','destination': 'https://kalepainsurance.com/'}
]

# Delete database file if it exists currently
if os.path.exists('short_link.db'):
    os.remove('short_link.db')

# Create the database
db.create_all()

# Iterate over the LINKS structure and populate the database
for link in LINKS:
    sLink = ShortLink(slug=link['slug'], destination=link['destination'])
    db.session.add(sLink)

db.session.commit()
