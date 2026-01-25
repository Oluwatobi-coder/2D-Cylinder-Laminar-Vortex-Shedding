# Python script to calculate vortex shedding frequency and Strouhal number from OpenFOAM simulation data 
# and validate against Roshko's empirical correlation.
# Author: Bello Oluwatobi
# Last Updated: January 6, 2026

# importing the required libraries
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# specifying the path to coefficient.dat file
filename = "postProcessing/forceCoeffs1/0/coefficient.dat"


# loading the data from the file and ignoring comment lines
data = np.genfromtxt(filename, comments='#')


# specifying the cylinder parameters
diameter = 1.0   # Cylinder diameter (m)
velocity = 1.0   # Inlet velocity (m/s)

# extracting time and lift coefficient (Cl) from the data
time = data[:, 0]
cl = data[:, 4]

# plotting the lift coefficient over time for the entire duration
plt.figure(figsize=(10, 6))
plt.plot(time, cl, label='Lift Coefficient (Cl)', color='b')
plt.title('Development of Von Kármán Vortex Shedding (0 - 100s)')
plt.xlabel('Time (s)')
plt.ylabel('Coefficient of Lift (Cl)')
plt.savefig('../results/vortex_all_timesteps.png', dpi=300)


# specifying the time when the flow becomes fully developed
start_time = 30 
# removing unstable data before start_time
mask = time > start_time
time_stable = time[mask]
cl_stable = cl[mask]


# plotting the stable portion of the data
plt.figure(figsize=(10, 6))
plt.plot(time_stable, cl_stable, label='Lift Coefficient (Cl)', color='b')
plt.title(r'Fully Developed Von Kármán Vortex Shedding ($t \geq \, 30s$)')
plt.xlabel('Time (s)')
plt.ylabel('Coefficient of Lift (Cl)')
plt.savefig('../results/vortex_fully_developed.png', dpi=300)
# plt.grid(True)


# finding the peaks in the lift coefficient data in the fully developed region
peaks, _ = find_peaks(cl_stable, height=0, distance=792)


# calculating the average period and frequency of vortex shedding
peak_times = time_stable[peaks]
avg_period = np.mean(np.diff(peak_times))
frequency = 1 / avg_period


# calculating the Strouhal number: St = (f * D) / U
strouhal = (frequency * diameter) / velocity

# printing the results
print(f"# vortex shedding results")
print(f"Average Period: {avg_period:.4f} s")
print(f"Shedding Frequency: {frequency:.4f} Hz")
print(f"Strouhal Number (St): {strouhal:.4f}")


# plotting the lift coefficient with detected peaks in the stable region
plt.figure(figsize=(10, 6))
plt.plot(time_stable[peaks], cl_stable[peaks], "x", color='r', label='Peaks')
plt.legend()
plt.title('Lift Coefficient ($C_l$) Peaks vs. Time (Re=100)')
plt.xlabel('Simulation Time ($s$)')
plt.ylabel('Lift Coefficient ($C_l$)')
plt.savefig('../results/lift_coefficient_peaks_re100.png', dpi=300)


# defining the Reynolds number range according to the Roshko correlation and calculating Strouhal numbers
re_range = np.linspace(50, 150, 100)
st_roshko = 0.212 - (4.5 / re_range)

# calculating Roshko's Strouhal number at Re=100 for validation
roshko_at_100 = 0.212 - (4.5/100)
re_100 = 100

print(f"Roshko's Strouhal number at Re=100: {roshko_at_100:.4f}")

# creating the validation plot
plt.figure(figsize=(8, 5))
plt.plot(re_range, st_roshko, 'k--', label='Roshko (1954) Correlation') # Dashed black line
plt.plot(re_100, strouhal, 'o', color='red', markersize=8, label=f'Strouhal Number (simulation) ={strouhal:.4f}')
plt.plot(re_100, roshko_at_100, color='blue', marker='o', markersize=8, label=f'Strouhal Number (Roshko correlation at Re=100) = 0.1670')

# adding the error line
plt.vlines(re_100, strouhal, roshko_at_100, colors='r', linestyles='dotted', label=f'Error: {abs(strouhal - roshko_at_100)/roshko_at_100:.2%}')


# styling the plot
plt.xlabel('Reynolds Number (Re)')
plt.ylabel('Strouhal Number (St)')
plt.title('Validation of Case Simulation: Strouhal Number vs Reynolds Number')
plt.legend()
plt.grid(True)
plt.savefig('../results/validation_plot.png', dpi=300)
