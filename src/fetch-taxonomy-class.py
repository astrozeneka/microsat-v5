import os
from glob import glob
from utils import *
import slugify
import shutil

def fetch_taxonomy_class(taxonomy, driver):
    taxonomy_slug=f"{os.path.basename(taxonomy[1])}-{slugify.slugify(taxonomy[0])}"
    print(taxonomy_slug)
    outfile = f"../data/taxonomy-list/{taxonomy_slug}.tsv"
    if os.path.isfile(outfile):
        print("Skip")
        return
    driver.get(taxonomy[1])
    output = driver.execute_script("return document.querySelector('p.desc').innerText")
    output = output.split(",")
    output = [a.strip() for a in output]
    with open(outfile, "w") as f:
        f.write("\t".join(output))


if __name__ == '__main__':
    driver = get_driver()

    genome_list = [os.path.basename(a).split(".")[0] for a in glob("../data/genome-taxonomy-list/*.tsv")]

    for genome in genome_list:
        with open(f"../data/genome-taxonomy-list/{genome}.tsv") as f:
            taxonomy_list=f.read().split("\n")
            taxonomy_list=[a for a in taxonomy_list if a.strip() != ""]
            taxonomy_list=[a.split("\t") for a in taxonomy_list]

            for taxonomy in taxonomy_list:
                fetch_taxonomy_class(taxonomy, driver)