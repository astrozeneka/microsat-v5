
import os
from glob import glob
from utils import *
import slugify

def fetch_taxonomy(genome, driver):
    print("Fetching taxonomy - " + genome[0])
    driver.get(genome[4])
    output = driver.execute_script("""
    output=[]
list=document.querySelectorAll('.GenomeLineage a')
list.forEach(item=>{
    if(item.href.includes("taxonomy"))
        output.push([
            item.innerText,
            item.href
        ])
})
    return output""")
    oufile_name=f"data/taxonomy-list/{os.path.basename(genome[4])}-{slugify.slugify(genome[0])}.tsv"
    with open(oufile_name, "w") as f:
        f.write("\n".join(["\t".join(a) for a in output]))
    return output

if __name__ == '__main__':
    driver = get_driver()

    subgroup_list = [f for f in glob("data/genome-list-1/*.tsv")]
    subgroup_list = [os.path.basename(f).split(".")[0] for f in subgroup_list]

    for subgroup in subgroup_list:
        with open(f"data/genome-list-1/{subgroup}.tsv") as f:
            genome_list = f.read().split("\n")
            genome_list = [l for l in genome_list if l.strip() != ""]
            genome_list = [l.split("\t") for l in genome_list]

        for genome in genome_list:
            fetch_taxonomy(genome, driver)
            print()
