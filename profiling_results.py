import pstats

if __name__ == '__main__':
    p = pstats.Stats('profiling_results')
    p.sort_stats('cumulative').print_stats(10)
