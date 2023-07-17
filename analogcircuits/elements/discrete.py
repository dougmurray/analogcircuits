import numpy as np

def ind_imp(ind, freq):
    impedance =  0 + 1j *(2 * np.pi * freq * ind)
    return impedance

def cap_imp(cap, freq):
    impedance = 0 + 1j * -(1 / (2 * np.pi * freq * cap))
    return impedance

def parallel_res(*args):
    """
    Returns the equivalent resistance in Ohms of components in parallel.

    Parameters
    ----------
    args : float
        Resistance in Ohms.
    
    Returns
    -------
    parallel_res : float
        Equivalent resistance in Ohms.
    
    """
    product = 1
    for arg in args:
        product *= arg
    summed = 1
    for arg in args:
        summed += arg
    parallel_res = product / summed

    return parallel_res

def series_res(*args):
    """
    Returns the equivalent resistance in Ohms of components in series.

    Parameters
    ----------
    args : float
        Resistance in Ohms.
    
    Returns
    -------
    summed : float
        Equivalent resistance in Ohms.
    
    """
    summed = 1
    for arg in args:
        summed += arg
    
    return summed

def voltage_divider(voltage, res_one, res_two):
    """
    Returns the output voltage in V of components in a voltage divider.

    Parameters
    ----------
    voltage: float
        Input voltage in V.
    
    res_one : float
        Resistance in Ohms.
    
    res_two : float
        Resistance in Ohms.
    
    Returns
    -------
    divider_volt : float
        Output voltage in V.
    
    """
    divider_volt = voltage * (res_two / (res_one + res_two))
    return divider_volt