from __future__ import division
import numpy as np
import pylab as plt
from matplotlib.pyplot import cm

def sequential_spherical(xyz):
    """
    Converts sequence of cartesian coordinates into a sequence of
    line segments defined by spherical coordinates.
    
    Args:
        xyz = 2d numpy array, each row specifies a point in
              cartesian coordinates (x,y,z) tracing out a
              path in 3D space.
    
    Returns:
        r = lengths of each line segment (1D array)
        theta = angles of line segments in XY plane (1D array)
        phi = angles of line segments down from Z axis (1D array)
    """
    d_xyz = np.diff(xyz,axis=0)
    
    r = np.linalg.norm(d_xyz,axis=1)
    theta = np.arctan2(d_xyz[:,1], d_xyz[:,0])
    hyp = d_xyz[:,0]**2 + d_xyz[:,1]**2
    phi = np.arctan2(np.sqrt(hyp), d_xyz[:,2])
    
    return (r,theta,phi)

def spherical_to_cartesian(r,theta,phi):
    """
    Simple conversion of spherical to cartesian coordinates
    
    Args:
        r,theta,phi = scalar spherical coordinates
    
    Returns:
        x,y,z = scalar cartesian coordinates
    """
    x = r * np.sin(phi) * np.cos(theta)
    y = r * np.sin(phi) * np.sin(theta)
    z = r * np.cos(phi)
    return (x,y,z)

def find_coord(targ_length,xyz,rcum,theta,phi):
    """
    Find (x,y,z) ending coordinate of segment path along section
    path.

    Args:
        targ_length = scalar specifying length of segment path, starting
                      from the begining of the section path
        xyz = coordinates specifying the section path
        rcum = cumulative sum of section path length at each node in xyz
        theta, phi = angles between each coordinate in xyz
    """
    #   [1] Find spherical coordinates for the line segment containing
    #           the endpoint.
    #   [2] Find endpoint in spherical coords and convert to cartesian
    i = np.nonzero(rcum <= targ_length)[0][-1]
    if i == len(theta):
        return xyz[-1,:]
    else:
        r_lcl = targ_length-rcum[i] # remaining length along line segment
        (dx,dy,dz) = spherical_to_cartesian(r_lcl,theta[i],phi[i])
        return xyz[i,:] + [dx,dy,dz]

def interpolate_jagged(xyz,nseg):
    """
    Interpolates along a jagged path in 3D
    
    Args:
        xyz = section path specified in cartesian coordinates
        nseg = number of segment paths in section path
        
    Returns:
        interp_xyz = interpolated path
    """
    
    # Spherical coordinates specifying the angles of all line
    # segments that make up the section path
    (r,theta,phi) = sequential_spherical(xyz)
    
    # cumulative length of section path at each coordinate
    rcum = np.append(0,np.cumsum(r))

    # breakpoints for segment paths along section path
    breakpoints = np.linspace(0,rcum[-1],nseg+1)
    np.delete(breakpoints,0)
    
    # Find segment paths
    seg_paths = []
    for a in range(nseg):
        path = []
        
        # find (x,y,z) starting coordinate of path
        if a == 0:
            start_coord = xyz[0,:]
        else:
            start_coord = end_coord # start at end of last path
        path.append(start_coord)

        # find all coordinates between the start and end points
        start_length = breakpoints[a]
        end_length = breakpoints[a+1]
        mid_boolean = (rcum > start_length) & (rcum < end_length)
        mid_indices = np.nonzero(mid_boolean)[0]
        for mi in mid_indices:
            path.append(xyz[mi,:])

        # find (x,y,z) ending coordinate of path
        end_coord = find_coord(end_length,xyz,rcum,theta,phi)
        path.append(end_coord)

        # Append path to list of segment paths
        seg_paths.append(np.array(path))
    
    # Return all segment paths
    return seg_paths

def get_section_path(h,sec):
    n3d = int(h.n3d(sec=sec))
    xyz = []
    for i in range(0,n3d):
        xyz.append([h.x3d(i,sec=sec),h.y3d(i,sec=sec),h.z3d(i,sec=sec)])
    xyz = np.array(xyz)
    return xyz

def shapeplot(h,ax,sections=None,lw=1):
    """
    Plots a 3D shapeplot

    Args:
        h = hocObject to interface with neuron
        ax = matplotlib axis for plotting
        sections = list of h.Section() objects to be plotted
        lw = linewidth
        res = resolution(how many points to sample along paths)

    Returns:
        lines = list of line objects making up shapeplot
    """
    
    # Default is to plot all sections
    if sections is None:
        sections = list(h.allsec())

    lines = []
    for sec in sections:
        xyz = get_section_path(h,sec)
        seg_paths = interpolate_jagged(xyz,sec.nseg)
        for path in seg_paths:
            line, = plt.plot(path[:,0], path[:,1], path[:,2], \
                             '-k',lw=lw)
            lines.append(line)

    return lines

def shapeplot_animate(v,lines,nframes,x_min=-80,x_max=50,cmap=cm.YlOrBr_r):
    """ Returns animate function updates color of shapeplot """
    def animate(i):
        i_t = int((i/nframes)*v.shape[0])
        for i_seg in range(v.shape[1]):
            lines[i_seg].set_color(cmap(int((v[i_t,i_seg]-x_min)*255/(x_max-x_min))))

    return animate

def mark_locations(h,section,locs,markspec='or',**kwargs):
    """
    Marks one or more locations on along a section. Could be used to
    mark the location of a recording or electrical stimulation.

    Args:
        h = hocObject to interface with neuron
        section = reference to section
        locs = float between 0 and 1, or array of floats
        optional arguments specify details of marker

    Returns:
        line = reference to plotted markers
    """

    # get list of cartesian coordinates specifying section path
    xyz = get_section_path(h,section)
    (r,theta,phi) = sequential_spherical(xyz)
    rcum = np.append(0,np.cumsum(r))

    # convert locs into lengths from the beginning of the path
    if type(locs) is float:
        locs = np.array([locs])
    if type(locs) is list:
        locs = np.array(locs)
    lengths = locs*rcum[-1]

    # find cartesian coordinates for markers
    xyz_marks = []
    for targ_length in lengths:
        xyz_marks.append(find_coord(targ_length,xyz,rcum,theta,phi))
    xyz_marks = np.array(xyz_marks)

    # plot markers
    line, = plt.plot(xyz_marks[:,0], xyz_marks[:,1], \
                     xyz_marks[:,2], markspec, **kwargs)
    return line
