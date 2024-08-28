#!/home/dcha/anaconda3/envs/cwas/bin/python3

import os,sys

def cwasformatted_vcf(iPath, vcfFn, oPath):
    newVcfFn=vcfFn.replace("02.extracted_vcf",oPath.split("/")[0]).replace(".soft.vcf", ".soft.converted.vcf")
    with open(iPath+vcfFn) as vcf:
        lines = vcf.readlines()
    with open(iPath+newVcfFn, "w") as newVcf:
        print("Generating "+iPath+newVcfFn+"...\n")
        for l in lines:
            if l.startswith("##"):
                continue
            elif l.startswith("#"):
                newVcf.write("\t".join(l.split("\t")[:8])+"\n")
            elif l.startswith("chrX") or l.startswith("chrY") or l.startswith("chrM"):
                continue
            else:
                sampleName="SAMPLE="+newVcfFn.split(oPath)[1].split(".MT")[0]
                newVcf.write("\t".join(l.split("\t")[:7]+[sampleName])+"\n")
#    print("Extracted sample information from input VCFs")

def cwasAllInOneVcf(path, iPath, oPath):
    iVcfs= [path+iPath+vcfN for vcfN in os.listdir(path+iPath)]
    
    os.system('grep "^#" {0} > {1}{2}all.sorted.vcf'.format(iVcfs[0], path, oPath))

    os.system('touch {0}{1}all.unsorted.vcf'.format(path, oPath))

    for iVcf in iVcfs:
        os.system('grep -v "^#" {0} >> {1}{2}all.unsorted.vcf'.format(iVcf, path, oPath))
    
    os.system('cat {0}{1}all.unsorted.vcf | sort -k1,1V -k2,2n >> {0}{1}all.sorted.vcf'.format(path, oPath))

    os.system('rm {0}{1}all.unsorted.vcf'.format(path, oPath))

    os.system('bgzip {0}{1}all.sorted.vcf > {0}{1}all.sorted.vcf.gz\
            && tabix -p vcf {0}{1}all.sorted.vcf.gz'.format(path, oPath))
    print("\nGenerated all-in-one {0}{1}all.sorted.vcf for CWAS".format(path, oPath))

if __name__ == "__main__":
    path="/home/dcha/cwas/"
    vcfPath="02.extracted_vcf/"
    convertedPath="03.converted_vcf/"
    readyPath="04.ready_vcf/"

    os.system("mkdir -p {0}{1} && mkdir -p {0}{2}".format(path, convertedPath, readyPath))

    for vcfName in os.listdir(path+vcfPath):
        cwasformatted_vcf(path, vcfPath+vcfName, convertedPath)

    cwasAllInOneVcf(path, convertedPath, readyPath)
