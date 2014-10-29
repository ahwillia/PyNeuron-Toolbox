import numpy as np
from morphology import get_all_sections

def ez_record(h,var='v',sections=None,order=None,\
              targ_names=None,cust_labels=None):
    """
    Records state variables across segments

    Args:
        h = hocObject to interface with neuron
        var = string specifying state variable to be recorded.
              Possible values are:
                  'v' (membrane potential)
                  'cai' (Ca concentration)
        sections = list of h.Section() objects to be recorded
        targ_names = list of section names to be recorded; alternative
                     passing list of h.Section() objects directly
                     through the "sections" argument above.
        cust_labels =  list of custom section labels

    Returns:
        data = list of h.Vector() objects recording membrane potential
        labels = list of labels for each voltage trace
    """
    if sections is None:
        if order == 'pre':
            sections = get_all_sections(h)
        else:
            sections = list(h.allsec())
    if targ_names is not None:
        old_sections = sections
        sections = []
        for sec in old_sections:
            if sec.name() in targ_names:
                sections.append(sec)

    data, labels = [], []
    for i in range(len(sections)):
        sec = sections[i]
        positions = np.linspace(0,1,sec.nseg+2)
        for position in positions[1:-1]:
            # record data
            data.append(h.Vector())
            if var is 'v':
                data[-1].record(sec(position)._ref_v)
            elif var is 'cai':
                data[-1].record(sec(position)._ref_cai)
            # determine labels
            if cust_labels is None:
                lab = sec.name()+'_'+str(round(position,5))
            else: 
                lab = cust_labels[i]+'_'+str(round(position,5))
            labels.append(lab)

    return data, labels

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
