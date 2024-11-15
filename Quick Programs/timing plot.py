import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# Amdahl's law function definition
def Amdahl_objective(N, a):
    return 1 / (a + (1 - a) / N)

# Data
threads = np.array([1, 2, 4, 8, 16, 32, 64])
time_1_node = np.array([1089.55, 652.40, 455.14, 296.40, 158.66, 78.02, np.nan])
time_2_nodes = np.array([1089.55, 436.76, 355.51, 244.15, 157.80, 49.07, 40.44])

# Removing NaNs for fitting purposes
valid_indices_1_node = ~np.isnan(time_1_node)
valid_indices_2_nodes = ~np.isnan(time_2_nodes)

# Fitting Amdahl's law to the data
popt_1_node, _ = curve_fit(Amdahl_objective, threads[valid_indices_1_node], time_1_node[valid_indices_1_node] / time_1_node[0])
popt_2_nodes, _ = curve_fit(Amdahl_objective, threads[valid_indices_2_nodes], time_2_nodes[valid_indices_2_nodes] / time_2_nodes[0])

# Generate fitted data
speedup_1_node = Amdahl_objective(threads, *popt_1_node) * time_1_node[0]
speedup_2_nodes = Amdahl_objective(threads, *popt_2_nodes) * time_2_nodes[0]

# Plotting
plt.figure(figsize=(10, 7))
plt.plot(threads, time_1_node, 'o-', label='Measured Time (1 Node)')
plt.plot(threads, time_2_nodes, 's-', label='Measured Time (2 Nodes)')
plt.plot(threads, speedup_1_node, 'r--', label=f'Fitted Amdahl (1 Node, a={popt_1_node[0]:.5f})')
plt.plot(threads, speedup_2_nodes, 'b--', label=f'Fitted Amdahl (2 Nodes, a={popt_2_nodes[0]:.5f})')

# Customizing the plot
plt.title('Strong Scaling Analysis with Amdahl\'s Law Fit')
plt.xlabel('Threads')
plt.ylabel('Time (seconds)')
plt.xscale('log', base=2)  # Using a log scale for better visualization
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.legend()

# Display the plot
plt.show()
