from distutils.core import setup

DESCRIPTION = "Makes interactive plots for simulations in NEURON"
LONG_DESCRIPTION = DESCRIPTION
NAME = "PyNeuronToolbox"
AUTHOR = "Alex Williams"
AUTHOR_EMAIL = "alex.h.willia@gmail.com"
MAINTAINER = "Alex Williams"
MAINTAINER_EMAIL = "alex.h.willia@gmail.com"
DOWNLOAD_URL = 'http://github.com/ahwillia/PyNeuronToolbox'
LICENSE = 'BSD'

VERSION = '0.1'

setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      maintainer=MAINTAINER,
      maintainer_email=MAINTAINER_EMAIL,
      url=DOWNLOAD_URL,
      download_url=DOWNLOAD_URL,
      license=LICENSE,
      packages=['PyNeuronToolbox'],
      package_data={}
     )
