PyNeuron-Toolbox
================

The [NEURON simulation environment](http://www.neuron.yale.edu/neuron/) is one of the most popular options for simulating multi-compartment neuron models. [Hines et al. (2009)](http://journal.frontiersin.org/Journal/10.3389/neuro.11.001.2009/abstract) developed a module that allowed users to execute simulations from python. This option appears to be very popular with users.

However, much of the data analysis capabilities of NEURON (e.g. [shape plots](http://www.oberlin.edu/OCTET/HowTo/NEURON/B2_RealisticMorph.html)) are still limited to the traditional environment in [hoc](http://en.wikipedia.org/wiki/Hoc_(programming_language)). The toolbox provides some functions to do data analysis and visualization in matplotlib. One of the advantages of this approach is that analysis can be easily shared with researchers that use python, even if they are unfamiliar with NEURON or hoc.

**Disclaimer:** This code is only a side project at the moment. Use with caution and let me know if you find any unexpected behaviors. Feature requests are also welcome.

Installation
=============
Download or clone this repository, then run:

`python setup.py install`

Tutorials
==========
At the moment, only a few basic functions are included in the toolbox. These mostly relate to visualizing the morphology of model cells. [Click here for a tutorial on the morphology toolbox](http://alexhwilliams.info/code/pyneuron_morph.html) - the animations seem to work best when viewed in Chrome. 

Future Plans
============
I would like to add functions to support:

* [Morphoelectric Transforms](http://zadorlab.cshl.edu/PDF/zador-thesis1993.pdf)
