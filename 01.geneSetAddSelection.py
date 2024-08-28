#!/home/dcha/anaconda3/envs/cwas/bin/python3

from collections import OrderedDict
import os,sys, argparse

def import_gene_matrix(fn, wfn, addonPath, toInclude = None):

    with open(fn) as rf:
        oldHeader = rf.readline().strip().split("\t")
        oldContents = [k.strip().split("\t") for k in rf.readlines()]
    gmDic = OrderedDict()
    
    addonFiles = [addonPath+k for k in os.listdir(addonPath)]

    if toInclude:
        newHeader = ["gene_id", "gene_name"]+toInclude
    else:
        newHeader = oldHeader

    
    for x in oldContents:
        gene_n = x[1]
        gmDic[gene_n] = []
        for k in newHeader:
            gmDic[gene_n]+=[x[oldHeader.index(k)]]
            
    for afn in addonFiles:
        if afn.endswith(".txt"):
            with open(afn) as af:
                geneSetName = af.readline().strip()
                print("processing "+geneSetName+" genes...")
                geneSets = [k.strip() for k in af.readlines()]
                newHeader+=[geneSetName]
                for k in gmDic.keys():
                    gmDic[k]+=[0]
                    for g in geneSets:
                        if g == k:
                            gmDic[k][-1]+=1
#    print(gmDic)
#    print(newHeader)
    
    with open(wfn, "w") as wf:
        wf.write("\t".join(newHeader)+"\n")
        for k in gmDic.keys():
            wf.write("\t".join([str(j) for j in gmDic[k]])+"\n")


if __name__ == "__main__":
    toInclude = sys.argv[1:]
    cwasPath = "/home/dcha/cwas"
    addonPath = cwasPath+"/00.gene_sets_additional/"
    import_gene_matrix(cwasPath+"-dataset/gene_matrix_raw.txt",\
            cwasPath+"-dataset/gene_matrix.txt", addonPath, toInclude = None)


