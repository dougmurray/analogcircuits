#!/usr/bin/env python3
""" Operational Amplifier Noise Comparison

    This is based on the Analog Devices AN-940, which uses the 
    opamps voltage and current noise to make an equivalent resistance
    to compare with the source resistance.

    Author: Douglass Murray
"""
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def resistor_vnoise(res, bandwidth=1):
    """ Calculates Johnson-Nyquist noise (thermal noise) of resistors.
    Default temp is room temp, 20 C.  

    Args:
        res: resistor value in Ohms
        bandwidth: bandwidth in Hz (default 1)
    
    Returns:
        vnoise: voltage noise of resistor in V/sqrt(Hz)
    """
    k = 1.38e-23 # J/K, Boltzmann constant J/K
    room_temp = 293.15 # K, 20 C
    vnoise = np.sqrt(4 * k * room_temp * bandwidth * res)
    return vnoise

def resistor_inoise(res, bandwidth=1):
    """ Calculates the Johnson-Nyquist current noise of resistor.
    Default temp is room temp, 20 C.
    
    Args:
        res: resistor in Ohms
        bandwidth: bandwidth in Hz
    
    Returns:
        inoise: current noise in A/sqrt(Hz)
    """
    k = 1.38e-23 # J/K, Boltzmann constant J/K
    room_temp = 293.15 # K, 20 C
    inoise = np.sqrt((4 * k * room_temp * bandwidth) / res)
    return inoise

def opamp_Rs_op(vnoise_opamp, inoise_opamp):
    """ Opamp equvilant resistance based on its voltage and current noise.  
    Helper function.  Based on Analog Devices AN-940.
    
    Args:
        vnoise_opamp: opamp's voltage noise in V/sqrt(Hz), usually at 1 kHz
        inoise_opamp: opamp's current noise in A/sqrt(Hz), usually at 1 kHz
    
    Return:
        Rs_op: resistance in Ohms, based on vnoise/inoise of opamp
    """
    Rs_op = vnoise_opamp / inoise_opamp
    return Rs_op

if __name__ == "__main__":
    np.seterr(divide='ignore')
    my_parser = argparse.ArgumentParser(prog='opamp-noise-choice', description='Operational Amplifier Noise Comparison')
    my_parser.add_argument('source_resistance', metavar='source_resistance', type=float, nargs='?', default=1000,  help='Source resistance in Ohms (1000 Ohms)')
    args = my_parser.parse_args()

    filename = "ideal-low-noise-opamps.png"
    bw_low = 1 # Hz, bandwidth
    # source_resistance = 1000
    # source_resistance = float(sys.argv[1])
    source_resistance = args.source_resistance
    source_resistance_noise = resistor_vnoise(source_resistance, bw_low)

    source_resistance_range = np.linspace(10, 4e8) # Ohms
    source_resistance_range_vnoise = resistor_vnoise(source_resistance_range, bw_low)
    plt.loglog(source_resistance_range, source_resistance_range_vnoise, label="Johnson Noise")

    analog_devices_opamps = pd.read_csv("./data/ADIParametricSearch/Custom Data Format.csv")
    analog_devices_opamp_vnoise = analog_devices_opamps['VNoise Density (typ) V/rtHz'].to_numpy()
    analog_devices_opamp_inoise = analog_devices_opamps['Current Noise Density (typ)'].to_numpy()
    analog_devices_opamp_Rs_op = opamp_Rs_op(analog_devices_opamp_vnoise, analog_devices_opamp_inoise)
    plt.loglog(analog_devices_opamp_Rs_op, analog_devices_opamp_vnoise, '.', label="Opamps")
    plt.hlines(source_resistance_noise, xmin=source_resistance, xmax=4e8, linestyles="dashed", label="source_resistance")  # source reference
    plt.loglog(source_resistance, source_resistance_noise, 'o', mfc='none') # visual candy, circle as point of source resistance

    # just cannot get to work
    # source_range = np.linspace(10, source_resistance)
    # source_vnoise_range = resistor_vnoise(source_range, bw_low)
    # plt.loglog(source_range, -(np.log10(source_vnoise_range)/ np.log10(source_range)) * source_range, '--', label="decade")
    # plt.loglog(np.flip(source_range), np.flip(source_vnoise_range) / np.log10(np.flip(source_range)), '--', label="decade")
    # plt.loglog(np.flip(source_range), -np.log(np.flip(source_vnoise_range) / np.flip(source_range)), '--', label="decade")

    # for labeling the opamps which are lower noise than source resistance
    ideal_opamps = np.array([])
    for i, opamp_rs_noise in enumerate(analog_devices_opamp_vnoise):
        if opamp_rs_noise < source_resistance_noise:
            plt.annotate(analog_devices_opamps['Part Number'][i], (analog_devices_opamp_Rs_op[i], analog_devices_opamp_vnoise[i]))
            ideal_opamps = np.append(ideal_opamps, analog_devices_opamps['Part Number'][i])
        else:
            pass
    
    print(f"Ideal opamps for source resistance {source_resistance} Ohms:")
    print(type(ideal_opamps))
    np.savetxt("ideal-opamps.txt", ideal_opamps, delimiter = ",", fmt='%s')
    print("Saved %s/%s" % (os.getcwd(), "ideal-opamps.txt"))

    plt.xlabel("Source Resistance [Ohm]")
    plt.ylabel("Noise [V/sqrt(Hz)]")
    plt.legend()
    plt.grid(which='both')
    plt.savefig(filename, dpi=800, pad_inches=0.1)
    print("Saved %s/%s" % (os.getcwd(), filename))
    plt.show()