#!/home/dcha/anaconda3/envs/cwas/bin/python3

import os,sys, argparse

def runCwasAnnotationAndLoftee(process):
    os.system("mkdir -p ../05.annot_vcf")
    os.system("cwas annotation -v ../04.ready_vcf/all.sorted.vcf.gz -o_dir ../05.annot_vcf -p "+process)
    os.system("gunzip ../05.annot_vcf/all.sorted.annotated.vcf.gz")
    os.system("mv ../05.annot_vcf/all.sorted.annotated.vcf \
            ../05.annot_vcf/all.sorted.annotated.noLoftee.vcf")

    path = "/home/dcha/.vep/Plugins"
    inputVcf = "../05.annot_vcf/all.sorted.annotated.noLoftee.vcf"
    outputVcf = "../05.annot_vcf/all.sorted.loftee.only.vcf"

    print("### Applying Loftee-only")
    vepCmd = "vep --assembly GRCh38 --offline --cache --format vcf --vcf " +\
    "--dir_cache /home/dcha/.vep/ --dir_plugins {0} ".format(path)+\
    "-i {0} -o {1} ".format(inputVcf, outputVcf) +\
    "--distance 2000 --force_overwrite --no_stats --nearest gene " +\
    "--per_gene --pick --pick_order rank,canonical,appris,tsl,biotype,ccds,length "+\
    "--plugin LoF,loftee_path:{0}/loftee,".format(path) +\
    "conservation_file:{0}/loftee/resources/loftee.sql,".format(path) +\
    "human_ancestor_fa:{0}/loftee/resources/human_ancestor.fa.gz,".format(path) +\
    "gerp_bigwig:{0}/loftee/resources/gerp_conservation_scores.homo_sapiens.GRCh38.bw".format(path)

    os.system(vepCmd)
    os.system("mkdir -p ../05.annot_vcf/warnings_all")
    os.system("mv ../05.annot_vcf/*_warnings.txt ../05.annot_vcf/warnings_all")

    print("### Merging annotated.noLoftee and Loftee-only into annotated file")
    mergedVcf = "../05.annot_vcf/all.sorted.annotated.vcf"
    mergeAnnotLoftee(inputVcf, outputVcf, mergedVcf)
    
    os.system("bgzip {0} && tabix {0}.gz".format(mergedVcf))
    print("### Done")

def mergeAnnotLoftee(annotVcfFn, lofteeVcfFn, mergedVcfFn):
    with open(annotVcfFn) as _annotVcf:
        annotVcf = _annotVcf.readlines()
    
    with open(lofteeVcfFn) as _lofteeVcf:
        lofteeVcf = _lofteeVcf.readlines()
    
    annotVcf_lines = [k for k in annotVcf if not k.startswith("#")]
    lofteeVcf_lines = [k for k in lofteeVcf if not k.startswith("#")]


    with open(mergedVcfFn, "w") as mergedVcf:
        mergedVcf.write(annotVcf[0]+annotVcf[1])
        mergedVcf.write('##INFO=<ID=CSQ,Number=.,Type=String,Description="Consequence annotations from Ensembl VEP. Format: Allele|Consequence|IMPACT|SYMBOL|Gene|Feature_type|Feature|BIOTYPE|EXON|INTRON|HGVSc|HGVSp|cDNA_position|CDS_position|Protein_position|Amino_acids|Codons|Existing_variation|DISTANCE|STRAND|FLAGS|SYMBOL_SOURCE|HGNC_ID|SOURCE|NEAREST|LoF|LoF_filter|LoF_flags|LoF_info|MisDb|MisDb_MPC">\n')

        mergedVcf.write("##LoF=Loss-of-function annotation (HC = High Confidence; LC = Low Confidence\n")
        mergedVcf.write("##LoF_filter=Reason for LoF not being HC\n")
        mergedVcf.write("##LoF_flags=Possible warning flags for LoF\n")
        mergedVcf.write("##LoF_info=Info used for LoF annotation\n")
        mergedVcf.write(annotVcf[3]+annotVcf[4]+lofteeVcf[10]+annotVcf[6]+annotVcf[7])
    

        for num in range(len(annotVcf_lines)):
            annotLine = annotVcf_lines[num].strip().split("\t")
            annotInfo = annotLine[-1].split(";")
            annotCSQ = annotInfo[1].split("|")
    
            lofteeLine = lofteeVcf_lines[num].strip().split("\t")
            lofteeInfo = lofteeLine[-1].split(";")
            lofteeCSQ = lofteeInfo[2].split("|")

            annotLofteeCSQ = annotCSQ[:-2] + lofteeCSQ[-4:] + annotCSQ[-2:]
            annotLofteeInfo = ";".join([annotInfo[0], "|".join(annotLofteeCSQ),annotInfo[2]])

            mergedVcf.write("\t".join(annotLine[:-1]+[annotLofteeInfo])+"\n")


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('-p', '--process',required=False, type=str, help='Processors: default=20', default='20', metavar='')
    args=parser.parse_args()

    runCwasAnnotationAndLoftee(args.process)


if __name__ == "__main__":
    main()
