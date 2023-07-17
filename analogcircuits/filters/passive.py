#!/usr/bin/env python3
# Run in analogcircuits: python3 -m analogcircuits.filters.passive

import numpy as np
import matplotlib.pyplot as plt
from analogcircuits.elements import(voltage_divider, cap_imp, ind_imp, parallel_res)

def rc_filter(res, cap):
    freq_corner = 1 / (2 * np.pi * res * cap)
    return freq_corner

def lc_filter(ind, cap):
    freq_corner = 1 / (2 * np.pi * np.sqrt(ind * cap))
    return freq_corner

def cr_filter(cap, res):
    freq_corner = 1 / (2 * np.pi * res * cap)
    return freq_corner

def cl_filter(cap, ind):
    freq_corner = 1 / (2 * np.pi * np.sqrt(ind * cap))
    return freq_corner

def filter_signal(freqs, imped_one, imped_two):
    voltage_amplitude = 1 # V
    voltage_offset = 0 # V
    voltage_in_freq_domain = voltage_amplitude * np.sin(2 * np.pi * freqs) + voltage_offset
    voltage_out_freq_domain = voltage_divider(voltage_in_freq_domain, imped_one, imped_two) # filters are voltage dividers
    return voltage_in_freq_domain, voltage_out_freq_domain

def filter_bode_plotter(freqs, vin, vout, corner_freq_text='Hz'):
    plt.semilogx(freqs, (20 * np.log10(vout/vin)))
    plt.grid(which='both')
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Gain (dB)")
    plt.title("Bode plot")
    plt.text(0.1, 0.1, f"{corner_freq_text} Hz")
    plt.show()

def user_input(args):
    match args:
        case "rc":
            print("Low-pass RC filter")
            res_one = float(input("res: "))
            cap_one = float(input("cap: "))
            rc_filter_freq_corner = rc_filter(res_one, cap_one)
            output_impedance = parallel_res(res_one, np.abs(cap_imp(cap_one, rc_filter_freq_corner)))
            print(f"Freq corner: {rc_filter_freq_corner} Hz")
            print(f"Output impedance: {output_impedance} Ohms at {rc_filter_freq_corner} Hz")
            freq_range = np.linspace(0.1, 10e6, num=10_000_000)
            cap_one_imp = np.abs(cap_imp(cap_one, freq_range))
            vin, vout = filter_signal(freq_range, res_one, cap_one_imp)
            filter_bode_plotter(freq_range, vin, vout, rc_filter_freq_corner)
        case "lc":
            print("Low-pass LC filter")
            ind_one = float(input("ind: "))
            cap_one = float(input("cap: "))
            lc_filter_freq_corner = lc_filter(ind_one, cap_one)
            output_impedance = parallel_res(np.abs(ind_imp(ind_one, lc_filter_freq_corner)), 
                                            np.abs(cap_imp(cap_one, lc_filter_freq_corner)))
            print(f"Freq corner: {lc_filter_freq_corner} Hz")
            print(f"Output impedance: {output_impedance} Ohms at {lc_filter_freq_corner} Hz")
            freq_range = np.linspace(0.1, 10e6, num=10_000_000)
            ind_one_imp = np.abs(ind_imp(ind_one, freq_range))
            cap_one_imp = np.abs(cap_imp(cap_one, freq_range))
            vin, vout = filter_signal(freq_range, ind_one_imp, cap_one_imp)
            filter_bode_plotter(freq_range, vin, vout, lc_filter_freq_corner)
        case "cr":
            print("High-pass CR filter")
            cap_one = float(input("cap: "))
            res_one = float(input("res: "))
            cr_filter_freq_corner = cr_filter(cap_one, res_one)
            output_impedance = parallel_res(np.abs(cap_imp(cap_one, cr_filter_freq_corner)), res_one)
            print(f"Freq corner: {cr_filter_freq_corner} Hz")
            print(f"Output impedance: {output_impedance} Ohms at {cr_filter_freq_corner} Hz")
            freq_range = np.linspace(0.1, 10e6, num=10_000_000)
            cap_one_imp = np.abs(cap_imp(cap_one, freq_range))
            vin, vout = filter_signal(freq_range, cap_one_imp, res_one)
            filter_bode_plotter(freq_range, vin, vout, cr_filter_freq_corner)
        case "cl":
            print("High-pass CL filter")
            cap_one = float(input("cap: "))
            ind_one = float(input("ind: "))
            cl_filter_freq_corner = cl_filter(cap_one, ind_one)
            output_impedance = parallel_res(np.abs(cap_imp(cap_one, cl_filter_freq_corner)), 
                                            np.abs(ind_imp(ind_one, cl_filter_freq_corner)))
            print(f"Freq corner: {cl_filter_freq_corner} Hz")
            print(f"Output impedance: {output_impedance} Ohms at {cl_filter_freq_corner} Hz")
            freq_range = np.linspace(0.1, 10e6, num=10_000_000)
            cap_one_imp = np.abs(cap_imp(cap_one, freq_range))
            ind_one_imp = np.abs(ind_imp(ind_one, freq_range))
            vin, vout = filter_signal(freq_range, cap_one_imp, ind_one_imp)
            filter_bode_plotter(freq_range, vin, vout, cl_filter_freq_corner)

        case "rl" | "lr":
            print("Why would you?")
        case _:
            print("Not a filter type.")

if __name__ == "__main__":
    import argparse
    my_parser = argparse.ArgumentParser(prog='filters', 
                                        description='Run `python filters.py rc`. For filters freqs.')
    my_parser.add_argument('filter', metavar='filter', type=str,
                           nargs='?', default="rc", help='Filter type (rc)')
    args = my_parser.parse_args()
    filter_type = args.filter
    user_input(filter_type)