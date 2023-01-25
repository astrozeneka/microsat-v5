import os
from glob import glob
from utils import *
import slugify

def fetch_chromosome_list(genome, driver):
    print("Fetching chromosomes - " + genome[0])
    outfile_name = f"../data/chromosome_list/{os.path.basename(genome[4])}-{slugify.slugify(genome[0])}.tsv"
    if os.path.exists(outfile_name):
        print(f"Skip")
        return
    driver.get(genome[4])
    script = f"""
output = []
chromosomes = document.querySelectorAll(".genome_replicons tr[align=center]")
chromosomes.forEach(chromosome=>output.push(chromosome.querySelector('a').href))
return output
"""
    output = driver.execute_script(script)
    output = "\n".join(output)

    with open(outfile_name, "w") as f:
        f.write(output)

if __name__ == '__main__':
    driver = get_driver()

    subgroup_list = [f for f in glob("data/genome-list-1/*.tsv")]
    subgroup_list = [os.path.basename(f).split(".")[0] for f in subgroup_list]

    for subgroup in subgroup_list:
        with open(f"../data/genome-list-1/{subgroup}.tsv") as f:
            genome_list = f.read().split("\n")
            genome_list = [l for l in genome_list if l.strip() != ""]
            genome_list = [l.split("\t") for l in genome_list]

        for genome in genome_list:
            fetch_chromosome_list(genome, driver)