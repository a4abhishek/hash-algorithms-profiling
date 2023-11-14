#!/usr/bin/env python3.9

import hashlib
import json
import time
import psutil
import zlib
from memory_profiler import memory_usage
import cProfile

profile_results_json = 'profiling_results.json'


# Hash Functions
def hash_md5(data):
    return hashlib.md5(data).hexdigest()


def hash_sha1(data):
    return hashlib.sha1(data).hexdigest()


def hash_sha256(data):
    return hashlib.sha256(data).hexdigest()


def hash_crc32(data):
    return '%08X' % (zlib.crc32(data) & 0xFFFFFFFF)


# Profiling Function
def profile_hash_function(hash_function, data):
    start_time = time.time()
    start_cpu = psutil.cpu_percent(interval=None)
    mem_usage = memory_usage((hash_function, (data,)))
    end_cpu = psutil.cpu_percent(interval=None)
    end_time = time.time()

    return {
        'time': end_time - start_time,
        'memory': max(mem_usage),
        'cpu': (end_cpu - start_cpu)
    }


# Main Execution
def main():
    eight_bit_string = b"8bitsstr"
    file_sizes = {'1 KB': 1024,
                  '1 MB': 1024 * 1024,
                  '50 MB': 50 * 1024 * 1024}
    # '500 MB': 500 * 1024 * 1024} # Refrain from having very large size as it will be stored in memory
    hash_functions = [hash_md5, hash_sha1, hash_sha256, hash_crc32]
    results = {}

    for file_size_str, file_size in file_sizes.items():
        data = eight_bit_string * file_size  # Sample data to hash
        for func in hash_functions:
            aggregated_results = {'time': 0, 'memory': 0, 'cpu': 0}
            iterations = 10
            for _ in range(iterations):
                result = profile_hash_function(func, data)
                aggregated_results['time'] += result['time']
                aggregated_results['memory'] += result['memory']
                aggregated_results['cpu'] += result['cpu']

            # Averaging results
            aggregated_results['time'] /= iterations
            aggregated_results['memory'] /= iterations
            aggregated_results['cpu'] /= iterations

            if file_size not in results:
                results[file_size] = {}
            results[file_size][func.__name__] = aggregated_results

            print(
                f"{func.__name__} - {file_size_str}: Time - {aggregated_results['time']:.4f}s, Memory - {aggregated_results['memory']:.2f}MB, CPU - {aggregated_results['cpu']}%")

            # Save results so far
            with open(profile_results_json, 'w') as f:
                json.dump(results, f)


if __name__ == '__main__':
    cProfile.run('main()', 'profiling_results')
