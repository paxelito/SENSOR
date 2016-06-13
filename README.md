# SENSOR (Socioeconomic ENergy System simulatOR)

Plaftorms: MacOS, Linux, Windows
Language: Python
Comments: The presence of [C] string within comments indicates a WaRNING. Model here must be controlled. 

# RELEASE NOTES

## 2014 - 10 - 24 ver.1.3
- Configuration file has been extended with new params
- Policy end time has been added to the policy class
- main_GA.py (main devoted to the introduction of a genetic algorithm) has been created
- !!! Add and remove agents each month (%) (each month an agent randomly selected is removed and a new casual agent is added)
- a = [np.random.randn() for i in range(1000)] - np.random.normal(mu, sigma, 1000)
- beta distribution http://en.wikipedia.org/wiki/Beta_distribution
- http://docs.scipy.org/doc/numpy/reference/generated/numpy.random.beta.html=numpy.random.beta
- !!! To fix che continue creation of the technologies and of the policie at each run
- !!! CONTROL THE FITTING FUNCTION

## 2014 - 05 - 08 ver.1.2
- bioenergy year yield has been added
- Attractiveness is now based on both the energetic and the physical dimension of the agents.
- Source code has been arranged in folder (a code library has been created)
- Agents technology awareness is now based on the aptitude risk of the agent.
- Several Bugs Fixed


## 2014 - 04 - 16 ver.1.1
- The technology awareness behavior has been added
- The acceptance of the financial investment has been implemented
- Several bugs fixed
## 2014 - 02 - 19 ver.1.0
- The introduction time is now considered for each technology

# Documentation
sphinx-apidoc -o ./doc/sphynx ./ -A 'Alessandro Filisetti' -V 1.3 -R 20141010 -f -H 'SENSOR: Socio-Economic Energy Simulator' -F 

