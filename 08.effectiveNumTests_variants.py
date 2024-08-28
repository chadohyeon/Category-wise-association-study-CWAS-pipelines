#!/usr/bin/python3

import os,sys,argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--cutoff', required=True, type=str, help='Categories with variant >= cutoff', default='5',metavar='')
    args=parser.parse_args()
 
    if args.cutoff:
        try:
            cutoff = int(args.cutoff)

            os.system("mkdir -p ../09.effTestNumVariantsSpecified_{0}".format(cutoff))
            cmd = "cwas effective_num_test -i ../08.correlation_variants/all.sorted.correlation_matrix.all.zarr \
                    -o_dir ../09.effTestNumVariantsSpecified_{0} -if corr -n 10000 -thr {0} -ef \
                    -c_count ../07.binomial_test_variants/all.sorted.category_counts.txt".format(cutoff)
            print("### Variant-level Effective number of tests is being calculated with 10,000 simulations, specified cutoff >= {0}".format(cutoff))
            os.system(cmd)
            print("### Done")



        except:
            print("### Error: please provide integer number of cutoff value")


if __name__ == "__main__":
    main()
