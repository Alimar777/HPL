import matplotlib.pyplot as plt

# Data: NB and flops extracted from your given data
data = [
    (1, 8.3130e+00), (2, 1.6619e+01), (4, 3.2992e+01), (8, 6.5301e+01), 
    (16, 1.2322e+02), (32, 2.1975e+02), (64, 2.5499e+02), (128, 2.5049e+02),
    (256, 2.1998e+02), (512, 1.8851e+02), (1024, 1.4235e+02), (2048, 9.0431e+01),
    (32, 2.2201e+02), (48, 2.5385e+02), (64, 2.5631e+02), (80, 2.5828e+02),
    (96, 2.5531e+02), (112, 2.5445e+02), (128, 2.5167e+02), (144, 2.4969e+02),
    (160, 2.4213e+02), (176, 2.3807e+02), (192, 2.3324e+02), (208, 2.2586e+02),
    (224, 2.2830e+02), (240, 2.2358e+02), (256, 2.1475e+02), (272, 2.2732e+02),
    (288, 2.2427e+02), (304, 2.2021e+02), (320, 2.1810e+02), (336, 2.1495e+02),
    (352, 2.1024e+02), (368, 2.0891e+02), (384, 2.0592e+02), (400, 2.0374e+02),
    (416, 2.0005e+02), (432, 1.9550e+02), (448, 1.9530e+02), (464, 1.9579e+02),
    (480, 1.8931e+02), (496, 1.8956e+02), (512, 1.8545e+02)
]

# Sort data by NB value
data.sort(key=lambda x: x[0])

# Split data into x (NB values) and y (flops)
nb_values, flops = zip(*data)

# Find the index of the maximum flops value
max_index = flops.index(max(flops))

# Determine the window range (±2)
highlight_indices = range(max(0, max_index - 2), min(len(flops), max_index + 3))

# Plotting
plt.figure(figsize=(12, 6))
plt.plot(nb_values, flops, marker='o', linestyle='-', color='b', label='Flops')

# Highlight the range of the highest point
plt.plot(
    [nb_values[i] for i in highlight_indices],
    [flops[i] for i in highlight_indices],
    marker='o', linestyle='-', color='r', label='Highlighted Range'
)

# Find the index of the maximum flops value
max_index = flops.index(max(flops))

# Determine the window range (±2)
highlight_indices = range(max(0, max_index - 2), min(len(flops), max_index + 3))

# Extract NB values in the highlighted range
highlighted_nb_values = [nb_values[i] for i in highlight_indices]

# Print the NB values along the highlighted range
print("NB values in the highlighted range:", highlighted_nb_values)


plt.title('Flops vs. NB Values with Highlighted Peak')
plt.xlabel('NB Values')
plt.ylabel('Flops')
plt.grid(True)
plt.legend()
plt.show()
