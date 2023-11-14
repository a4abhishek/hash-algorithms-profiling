import json
import matplotlib.pyplot as plt

# Load profiling results
with open('profiling_results.json', 'r') as f:
    results = json.load(f)

# Initialize data structures for plotting
file_sizes = []  # X-axis: File sizes
compute_time = { 'hash_md5': [], 'hash_sha1': [], 'hash_sha256': [], 'hash_crc32': [] }  # Y-axis: Compute time per algorithm
cpu_usage = { 'hash_md5': [], 'hash_sha1': [], 'hash_sha256': [], 'hash_crc32': [] }  # Y-axis: CPU usage per algorithm
memory_usage = { 'hash_md5': [], 'hash_sha1': [], 'hash_sha256': [], 'hash_crc32': [] }  # Y-axis: Memory usage per algorithm

# Extract data
for file_size, algorithms in results.items():
    file_sizes.append(file_size)
    for algorithm, metrics in algorithms.items():
        compute_time[algorithm].append(metrics['time'])
        cpu_usage[algorithm].append(metrics['cpu'])
        memory_usage[algorithm].append(metrics['memory'])

# Plot Compute Time
plt.figure(figsize=(10, 6))
for algorithm, usages in compute_time.items():
    plt.plot(file_sizes, usages, label=algorithm)

plt.xlabel('File Size')
plt.ylabel('Compute Time (Seconds)')
plt.title('Compute Time by File Size for Each Hashing Algorithm')
plt.legend()
plt.show()

# Plot CPU Usage
plt.figure(figsize=(10, 6))
for algorithm, usages in cpu_usage.items():
    plt.plot(file_sizes, usages, label=algorithm)

plt.xlabel('File Size')
plt.ylabel('CPU Usage (%)')
plt.title('CPU Usage by File Size for Each Hashing Algorithm')
plt.legend()
plt.show()

# Plot Memory Usage
plt.figure(figsize=(10, 6))
for algorithm, usages in memory_usage.items():
    plt.plot(file_sizes, usages, label=algorithm)

plt.xlabel('File Size')
plt.ylabel('Memory Usage (MB)')
plt.title('Memory Usage by File Size for Each Hashing Algorithm')
plt.legend()
plt.show()
