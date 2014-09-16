import numpy as np

def ez_record(h,var='v',sections=None,secnames=None):
    """
    Plots a 3D shapeplot

    Args:
        h = hocObject to interface with neuron
        var = string specifying state variable to be recorded.
              Possible values are:
                  'v' (membrane potential)
                  'cai' (Ca concentration)
        sections = list of h.Section() objects to be recorded
        secnames = custom list of section names

    Returns:
        data = list of h.Vector() objects recording membrane potential
        labels = list of labels for each voltage trace
    """
    if sections is None:
        sections = list(h.allsec())

    data, labels = [], []
    for i in range(len(sections)):
        sec = sections[i]
        for position in np.linspace(0,1,sec.nseg):
            # record data
            data.append(h.Vector())
            if var is 'v':
                data[-1].record(sec(position)._ref_v)
            elif var is 'cai':
                data[-1].record(sec(position)._ref_cai)
            # determine label
            if secnames is None:
                lab = sec.name()+'_'+str(round(position,5))
            else: 
                lab = secnames[i]+'_'+str(round(position,5))
            labels.append(lab)

    return (data,labels)

def ez_convert(data):
    """
    Takes data, a list of h.Vector() objects filled with data, and converts
    it into a 2d numpy array, data_clean. This should be used together with
    the ez_record command. 
    """
    data_clean = np.empty((len(data[0]),len(data)))
    for (i,vec) in enumerate(data):
        data_clean[:,i] = vec.to_python()
    return data_clean
