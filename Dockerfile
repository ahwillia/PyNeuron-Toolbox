#
# NEURON Dockerfile
#

# Pull base image.
FROM andrewosh/binder-base

MAINTAINER Alex Williams <alex.h.willia@gmail.com>

USER root

RUN \
  apt-get update && \
  apt-get install -y libncurses-dev

# Make ~/neuron directory to hold stuff.
WORKDIR neuron

# Fetch NEURON source files, extract them, delete .tar.gz file.
RUN \
  wget http://www.neuron.yale.edu/ftp/neuron/versions/v7.4/nrn-7.4.tar.gz && \
  tar -xzf nrn-7.4.tar.gz && \
  rm nrn-7.4.tar.gz

# Fetch Interviews.
# RUN \
#  wget http://www.neuron.yale.edu/ftp/neuron/versions/v7.4/iv-19.tar.gz  && \  
#  tar -xzf iv-19.tar.gz && \
#  rm iv-19.tar.gz

WORKDIR nrn-7.4

# Compile NEURON.
RUN \
  ./configure --prefix=`pwd` --without-iv --with-nrnpython=$HOME/anaconda/bin/python && \
  make && \
  make install

# Install python interface
WORKDIR src/nrnpython
RUN python setup.py install

# Install PyNeuron-Toolbox
WORKDIR $HOME
RUN git clone https://github.com/ahwillia/PyNeuron-Toolbox
WORKDIR PyNeuron-Toolbox
RUN python setup.py install

# Install JSAnimation
WORKDIR $HOME
RUN git clone https://github.com/jakevdp/JSAnimation.git
RUN python JSAnimation/setup.py install


ENV PYTHONPATH $PYTHONPATH:$HOME/JSAnimation/:$HOME/PyNeuron-Toolbox/

# Switch back to non-root user privledges
WORKDIR $HOME
USER main
