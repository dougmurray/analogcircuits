import numpy as np

def inverting_opamp_gain(feedback_res, g_res):
    "Simple helper function."
    inv_gain = feedback_res / g_res
    return inv_gain

def parallel_res(res_one, res_two):
    "Equivalent resistance of resistors parallel."
    parallel_res = (res_one * res_two) / (res_one + res_two)
    return parallel_res

def resistor_thermal_noise(res):
    "Johnson-Nyquist noise, aka thermal noise"
    k = 1.38e-23 # J/K, Boltzmann constant
    temp = 289 # K, room temperature
    thermal_noise = np.sqrt(4 * k * temp * res)
    return thermal_noise

def noise_gain(feedback_res, res_g):
    gain_of_noise = 1 + feedback_res / res_g # ALWAYS! Regardless of opamp config
    return gain_of_noise

def opamp_broadband_noise(opamp_GBW, noise_gain, filter_order=1.57):
    "BW_n of opamp.  If there is a feedback cap, or RC filter, then DO NOT USE THIS"
    broadband_noise_freq = filter_order * (opamp_GBW / noise_gain) # Hz
    return broadband_noise_freq

def total_input_noise_rms(opamp_input_voltage_noise, opamp_input_current_noise, 
                          feedback_res, g_res, opamp_GBW, filter_res=None, filter_cap=None):
    "Total input voltage noise in Vrms."
    current_noise = parallel_res(feedback_res, g_res) * opamp_input_current_noise
    resistors_voltage_noise = resistor_thermal_noise(parallel_res(feedback_res, g_res))
    opamp_noise_gain = noise_gain(feedback_res, g_res)
    broadband_noise = opamp_broadband_noise(opamp_GBW, opamp_noise_gain) # Hz
    if not (filter_res or filter_cap):
        total_input_voltage_noise = np.sqrt(opamp_input_voltage_noise**2 
                                            + current_noise**2 
                                            + resistors_voltage_noise**2) * np.sqrt(broadband_noise) # Vrms
        print(f"At bandwidth of: {broadband_noise} Hz")
    else:
        rc_freq = 1 / (2 * np.pi * filter_res * filter_cap) # Hz
        if rc_freq > broadband_noise:
            total_input_voltage_noise = np.sqrt(opamp_input_voltage_noise**2 
                                            + current_noise**2 
                                            + resistors_voltage_noise**2) * np.sqrt(broadband_noise) # Vrms
            print(f"At bandwidth of: {broadband_noise} Hz") 
        else:
            total_input_voltage_noise = np.sqrt(opamp_input_voltage_noise**2 
                                                         + current_noise**2 
                                                         + resistors_voltage_noise**2) * np.sqrt(1.57 * rc_freq) # Vrms
            print(f"At bandwidth of: {rc_freq} Hz") 
    return total_input_voltage_noise

def total_output_noise_rms(input_voltage_noise, opamp_gain):
    "Total output voltage noise in Vrms."
    total_output_voltage_noise = input_voltage_noise * opamp_gain # Vrms
    return total_output_voltage_noise

# First stage ADA4807
first_ada4807_input_voltage_noise = 3.1e-9 # V/sqrt(Hz)
first_ada4807_input_current_noise = 0.7e-12 # A/sqrt(Hz)
first_ada4807_GBW = 180e6 # Hz
first_ada4807_noise_corner_freq = 29 # Hz
first_ada4807_feedback_res = 3e3 # Ohms
first_ada4807_g_res = 1e3 # Ohms
first_ada4807_filter_res = 5e3 # F
first_ada4807_filter_cap = 4.7e-9 # F
first_ada4807_gain = inverting_opamp_gain(first_ada4807_feedback_res, first_ada4807_g_res)

first_ada4807_total_input_noise = total_input_noise_rms(first_ada4807_input_voltage_noise, 
                                                        first_ada4807_input_current_noise, 
                                                        first_ada4807_feedback_res, 
                                                        first_ada4807_g_res, first_ada4807_GBW, 
                                                        filter_res=first_ada4807_filter_res, 
                                                        filter_cap=first_ada4807_filter_cap)
first_ada4807_total_output_noise = total_output_noise_rms(first_ada4807_total_input_noise, first_ada4807_gain)
# print(f"First ADA4807 total input noise: {first_ada4807_total_input_noise} Vrms")
print(f"First ADA4807 total output noise: {first_ada4807_total_output_noise} Vrms")

# Second stage ADA4807
second_ada4807_input_voltage_noise = 3.1e-9 # V/sqrt(Hz)
second_ada4807_input_current_noise = 0.7e-12 # A/sqrt(Hz)
second_ada4807_GBW = 180e6 # Hz
second_ada4807_noise_corner_freq = 29 # Hz
second_ada4807_feedback_res = 5e3 # Ohms
second_ada4807_g_res = 10e3 # Ohms
second_ada4807_filter_res = 5e3 # Ohms, variable
second_ada4807_filter_cap = 1e-9 # F
second_ada4807_gain = inverting_opamp_gain(second_ada4807_feedback_res, second_ada4807_g_res)

second_ada4807_total_input_noise = total_input_noise_rms(second_ada4807_input_voltage_noise, 
                                                         second_ada4807_input_current_noise, 
                                                         second_ada4807_feedback_res, 
                                                         second_ada4807_g_res, 
                                                         second_ada4807_GBW, 
                                                         filter_res=second_ada4807_filter_res, 
                                                         filter_cap=second_ada4807_filter_cap)
second_ada4807_total_output_noise = total_output_noise_rms(second_ada4807_total_input_noise, second_ada4807_gain)
# print(f"Second ADA4807 total input noise: {second_ada4807_total_input_noise} Vrms")
print(f"Second ADA4807 total output noise: {second_ada4807_total_output_noise} Vrms")

# Third stage ADA4807
third_ada4807_input_voltage_noise = 3.1e-9 # V/sqrt(Hz)
third_ada4807_input_current_noise = 0.7e-12 # A/sqrt(Hz)
third_ada4807_GBW = 180e6 # Hz
third_ada4807_noise_corner_freq = 29 # Hz
third_ada4807_feedback_res = 1 # Ohms
third_ada4807_g_res = 1 # Ohms
third_ada4807_filter_res = 5e3 # Ohms, variable
third_ada4807_filter_cap = 1e-9 # F
third_ada4807_gain = inverting_opamp_gain(third_ada4807_feedback_res, third_ada4807_g_res)

third_ada4807_total_input_noise = total_input_noise_rms(third_ada4807_input_voltage_noise, 
                                                        third_ada4807_input_current_noise, 
                                                        third_ada4807_feedback_res, 
                                                        third_ada4807_g_res, 
                                                        third_ada4807_GBW, 
                                                        filter_res=third_ada4807_filter_res, 
                                                        filter_cap=third_ada4807_filter_cap)
third_ada4807_total_output_noise = total_output_noise_rms(third_ada4807_total_input_noise, third_ada4807_gain)
# print(f"Third ADA4807 total input noise: {third_ada4807_total_input_noise} Vrms")
print(f"Third ADA4807 total output noise: {third_ada4807_total_output_noise} Vrms")

# Forth stage ADA4807
forth_ada4807_input_voltage_noise = 3.1e-9 # V/sqrt(Hz)
forth_ada4807_input_current_noise = 0.7e-12 # A/sqrt(Hz)
forth_ada4807_GBW = 180e6 # Hz
forth_ada4807_noise_corner_freq = 29 # Hz
forth_ada4807_feedback_res = 1 # Ohms
forth_ada4807_g_res = 1 # Ohms
forth_ada4807_gain = inverting_opamp_gain(forth_ada4807_feedback_res, forth_ada4807_g_res)

forth_ada4807_total_input_noise = total_input_noise_rms(forth_ada4807_input_voltage_noise, 
                                                        forth_ada4807_input_current_noise, 
                                                        forth_ada4807_feedback_res, 
                                                        forth_ada4807_g_res, 
                                                        forth_ada4807_GBW, 
                                                        filter_res=None, 
                                                        filter_cap=None)
forth_ada4807_total_output_noise = total_output_noise_rms(forth_ada4807_total_input_noise, forth_ada4807_gain)
# print(f"Forth ADA4807 total input noise: {forth_ada4807_total_input_noise} Vrms")
print(f"Forth ADA4807 total output noise: {forth_ada4807_total_output_noise} Vrms")

# Fifth stage AD8057
fifth_ad8057_input_voltage_noise = 7.0e-9 # V/sqrt(Hz)
fifth_ad8057_input_current_noise = 0.7e-12 # A/sqrt(Hz)
fifth_ad8057_GBW = 325e6 # Hz
fifth_ad8057_noise_corner_freq = 2e3 # Hz
fifth_ad8057_feedback_res = 10e3 # Ohms
fifth_ad8057_g_res = 100 # Ohms
fifth_ad8057_filter_res = 100 # Ohms, variable
fifth_ad8057_filter_cap = 10e-12 # F
fifth_ad8057_gain = inverting_opamp_gain(fifth_ad8057_feedback_res, fifth_ad8057_g_res)

fifth_ad8057_total_input_noise = total_input_noise_rms(fifth_ad8057_input_voltage_noise, 
                                                       fifth_ad8057_input_current_noise, 
                                                       fifth_ad8057_feedback_res, 
                                                       fifth_ad8057_g_res, 
                                                       fifth_ad8057_GBW, 
                                                       filter_res=fifth_ad8057_filter_res, 
                                                       filter_cap=fifth_ad8057_filter_cap)
fifth_ad8057_total_output_noise = total_output_noise_rms(fifth_ad8057_total_input_noise, fifth_ad8057_gain)
# print(f"Fifth AD8057 total input noise: {forth_ada4807_total_input_noise} Vrms")
print(f"Fifth AD8057 total output noise: {fifth_ad8057_total_output_noise} Vrms")

total_system_noise = (first_ada4807_total_output_noise + second_ada4807_total_output_noise 
                      + third_ada4807_total_output_noise + forth_ada4807_total_output_noise 
                      + fifth_ad8057_total_output_noise)
print(f"Total system noise: {total_system_noise} Vrms")