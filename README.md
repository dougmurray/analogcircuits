analogcircuits
==============

AnalogCircuits is for using Python as a quick analog circuits design tool.

It provides:

- analog filters
- opamp circuits noise analysis
- best opamps choice based on source resistance and noise

Although this is a module, each section can be run as an independent script. Ensure when doing so to use the command `python3 -m file.location.script`.


File Structure
--------------

- analogcircuits/
	- elements/
		- discrete.py
	- amplifiers/
		- opamps/
			- opamp_noise.py
		- transistors/
			- transistors.py
	- filters/
		- passive.py
		- active.py