#!/usr/bin/python3

import os,sys,argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--threshold', required=True, type=str, help='Control categories with variant >= threshold', default='3',metavar='')
    parser.add_argument('-p', '--process', required=False, type=str, help='Processors', default='20',metavar='')
    parser.add_argument('-d', '--domain', required=False, type=str, help='Domain of interest', default='', metavar='')
    parser.add_argument('-f', '--fractionTraining', required=False, type=str, help='Training set percentage, default = 0.7', default='0.7', metavar='')
    args=parser.parse_args()


    if not args.domain:
        domains = ["all", "coding", "noncoding", "ptv", "missense", "damaging_missense", "promoter", "noncoding_wo_promoter", "intron", "intergenic", "utr", "lincRNA"]
    else:
        try:
            domains = [args.domain]
        except:
            print("### Please provide right domain name")
 
    if args.fractionTraining:
        try:
            fraction = float(args.fractionTraining)
        except:
            print("### Please provide right training fraction. e.g., -f 0.7")
            fraction = 0.7

    if args.threshold:
        try:
            fracStr = "".join(str(fraction).split("."))
            threshold = int(args.threshold)
            os.system("mkdir -p ../10.riskScoreAnalysis_{0}".format(threshold))

            for domain in domains:
                os.system("mkdir -p ../10.riskScoreAnalysis_{0}/{1}_riskScore_tf{2}".format(threshold, domain, fracStr))

                cmd = "cwas risk_score -i ../06.category/all.sorted.categorization_result.zarr \
                        -o_dir ../10.riskScoreAnalysis_{0}/{2}_riskScore_tf{4} \
                        -s ../SAMPLE_LIST.txt \
                        -a ../ADJUST_FACTOR.txt \
                        -c_info ../07.binomial_test_variants/all.sorted.category_info.txt \
                        -thr {0} \
                        -tf {1} \
                        -n_reg 10 \
                        -n 1000 \
                        -d {2} \
                        -p {3}".format(threshold, fraction, domain, args.process, fracStr)
                print("### {0}: Variant-level calculation of Risk-score using control-categories number threshold >= {1}, \
                        5-fold CV, training set: {2}, 10 regressions, 1000 permutations, with processors: {3}".format(domain.upper(), threshold, fraction, args.process))
                os.system(cmd)
                print("### Done")


        except:
            print("### Error: please provide integer number of threshold value for element numbers of control-categories")


if __name__ == "__main__":
    main()
