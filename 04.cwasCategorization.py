#!/home/dcha/anaconda3/envs/cwas/bin/python3

import os,sys,argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--process', required=False, type=str, help='Processors: default=20', default='20',metavar='')
    args=parser.parse_args()

    os.system("mkdir -p ../06.category")
    print("### Categorizing variants with {0} processors".format(args.process))
    os.system("cwas categorization -i ../05.annot_vcf/all.sorted.annotated.vcf.gz -o_dir ../06.category -p "+args.process)
    
if __name__ == "__main__":
    main()
