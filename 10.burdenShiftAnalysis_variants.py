#!/usr/bin/python3

import os,sys,argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--cutoff', required=True, type=str, help='Categories with variant >= cutoff', default='5',metavar='')
    args=parser.parse_args()
 
    if args.cutoff:
        try:
            cutoff = int(args.cutoff)
            os.system("mkdir -p ../11.burdenShift_variants_{0}".format(cutoff))
            cmd = "cwas burden_shift -i ../07.binomial_test_variants/all.sorted.burden_test.txt \
                    -b ../07.permutation_test_variants/all.sorted.binom_pvals.txt.gz \
                    -o_dir ../11.burdenShift_variants_{0} -c_cutoff {0} -c_info ../07.binomial_test_variants/all.sorted.category_info.txt \
                    -c_count ../07.binomial_test_variants/all.sorted.category_counts.txt --pval 0.05".format(cutoff)
            print("### Variant-level burden shift analysis, specified cutoff >= {0}".format(cutoff))
            os.system(cmd)
            print("### Done")


        except:
            print("### Error: please provide integer number of cutoff value")


if __name__ == "__main__":
    main()
