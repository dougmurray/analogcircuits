#!/usr/bin/env python3
import numpy as np

def resistor_thermal_noise(res):
    "Johnson-Nyquist noise, aka thermal noise"
    k = 1.38e-23 # J/K, Boltzmann constant
    temp = 289 # K, room temperature
    thermal_noise = np.sqrt(4 * k * temp * res)
    return thermal_noise

def parallel_res(res_one, res_two):
    "Equivalent resistance of resistors parallel."
    parallel_res = (res_one * res_two) / (res_one + res_two)
    return parallel_res

def amplitude_to_rms(amplitude):
    "Converts amplitude to rms."
    return amplitude / np.sqrt(2)

def rms_to_amplitude(rms):
    "Converts rms to amplitude."
    return np.sqrt(2) * rms

def snr(signal_rms, noise_rms):
    "Signal to Noise in dB."
    signal_amplitude = rms_to_amplitude(signal_rms)
    noise_amplitude = rms_to_amplitude(noise_rms)
    snr_dB = 20 * np.log10(signal_amplitude/noise_amplitude)
    return snr_dB

def opamp_current_noise(Req, opamp_input_current_noise_A_per_sqrtHz):
    current_noise = Req * opamp_input_current_noise_A_per_sqrtHz
    return current_noise

def noise_gain(feedback_res, res_g):
    gain_of_noise = 1 + feedback_res / res_g # ALWAYS! Regardless of opamp config
    return gain_of_noise

def opamp_broadband_noise(opamp_GBW, noise_gain, filter_order=1.57):
    "BW_n of opamp.  If there is a feedback cap, or RC filter, then DO NOT USE THIS"
    broadband_noise_freq = filter_order * (opamp_GBW / noise_gain) # Hz
    return broadband_noise_freq

def opamp_configuration(opamp_config=True):
    # noninverting_config
    if opamp_config == True:
        gain = 1 + res_feedback / res_g
    elif opamp_config == True:
        gain = res_feedback / res_g
    else:
         pass 
    return gain

def total_input_noise_rms(opamp_input_voltage_noise, input_current_noise, 
                          resistors_voltage_noise, broadband_noise, filter_res=None, filter_cap=None):
    "Total input voltage noise in Vrms."
    if filter_res or filter_cap:
        rc_freq = 1 / (2 * np.pi * filter_res * filter_cap)
        total_input_voltage_noise = np.sqrt(opamp_input_voltage_noise**2 
                                                     + input_current_noise**2 
                                                     + resistors_voltage_noise**2) * np.sqrt(1.57 * rc_freq) # Vrms
    else:
        total_input_voltage_noise = np.sqrt(opamp_input_voltage_noise**2 
                                            + input_current_noise**2 
                                            + resistors_voltage_noise**2) * np.sqrt(broadband_noise) # Vrms  
    return total_input_voltage_noise

def total_output_noise_rms(input_voltage_noise, opamp_gain):
    "Total output voltage noise in Vrms."
    total_output_voltage_noise = input_voltage_noise * opamp_gain # Vrms
    return total_output_voltage_noise

def resistor_or_opamp_noise_dominant(resistors_voltage_noise, opamp_input_voltage_noise):
    "Determines whether opamp input voltage noise or resistor thermal noise is dominant noise source."
    # Is resistor noise or opamp voltage noise dominant
    if (3 * resistors_voltage_noise) > opamp_input_voltage_noise:
        print("\nBad, resistor noise is dominant over opamp voltage noise.")
        print("Try to reduce feedback resistor values.")
        print("Low noise opamp not necessary.")
        ignore_resistor_noise = False # cannot ignore the resistor noise
    elif opamp_input_voltage_noise > (3 * resistors_voltage_noise):
        print("\nGood, opamp voltage noise is dominant over resistor noise.")
        print("Ensure to use a low noise opamp.")
        ignore_resistor_noise = True
    else:
        print("\nNeither opamp votlage noise nor resistor noise is dominant.")

def current_noise_or_opamp_noise_dominant(input_current_noise, opamp_input_voltage_noise):
    "Determines whether opamp input voltage noise or (opamp_current_noise * Req) noise is dominant noise source."
    # Is current or voltage noise dominant
    if opamp_input_voltage_noise > (3 * input_current_noise):
        print("\nOpamp noise dominant over current noise.")
        ignore_current_noise = True
    elif (3 * input_current_noise) > opamp_input_voltage_noise:
        print("\nCurrent noise dominant over voltage noise.")
        print("Try to reduce feedback resistor values.")
        print("Try using a JFET/CMOS opamp.")
        ignore_current_noise = False # cannot ignore the current noise 
    else:
        print("\nNeither current nor voltage noise is dominant.")

def broadband_or_white_noise_dominant(opamp_GBW, opamp_noise_gain):
    "Determines whether broadband noise or 1/f noise is dominant noise source.  Usually it is broadband."
    # Is broadband or 1/f noise dominant (protip, if bandwidth > 10kHz, ignore 1/f)
    broadband_noise = opamp_broadband_noise(opamp_GBW, opamp_noise_gain)
    if broadband_noise > (10 * opamp_freq_corner):
        print("\nBroadband noise is dominant over 1/f noise.")
        print(f"Broadband noise: {broadband_noise} Hz")
    elif (10 * opamp_freq_corner) > broadband_noise:
        print("\n1/f noise is dominant over broadband noise.")
        print("Ensure to use low 0.1 Hz to 10 Hz noise opamp!")
    else:
        print("\nNeither broadband nor 1/f noise dominant.")

if __name__ == "__main__":
    import argparse
    
    my_parser = argparse.ArgumentParser(prog='opamp-total-output-noise', 
                                        description='Total output noise of opamp')
    my_parser.add_argument('opamp_input_voltage_noise', 
                           metavar='opamp_input_voltage_noise', 
                           type=float, nargs='?', default=1.0e-9,  
                           help='opamp input voltage noise')
    my_parser.add_argument('opamp_input_current_noise', 
                           metavar='opamp_input_current_noise', 
                           type=float, nargs='?', default=21.7e-12, 
                           help='opamp input current noise')
    my_parser.add_argument('opamp_GBW', metavar='opamp_GBW', 
                           type=float, nargs='?', default=80e6, 
                           help='opamp gain bandwidth')
    my_parser.add_argument('opamp_freq_corner', metavar='opamp_freq_corner', 
                           type=float, nargs='?', default=20, 
                           help='opamp noise corner freq (from graph)')
    my_parser.add_argument('res_feedback', metavar='res_feedback', 
                           type=float, nargs='?', default=100e3, 
                           help='feedback resistance')
    my_parser.add_argument('res_g', metavar='res_g', 
                           type=float, nargs='?', default=1e3, 
                           help='res_g resistance')
    my_parser.add_argument('opamp_config', metavar='opamp_config', 
                           type=float, nargs='?', default=True, 
                           help='Is opamp config noninv (True) or inv (False)')
    args = my_parser.parse_args()

    # Opamp properties
    opamp_input_voltage_noise = args.opamp_input_voltage_noise
    opamp_input_current_noise = args.opamp_input_current_noise
    opamp_GBW = args.opamp_GBW
    opamp_freq_corner = args.opamp_freq_corner
    res_feedback = args.res_feedback
    res_g = args.res_g
    opamp_config = args.opamp_config

    opamp_gain = opamp_configuration(opamp_config)
    resistors_voltage_noise = resistor_thermal_noise(parallel_res(res_feedback, 
                                                                  res_g))
    input_current_noise = opamp_current_noise(parallel_res(res_feedback, 
                                                           res_g), 
                                                           opamp_input_current_noise)
    opamp_noise_gain = noise_gain(res_feedback, res_g)

    # Which type of noise dominants circuit
    resistor_or_opamp_noise_dominant(parallel_res(res_feedback, res_g))
    current_noise_or_opamp_noise_dominant(opamp_current_noise(parallel_res(res_feedback, res_g), opamp_input_current_noise), opamp_input_voltage_noise)
    broadband_or_white_noise_dominant(opamp_GBW, opamp_noise_gain) # wrong?

    # Total noise
    total_input_noise_rms()
    total_output_noise_rms()

    print(f"\nOpamp gain: {opamp_gain} V/V")
    print(f"Feedback resistors voltage noise: {resistors_voltage_noise} V/sqrt(Hz)")
    print(f"Feedback equivalent current noise as voltage noise: {input_current_noise} V/sqrt(Hz)")
    print(f"Total output noise: {total_output_voltage_noise} Vrms")
    # print(f"\nWith RC filter, limiting bandwidth to: {rc_freq} Hz")
    # print(f"Adjusted total output noise: {total_output_voltage_noise_adjusted} Vrms")