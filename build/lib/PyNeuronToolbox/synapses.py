from __future__ import division
import numpy as np

def add_exp2(h,seg,spktimes,e=0,tau1=0.5,tau2=20,weight=0.001):
    """
    Adds a double-exponential synapse at seg, with spikes
    specified by the list/np.array spktimes. Optional arguments
    specify parameters for the synapse. Returns a list of
    hocObjects that must be kept in memory (see below).

    IMPORTANT: This function requires that you have the vecevent.mod
               file compiled and loaded into python. This file can
               be found in nrn/share/examples/nrniv/netcon/

    IMPORTANT: Neuron requires that you keep the Exp2Syn, VecStim,
               NetCon, and Vector objects in memory during the
               simulation. You will also need these objects if
               you wish to alter the weight of the synapse
               or other parameters during the simulation.
    """
    syn = h.Exp2Syn(seg)
    syn.e = 0
    syn.tau1 = 0.5
    syn.tau2 = 20
    vs = h.VecStim()
    vec = h.Vector(np.sort(spktimes)) # Spend a bit of overhead to make sure spktimes are sorted
    vs.play(vec)
    nc = h.NetCon(vs,syn)
    nc.weight[0] = weight
    return [syn,vs,nc,vec]            # All these things need to be kept in memory
