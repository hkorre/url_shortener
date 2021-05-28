FROM continuumio/anaconda3:latest


### custom installs ###################################
RUN apt-get update --fix-missing

# Helper libraries
RUN apt-get install -y \
       git \
       man \
       vim
#       libgtk2.0-0

#RUN conda install -y \
#          python=3.5.0

RUN pip install \
       pandas

# Needed for pdf2image
RUN apt-get install -y \
       poppler-utils

# Needed for pytesseract
RUN apt-get install -y \
       libleptonica-dev \
       tesseract-ocr \
       libtesseract-dev

# Optiocal Character Recognition libraries
RUN pip install \
       Pillow \
       pytesseract \
       pdf2image

# Named Entity  Recognition libraries
RUN pip install \
       spacy==2.3.1

RUN pip install \
       datefinder

#RUN conda install -y \
#          -c https://conda.anaconda.org/menpo opencv3
#
#RUN conda install -y \
#          -c conda-forge tensorflow
#
#RUN conda install -y \
#          jupyter \
#          scikit-learn
#
#
#### keras ##########################################
#RUN pip install \
#       keras \
#       h5py \
#       scipy \
#       scikit-learn \
#       Pillow
#
#COPY keras.json /root/.keras/keras.json
#
## Upgrade keras to latest
##RUN pip install git+git://github.com/fchollet/keras.git --upgrade
#
#### Behavior Cloning ################################
#RUN conda install -y -c conda-forge \
#          flask-socketio \
#          eventlet
#
#
#### moviepy ##########################################
#RUN pip install \
#       moviepy
#
#RUN echo "deb http://ftp.uk.debian.org/debian jessie-backports main" >> /etc/apt/sources.list \
#   && apt-get update \
#   && apt-get install -y ffmpeg


EXPOSE 5000-65535

CMD ["/bin/bash"]
