#!/usr/bin/python3

import os,sys


#os.system("mkdir -p ./tmp")
#os.system("mv ./all.sorted.*.txt ./tmp")
def main(path, fn):
    with open(path+fn) as rf:
        with open(path+fn.replace("all.sorted.","sSnv."), "w") as ssnv:
            with open(path+fn.replace("all.sorted.","coding.sSnv."), "w") as coding:
                with open(path+fn.replace("all.sorted.", "noncoding.sSnv."), "w") as noncoding:
                    with open(path+fn.replace("all.sorted.", "merged.sSnv."), "w") as merged:
                        with open(path+"coding_category_set.txt", "w") as codingCat:
                            with open(path+"noncoding_category_set.txt", "w") as noncodingCat:
                                header = rf.readline()
                                ssnv.write(header)
                                coding.write(header)
                                noncoding.write(header)
                                codingCat.write("Category\n")
                                noncodingCat.write("Category\n")
                                for l in rf.readlines():
                                    if l.startswith("SNV_"):
                                        ml=l.replace("_All","").replace("_Any","").replace("SNV_", "")
                                        if ml == "SNV":
                                            continue
                                        ssnv.write(ml)
                                        mltype = ml.strip().split("\t")[4]
                                        if mltype in ["CodingRegion", "PTVRegion", "DamagingMissenseRegion", "MissenseRegion", "SilentRegion"]:
                                            merged.write(ml)
                                            coding.write(ml)
                                            codingCat.write(l.split("\t")[0]+"\n")
                                        elif mltype in ["NoncodingRegion", "5PrimeUTRsRegion", "3PrimeUTRsRegion", "SpliceSiteRegion", "PromoterRegion",\
                                                "IntergenicRegion", "IntronRegion", "lincRnaRegion", "OtherTranscriptRegion"]:
                                            merged.write(ml)
                                            noncoding.write(ml)
                                            noncodingCat.write(l.split("\t")[0]+"\n")

if __name__ == "__main__":
    try:
        path1= "../07.binomial_test_samples/"
        fn1 = "all.sorted.burden_test.txt"
        main(path1, fn1)
    except:
        pass

    try:
        path2 = "../07.binomial_test_variants/"
        fn2 = "all.sorted.burden_test.txt"
        main(path2, fn2)
    except:
        pass
