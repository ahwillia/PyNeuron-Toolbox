"""
Load SWC files and instantiate inside a Python object.

This module may be used as a library or run as a script for a demo.

When run as a script, e.g. via

    python load_swc.py

it pulls the morphology for c91662 from NeuroMorpho.Org.

For more on NeuroMorpho.Org, see:

    Ascoli GA, Donohue DE, Halavi M. (2007) NeuroMorpho.Org: a central
    resource for neuronal morphologies.J Neurosci., 27(35):9247-51

The demo morphology is from:

    Ishizuka, N., Cowan, W. M., & Amaral, D. G. (1995). A quantitative
    analysis of the dendritic organization of pyramidal cells in the rat
    hippocampus. Journal of Comparative Neurology, 362(1), 17-45.

Minimal example:

    class Cell:
        def __str__(self):
            return 'neuron'

    cell = Cell()
    load_swc(filename, cell)

NOTE:

    Subtle differences may exist between morphologies instantiated with this
    module and those instantiated directly from the Import3D GUI due to
    rounding variations.

"""


def load_swc(filename, cell, use_axon=True, xshift=0, yshift=0, zshift=0):
    """Load an SWC from filename and instantiate inside cell.

    filename -- the filename of the SWC file
    use_axon -- include the axon? Default: True (yes)... set to False to not instantiate the axon
    xshift, yshift, zshift -- use to position the cell

    """
    from neuron import h, gui

    name_form = {1: 'soma[%d]', 2: 'axon[%d]', 3: 'dend[%d]', 4: 'apic[%d]'}

    # a helper library, included with NEURON
    h.load_file('import3d.hoc')

    # load the data. Use Import3d_SWC_read for swc, Import3d_Neurolucida3 for
    # Neurolucida V3, Import3d_MorphML for MorphML (level 1 of NeuroML), or
    # Import3d_Eutectic_read for Eutectic.
    morph = h.Import3d_SWC_read()
    morph.input(filename)

    # easiest to instantiate by passing the loaded morphology to the Import3d_GUI
    # tool; with a second argument of 0, it won't display the GUI, but it will allow
    # use of the GUI's features
    i3d = h.Import3d_GUI(morph, 0)

    # get a list of the swc section objects
    swc_secs = i3d.swc.sections
    swc_secs = [swc_secs.object(i) for i in xrange(int(swc_secs.count()))]

    # initialize the lists of sections
    cell.soma, cell.apic, cell.dend, cell.axon = [], [], [], []
    sec_list = {1: cell.soma, 2: cell.axon, 3: cell.dend, 4: cell.apic}

    # name and create the sections
    real_secs = {}
    for swc_sec in swc_secs:
        cell_part = int(swc_sec.type)

        # skip everything else if it's an axon and we're not supposed to
        # use it... or if is_subsidiary
        if (not(use_axon) and cell_part == 2) or swc_sec.is_subsidiary:
            continue
        
        # figure out the name of the new section
        if cell_part not in name_form:
            raise Exception('unsupported point type')
        name = name_form[cell_part] % len(sec_list[cell_part])

        # create the section
        sec = h.Section(cell=cell, name=name)
        
        # connect to parent, if any
        if swc_sec.parentsec is not None:
            sec.connect(real_secs[swc_sec.parentsec.hname()](swc_sec.parentx))

        # define shape
        if swc_sec.first == 1:
            h.pt3dstyle(1, swc_sec.raw.getval(0, 0), swc_sec.raw.getval(1, 0),
                        swc_sec.raw.getval(2, 0), sec=sec)

        j = swc_sec.first
        xx, yy, zz = [swc_sec.raw.getrow(i).c(j) for i in xrange(3)]
        dd = swc_sec.d.c(j)
        if swc_sec.iscontour_:
            # never happens in SWC files, but can happen in other formats supported
            # by NEURON's Import3D GUI
            raise Exception('Unsupported section style: contour')

        if dd.size() == 1:
            # single point soma; treat as sphere
            x, y, z, d = [dim.x[0] for dim in [xx, yy, zz, dd]]
            for xprime in [x - d / 2., x, x + d / 2.]:
                h.pt3dadd(xprime + xshift, y + yshift, z + zshift, d, sec=sec)
        else:
            for x, y, z, d in zip(xx, yy, zz, dd):
                h.pt3dadd(x + xshift, y + yshift, z + zshift, d, sec=sec)

        # store the section in the appropriate list in the cell and lookup table               
        sec_list[cell_part].append(sec)    
        real_secs[swc_sec.hname()] = sec

    cell.all = cell.soma + cell.apic + cell.dend + cell.axon

def demo(filename='morph.swc'):
    """demo test program"""
    class Cell:
        def __str__(self):
            return 'neuron'

    cell = Cell()
    load_swc(filename, cell)
    return cell

if __name__ == '__main__':
    from neuron import h, gui

    # pull the morphology for the demo from NeuroMorpho.Org
    import neuromorphoorg
    with open('c91662.swc', 'w') as f:
        f.write(neuromorphoorg.morphology('c91662'))

    cell = demo('c91662.swc')

    import morphology
    from matplotlib import pyplot
    from mpl_toolkits.mplot3d import Axes3D
    fig = pyplot.figure()
    ax = fig.gca(projection='3d')
    morphology.shapeplot(h, ax, sections=cell.all, color='k')
    pyplot.show()