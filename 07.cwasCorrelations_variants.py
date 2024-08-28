#!/usr/bin/python3

import os,sys,argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--process', required=False, type=str, help='Processors: default=20', default='20',metavar='')
    args=parser.parse_args()
    
    os.system("mkdir -p ../08.correlation_variants")
    print("### Generate correlation matrix in variant-level with {0} processors".format(args.process))
    os.system("cwas correlation -i ../06.category/all.sorted.categorization_result.zarr -v ../05.annot_vcf/all.sorted.annotated.vcf.gz -o_dir ../08.correlation_variants -p {0} -cm variant -im".format(args.process))



if __name__ == "__main__":
    main()
