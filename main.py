#!/usr/bin/env python3.9

import hashlib
import json
import time
import os
import psutil
import zlib
from memory_profiler import memory_usage
import cProfile

hash_input_directory = 'hash_input'
profile_results_json = 'profiling_results.json'
buffer_size = 50 * 1024 * 1024  # 50 MB buffer size


# Hash Functions for buffered reading from file
def hash_file_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(buffer_size), b''):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def hash_file_sha1(file_path):
    hash_sha1 = hashlib.sha1()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(buffer_size), b''):
            hash_sha1.update(chunk)
    return hash_sha1.hexdigest()


def hash_file_sha256(file_path):
    hash_sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(buffer_size), b''):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()


def hash_file_crc32(file_path):
    crc32 = 0
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(buffer_size), b''):
            crc32 = zlib.crc32(chunk, crc32)
    return '%08X' % (crc32 & 0xFFFFFFFF)


# Profiling Function
def profile_hash_function(hash_function, file_path):
    start_time = time.time()
    start_cpu = psutil.cpu_percent(interval=None)
    mem_usage = memory_usage((hash_function, (file_path,)))
    end_cpu = psutil.cpu_percent(interval=None)
    end_time = time.time()

    return {
        'time': end_time - start_time,
        'memory': max(mem_usage),
        'cpu': (end_cpu - start_cpu)
    }


# Main Execution
def main():
    hash_functions = [hash_file_md5, hash_file_sha1, hash_file_sha256, hash_file_crc32]
    results = {}

    for file_name in os.listdir(hash_input_directory):
        file_path = os.path.join(hash_input_directory, file_name)
        file_size = os.path.getsize(file_path)
        file_size_str = f'{file_size} bytes'
        for func in hash_functions:
            aggregated_results = {'time': 0, 'memory': 0, 'cpu': 0}
            iterations = 10
            for _ in range(iterations):
                result = profile_hash_function(func, file_path)
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
