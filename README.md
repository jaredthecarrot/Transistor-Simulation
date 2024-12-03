# Transistor Simulation

This repository provides a simulation tool for transistors using machine learning and material properties. It integrates data from the Materials Project API to evaluate various materials for use in transistor design.

## Requirements

### 1. Install LTSpice
- Download LTSpice from the [Analog Devices website](https://www.analog.com/en/design-center/design-tools-and-calculators/ltspice-simulator.html).
- Follow the installation instructions for your operating system (Windows or macOS).

### 2. Install Python and Dependencies
To run the simulation, Python 3.6+ is required. Install Python from the [official website](https://www.python.org/downloads/).

#### Install Required Libraries
After installing Python, install the required Python packages by running:
```bash
pip install numpy pandas scikit-learn mp-api

git clone https://github.com/jaredthecarrot/Transistor-Simulation.git
cd Transistor-Simulation

python simulation.py
```
### 3. Usage

LTSPICE_EXE_PATH in the simulation.py must be changed to the path to your LTSpice executable.
When running the simulation script, the terminal will display the material suitability
and there will be popups of LTSpice simulations showing you performnace of each transistor.
To graph the circuit, you will need to right clock and select Add Traces, and then select the
components you want to visualize.
