#!/home/dcha/anaconda3/envs/cwas/bin/python3

import os,sys,argparse

def main():
    print("### Performing burden test (binomial test)")
    os.system("mkdir -p ../07.binomial_test_samples")
    cmd_binom = "cwas binomial_test -i ../06.category/all.sorted.categorization_result.zarr -o_dir ../07.binomial_test_samples -s ../SAMPLE_LIST.txt -a ../ADJUST_FACTOR.txt -u"
    os.system(cmd_binom)


if __name__ == "__main__":
    main()
