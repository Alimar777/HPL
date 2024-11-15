import numpy as np

# Given problem sizes (N) for different numbers of CPUs
N_values = np.array([11585, 16384, 23170, 32767, 46340, 65535, 92680])

# Calculate the number of gigabytes of memory needed for each N
# Memory formula: ((N / 0.8)^2 * 8) / (1024^3)
memory_gb = ((N_values / 0.8)**2 * 8) / (1024**3)

# Print results
for N, mem in zip(N_values, memory_gb):
    print(f"N = {N}: Memory needed = {mem:.2f} GB")
