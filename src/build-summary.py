
import os
from glob import glob
from utils import *
import slugify

TAXONOMY_CLASSES={}
def get_taxonomy_class(taxonomy):
    global TAXONOMY_CLASSES
    name=taxonomy[0]
    url=taxonomy[1]
    if os.path.basename(url) + "-" + slugify.slugify(name) in TAXONOMY_CLASSES.keys():
        return TAXONOMY_CLASSES[os.path.basename(url) + "-" + slugify.slugify(name)]
    with open("../data/taxonomy-list/" + os.path.basename(url) + "-" + slugify.slugify(name) + ".tsv") as f:
        taxonomy_data=f.read().split("\t")
    taxonomy_data=[a for a in taxonomy_data if "(" not in a]
    TAXONOMY_CLASSES[os.path.basename(url) + "-" + slugify.slugify(name)]=taxonomy_data+[taxonomy[0]]
    return taxonomy_data+[taxonomy[0]]

if __name__ == '__main__':

    subgroup_list = [f for f in glob("../data/genome-list-1/*.tsv")]
    subgroup_list = [os.path.basename(f).split(".")[0] for f in subgroup_list]

    for subgroup in subgroup_list:
        subgroup_report = []

        with open(f"../data/genome-list-1/{subgroup}.tsv") as f:
            genome_list = f.read().split("\n")
            genome_list = [l for l in genome_list if l.strip() != ""]
            genome_list = [l.split("\t") for l in genome_list]

        for genome in genome_list:
            # Load genome taxonomy list (for the summary table)
            with open(f"../data/genome-taxonomy-list/{os.path.basename(genome[4])}-{slugify.slugify(genome[0])}.tsv") as f:
                lineage=f.read().split("\n")
                lineage=[a for a in lineage if a.strip() != ""]
                lineage=[a.split("\t") for a in lineage]
                entry_data = [get_taxonomy_class(a) for a in lineage]
                entry_data = {a[0]:a[-1] for a in entry_data if len(a) >= 2}

            with open(f"../data/chromosome-list/{os.path.basename(genome[4])}-{slugify.slugify(genome[0])}.tsv") as f:
                chromosome_data=f.read().split("\n")
                chromosome_data=[a for a in chromosome_data if a.strip() != ""]
                chromosome_data=[a.split("\t") for a in chromosome_data]
                entry_data["chromosome-length"]=len([c for c in chromosome_data if c[0].lower() != "MT" and c[0] != "-"])

                sex_chromosomes=[a[0] for a in chromosome_data if a[0].lower() in "xyzw"]
                entry_data["sex-chromosomes"]=','.join(sex_chromosomes)
                subgroup_report.append(entry_data)


        # Build the outfile table
        output=[["Class", "Order", "Family", "Specie", "Chromosomes available for use", "Sex chromosomes", "Eligibility"]]
        for genome in subgroup_report:
            entry=[]
            entry.append(genome["class"] if "class" in genome.keys() else "")
            entry.append(genome["order"] if "order" in genome.keys() else "")
            entry.append(genome["family"] if "family" in genome.keys() else "")
            entry.append(genome["species"] if "species" in genome.keys() else "")
            entry.append(genome["chromosome-length"] if "chromosome-length" in genome.keys() else 0)
            entry.append(genome["sex-chromosomes"] if "sex-chromosomes" in genome.keys() else "")

            # Conditionnal values
            if entry[-2]==0:
                continue
            entry.append("YES" if entry[-2]>0 and len(entry[-1])>0 else "NO")
            output.append(entry)

        # Write in file
        with open(f"../data/summaries/{subgroup}.tsv", "w") as f:
            f.write("\n".join("\t".join([str(b) for b in a]) for a in output))
    print("Done")