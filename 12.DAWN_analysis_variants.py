#!/usr/bin/python3

import os,sys,argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--cutoff', required=True, type=str, help='Categories with variant >= cutoff', default='20',metavar='')
    parser.add_argument('-p', '--process', required=True, type=str, help='Number of processors', default='20', metavar='')
    parser.add_argument('-e', '--effTestCutoff', required=False, type=str, help='Cutoff of effective number of variants test', default='5', metavar='')
    parser.add_argument('-s', '--set', required=True, type=str, help='Category set: all (default), coding, noncoding', default='all', metavar='')

    args=parser.parse_args()

    if args.cutoff:
        try:
            cutoff = int(args.cutoff)
            if args.set in ["all", "coding", "noncoding"]:
                try:
                    catSet = args.set
                    effTestDir = "12.DAWN.effTestNumVariantsSpecified_{0}_categorySet_{1}".format(args.effTestCutoff, catSet)
                    if effTestDir in [k for k in os.listdir("..")]:
                        eigVecDir = "/home/dcha/cwas/{0}/all.sorted.eig_vecs.all.zarr".format(effTestDir)
                        print("### Eigen value directory: {0}".format(eigVecDir))
                    else:
                        print("### Please provide right cutoff used in effective number of variants test")
                    os.system("mkdir -p ../13.DAWN_analysis_variants_{0}_categorySet_{1}".format(cutoff, catSet))
                    print(eigVecDir)
                    cmd = "cwas dawn -e {0} -c ../08.correlation_variants/all.sorted.correlation_matrix.all.zarr \
                            -P ../07.permutation_test_variants/all.sorted.permutation_test.txt.gz \
                            -o_dir ../13.DAWN_analysis_variants_{1}_categorySet_{2} \
                            -r 2,100 -s 123 -C {1} -R 0.12 -S 2 -p {3} -T exact -t {2} \
                            -c_count ../07.binomial_test_variants/all.sorted.category_counts.txt".format(eigVecDir, cutoff, catSet, args.process)
                    print(cmd)
                    print("### Variant-level DAWN analysis, {0} category / specified cutoff >= {1} / correlation R >= 0.12 / size threshold >= 2".format(catSet, cutoff))
                    os.system(cmd)
                    print("### Done")
                except:
                    print("### Error: please provide right category set")

        except:
            print("### Error: please provide integer number of cutoff value")


if __name__ == "__main__":
    main()
