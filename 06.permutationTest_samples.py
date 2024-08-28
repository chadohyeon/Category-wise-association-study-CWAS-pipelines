#!/home/dcha/anaconda3/envs/cwas/bin/python3

import os,sys,argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--numPermutation', required=False, type=str, help='Number of permutation: default=10000', default='10000', metavar='')
    parser.add_argument('-p', '--process', required=False, type=str, help='Processors: default=20', default='20', metavar='')
    args=parser.parse_args()
    
    os.system("mkdir -p ../07.permutation_test_samples")
    print("### Performing burden test (permutation test) with Permutations:{0}  Processors:{1}".format(args.numPermutation, args.process))
    cmd_perm = "cwas permutation_test -i ../06.category/all.sorted.categorization_result.zarr -o_dir ../07.permutation_test_samples -s ../SAMPLE_LIST.txt -a ../ADJUST_FACTOR.txt -n {0} -p {1} -b -u".format(args.numPermutation, args.process)
    os.system(cmd_perm)


if __name__ == "__main__":
    main()
