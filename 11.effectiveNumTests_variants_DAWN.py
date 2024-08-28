#!/usr/bin/python3

import os,sys,argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--cutoff', required=True, type=str, help='Categories with variant >= cutoff (default: 5)', default='5',metavar='')
    parser.add_argument('-s', '--set', required=True, type=str, help='Category set: all (default), coding, noncoding', default='all',metavar='')
    args=parser.parse_args()
 
    if args.cutoff:
        try:
            cutoff = int(args.cutoff)
            if args.set in ["all", "coding", "noncoding"]:
                try:
                    catSet = args.set
                    os.system("mkdir -p ../12.DAWN.effTestNumVariantsSpecified_{0}_categorySet_{1}".format(cutoff,catSet))
                    cmd = "cwas effective_num_test -i ../08.correlation_variants/all.sorted.correlation_matrix.all.zarr \
                        -o_dir ../12.DAWN.effTestNumVariantsSpecified_{0}_categorySet_{1} -if corr -n 10000 -thr {0} \
                        -c_count ../07.binomial_test_variants/all.sorted.category_counts.txt".format(cutoff,catSet)
                    if catSet in ["coding", "noncoding"]:
                        cmd += " -c_set ../07.binomial_test_variants/{0}_category_set.txt".format(catSet)
                    print("### Variant-level Effective number of tests is being calculated with 10,000 simulations, specified cutoff >= {0}, category set: {1}".format(cutoff, catSet))
                    os.system(cmd)
                    print("### Done")
                except:
                    print("###: please provide right category set: all, coding, noncoding")



        except:
            print("### Error: please provide integer number of cutoff value")


if __name__ == "__main__":
    main()
