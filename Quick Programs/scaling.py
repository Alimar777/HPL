import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# Amdahl's law function definition
def Amdahl_objective(x, a):
    return 1 / (a + (1 - a) / x)

# Data
threads = np.array([1, 2, 4, 8, 16, 32, 64])
time_1_node = np.array([1089.55, 652.40, 455.14, 296.40, 158.66, 78.02, np.nan])
time_2_nodes = np.array([1089.55, 436.76, 355.51, 244.15, 157.80, 49.07, 40.44])

# Remove NaN values from the data
valid_indices = ~np.isnan(time_1_node)  # Find indices that are not NaN
threads_valid = threads[valid_indices]  # Filter threads
time_1_node_valid = time_1_node[valid_indices]  # Filter time_1_node
time_2_nodes_valid = time_2_nodes[valid_indices]  # Filter time_2_nodes

# Plotting the measured times
plt.figure(figsize=(3.5, 3))  # Adjust figure size
plt.plot(threads, time_1_node, 'o-', label='Measured Time (1 Node)')
plt.plot(threads, time_2_nodes, 's-', label='Measured Time (2 Nodes)')

# Customizing the plot
plt.title('Strong Scaling', fontsize=10)  # Smaller title font size
plt.xlabel('Threads', fontsize=9)  # Smaller axis label font size
plt.ylabel('Time (s)', fontsize=9)  # Smaller axis label font size
plt.xscale('log', base=2)  # Using a log scale for better visualization
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.legend(fontsize=8)  # Smaller legend font size

# Adjust layout and display the plot
plt.tight_layout()  # Tight layout to ensure the plot fits well in the document
plt.show()

# Calculate speedup
y1 = time_1_node[0]
yy = y1 / time_1_node_valid
y = y1 / time_2_nodes_valid  # Calculate speedup (y1 divided by each value in time_2_nodes)

# Scatter plot for input vs. output (Speedup)
plt.scatter(threads_valid, y, label='Speedup (2 Nodes)', color='blue')
plt.scatter(threads_valid, yy, label='Speedup (1 Node)', color='orange')

# Fit the data to Amdahl's law
popt, _ = curve_fit(Amdahl_objective, threads_valid, y)
popt_2, _ = curve_fit(Amdahl_objective, threads_valid, yy)

a = popt[0]  # Extract the fitted parameter 'a' for 2 nodes
b = popt_2[0]  # Extract the fitted parameter 'b' for 1 node

# Print the fitted Amdahl's Law equation with labels
print(f'For 2 Nodes: y = 1 / ( {a:.5f} + (1 - {a:.5f}) / N )')
print(f'For 1 Node: y = 1 / ( {b:.5f} + (1 - {b:.5f}) / N )')

# Define a sequence of inputs between the smallest and largest known inputs
x_line = np.arange(min(threads_valid), max(threads_valid), 1)

# Calculate the output for the range using the fitted Amdahl's Law model
y_line = Amdahl_objective(x_line, a)
y_line_2 = Amdahl_objective(x_line, b)

# Plot the fitted Amdahl's Law line
plt.plot(x_line, y_line, '--', color='red', label='A_Fit (2 Nodes)')
plt.plot(x_line, y_line_2, '--', color='green', label='A_Fit (1 Node)')

# Customize the plot
plt.xticks(threads_valid, size=16)
plt.title('Speedup Analysis', size=16)
plt.yticks(size=16)
plt.xlabel("Threads", size=16)
plt.ylabel("Speedup", size=16)
plt.legend(fontsize=12)

# Show the plot
plt.show()
