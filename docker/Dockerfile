FROM continuumio/anaconda3:latest


### custom installs ###################################
RUN apt-get update --fix-missing

# Helper libraries
RUN apt-get install -y \
       git \
       man \
       vim
#       libgtk2.0-0

# Connexion for python
RUN pip install \
       connexion[swagger-ui]


# Get Flask
RUN pip install \
       Flask

# Add database dependencies
RUN pip install \
       Flask-SQLAlchemy \
       flask-marshmallow \
       marshmallow-sqlalchemy \
       marshmallow




EXPOSE 5000-65535

CMD ["/bin/bash"]
