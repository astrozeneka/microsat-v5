
import os
from glob import glob
from utils import *
import slugify

if __name__ == '__main__':

    subgroup_list = [f for f in glob("../data/summaries/*.tsv")]
    subgroup_list = [os.path.basename(f).split(".")[0] for f in subgroup_list]
    for subgroup in subgroup_list:
        pass