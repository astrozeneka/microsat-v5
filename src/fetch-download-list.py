
import os
from glob import glob
from utils import *
import slugify

if __name__ == '__main__':
    download_list=[]
    genome_list=[]
    subgroup_list = [f for f in glob("../data/summaries/*.tsv")]
    subgroup_list = [os.path.basename(f).split(".")[0] for f in subgroup_list]
    for subgroup in subgroup_list:
        with open(f"../data/summaries/{subgroup}.tsv") as f:
            _genome_list=f.read().split("\n")[1:]
            _genome_list=[a for a in _genome_list if a.strip() != ""]
            _genome_list=[a.split("\t") for a in _genome_list]
            _genome_list=[a for a in _genome_list if "YES" in a[6]]
            genome_list=genome_list+_genome_list

    # Parse genome by genome
    for genome in genome_list:
        id=genome[7]
        chromosome_list_file=glob(f"../data/chromosome-list/{id}*")

        if len(chromosome_list_file) == 0:
            print("File not found : " + f"../data/chromosome-list/{id}*")
        chromosome_list_file=chromosome_list_file[0]
        with open(chromosome_list_file) as f:
            chromosome_list=f.read().split("\n")
            chromosome_list=[a.split("\t")[1] for a in chromosome_list]
            chromosome_list=[os.path.basename(a) for a in chromosome_list]
            download_list=download_list+chromosome_list

    with open("../data/download-list.txt", "w") as f:
        f.write("\n".join(download_list))
    print("Done")