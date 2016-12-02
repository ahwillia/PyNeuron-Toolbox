def ivcurve(mechanism_name, i_type, vmin=-100, vmax=100, deltav=1, transient_time=50, test_time=50, rs=1, vinit=-665):
    """
    Returns the (peak) current-voltage relationship for an ion channel.

    Args:
        mechanism_name = name of the mechanism (e.g. hh)
        i_type = which current to monitor (e.g. ik, ina)
        vmin = minimum voltage step to test
        vmax = maximum voltage step to test
        deltav = increment of voltage
        transient_time = how long to ignore for initial conditions to stabilize (ms)
        test_time = duration of the voltage clamp tests (ms)
        rs = resistance of voltage clamp in MOhm
        vinit = initialization voltage

    Returns:
        i = iterable of peak currents (in mA/cm^2)
        v = iterable of corresponding test voltages

    Note:
        The initialization potential (vinit) may affect the result. For example, consider
        the Hodgkin-Huxley sodium channel; a large fraction are inactivated at rest. Using a
        strongly hyperpolarizing vinit will uninactivate many channels, leading to more
        current.
    """
    from neuron import h
    import numpy
    h.load_file('stdrun.hoc')
    sec = h.Section()
    sec.insert(mechanism_name)
    sec.L = 1
    sec.diam = 1
    seclamp = h.SEClamp(sec(0.5))
    seclamp.amp1 = vinit
    seclamp.dur1 = transient_time
    seclamp.dur2 = test_time 
    seclamp.rs = rs
    i_record = h.Vector()
    i_record.record(sec(0.5).__getattribute__('_ref_' + i_type))
    result_i = []
    result_v = numpy.arange(vmin, vmax, deltav)
    for test_v in result_v:
        seclamp.amp2 = test_v
        h.finitialize(vinit)
        h.continuerun(transient_time)
        num_transient_points = len(i_record)
        h.continuerun(test_time + transient_time)
        i_record2 = i_record.as_numpy()[num_transient_points:]
        baseline_i = i_record2[0]
        i_record_shift = i_record2 - baseline_i
        max_i = max(i_record_shift)
        min_i = min(i_record_shift)
        peak_i = max_i if abs(max_i) > abs(min_i) else min_i
        peak_i += baseline_i
        result_i.append(peak_i)
    return result_i, result_v

if __name__ == '__main__':
    from matplotlib import pyplot
    import numpy
    from neuron import h
    h.CVode().active(1)
    ik, v = ivcurve('hh', 'ik')
    pyplot.plot(v, ik, label='ik')
    ina, v = ivcurve('hh', 'ina', vinit=-100)
    pyplot.plot(v, ina, label='ina')
    pyplot.xlabel('v (mV)')
    pyplot.ylabel('current (mA/cm^2)')
    pyplot.legend()
    pyplot.show()
