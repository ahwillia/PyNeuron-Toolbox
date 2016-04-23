"""
Scraper for querying NeuroMorpho.Org from Python.

For more on NeuroMorpho.Org, see:

    Ascoli GA, Donohue DE, Halavi M. (2007) NeuroMorpho.Org: a central
    resource for neuronal morphologies.J Neurosci., 27(35):9247-51

Run this file as a stand-alone script for a demo. The demo queries NeuroMorpho.Org
in general, and provides extra information about the cell mb100318-a which is
associated with the publication:

    Bagnall, M. W., Hull, C., Bushong, E. A., Ellisman, M. H., & Scanziani, M. (2011).
    Multiple clusters of release sites formed by individual thalamic afferents onto
    cortical interneurons ensure reliable transmission. Neuron, 71(1), 180-194.

As a web-scraper, this module may break if the website structure changes, but it
was known to work as of April 2, 2016.

To get a list of all cell types, species, or regions, call cell_types(), species(),
or regions(), respectively.

Given a type from one of these lists, get the matching cell names via cell_names.
e.g. cell_names('blowfly')

To get the metadata for a given cell name, use metadata.
e.g. metadata('mb100318-a')

To get the morphology for a given cell name, use morphology.
e.g. morphology('mb100318-a')

An optional format keyword argument allows selecting between the original and the
standardized versions.
"""
import urllib2
import re
import json
import base64

_cache = {}

def _read_neuromorpho_table(bywhat):
    """Helper function, reads data from NeuroMorpho.Org, stores in cache."""
    html = urllib2.urlopen('http://neuromorpho.org/by%s.jsp' % bywhat).read()
    result = [m.strip() for m in re.findall("maketable\('(.*?)'\)", html)]
    _cache[bywhat] = set(result)
    return result

def cell_types():
    """Return a list of all cell types."""
    return _read_neuromorpho_table('cell')

def species():
    """Return a list of all species."""
    return _read_neuromorpho_table('species')

def regions():
    """Return a list of all the brain regions."""
    return _read_neuromorpho_table('region')

def cell_names(category):
    """Return a list of all the names of cells of a given cell type, species, or region.

    Examples:

        cell_names('Aspiny')
        cell_names('blowfly')
        cell_names('amygdala')
    """
    # figure out if category is a cell type, species, or region
    # check the cached sets first
    for bywhat, items in _cache.iteritems():
        if category in items:
            return _get_data_for_by(bywhat, category)
    # no luck: try all three options
    for bywhat in ['cell', 'region', 'species']:
        result = _get_data_for_by(bywhat, category)
        if result:
            return result
    return []

def _get_data_for_by(bywhat, category):
    """Helper function for cell_names."""
    query_code = bywhat if bywhat != 'cell' else 'class'

    html = urllib2.urlopen('http://neuromorpho.org/getdataforby%s.jsp?%s=%s' % (bywhat, query_code, category.replace(' ', '%20'))).read()
    return [m for m in re.findall("neuron_name=(.*?)'", html)]

def metadata(neuron_name):
    """Return a dict of the metadata for the specified neuron.

    Example:

        metadata('mb100318-a')
    """
    html = urllib2.urlopen('http://neuromorpho.org/neuron_info.jsp?neuron_name=%s' % neuron_name).read()
    # remove non-breaking spaces
    html = html.replace('&nbsp;', ' ')

    # remove units
    html = html.replace('&#956;m<sup>2</sup>', ' ')
    html = html.replace('&#956;m', ' ')
    html = html.replace('&deg;', ' ')
    html = html.replace('<b>x</b>', ' ')
    html = html.replace('<sup>3</sup>', '')
    html2 = html.replace('\n', '')
    keys = [i[1][:-3].strip() for i in re.findall('<td align="right" width="50%"(.*?)>(.*?)</td>', html2)]
    values = [i[1].strip() for i in re.findall('<td align="left"(.*?)>(.*?)</td>', html2)[2:]]

    return dict(zip(keys, values))

def morphology(neuron_name, format='swc'):
    """Return the morphology associated with a given name.

    Format options:

        swc -- always "stanadardized" file format (default)
        original -- original

    Example:

        morphology('mb100318-a', format='swc')
        morphology('mb100318-a', format='original')
    """
    url_paths_from_format = {'swc': 'CNG%20Version', 'original': 'Source-Version'}
    assert(format in url_paths_from_format)
    # locate the path to the downloads
    html = urllib2.urlopen('http://neuromorpho.org/neuron_info.jsp?neuron_name=%s' % neuron_name).read()
    if format == 'swc':
        url = re.findall("<a href=dableFiles/(.*?)>Morphology File \(Standardized", html)[0]
    else:
        url = re.findall("<a href=dableFiles/(.*?)>Morphology File \(Original", html)[0]
    return urllib2.urlopen('http://NeuroMorpho.org/dableFiles/%s' % url).read()

def download(neuron_name, filename=None):
    format = 'swc'
    if filename is not None and len(filename.split('.'))==0:
        filename = base64.urlsafe_b64encode(filename+'.'+format)
    if filename is None:
        filename = base64.urlsafe_b64encode(neuron_name+'.'+format)
    with open(filename, 'w') as f:
        f.write(morphology(neuron_name, format=format))

if __name__ == '__main__':
    print 'Demo of reading data from NeuroMorpho.Org'
    print

    for string, fn in zip(['cell types', 'brain regions', 'species'], [cell_types, regions, species]):
        print 'All %s:' % string
        print ', '.join(fn())
        print
    for category in ['amygdala', 'blowfly', 'Aspiny']:
        print 'All %s:' % category
        print ', '.join(cell_names(category))
        print
    print 'Metadata for mb100318-a:'
    print json.dumps(metadata('mb100318-a'), indent=4)
    print
    print 'Morphology (standardized) for mb100318-a (first 10 lines):'
    print '\n'.join(morphology('mb100318-a', format='standardized').split('\n')[:10])