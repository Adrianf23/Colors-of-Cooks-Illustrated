The Covers of Cook's Illustrated
==============================

A color analysis of the covers of Cook's Illustrated from 1992-2024 using k-means clustering.

![Animated gif of magazines with their kmeans representation](https://github.com/Adrianf23/Colors-of-Cooks-Illustrated/blob/main/reports/figures/compressed-magazine-covers.gif)




Project Organization
------------

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    ├── data (generated with commands)
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── conda-lock.yml     <- The lock file for reproducing this project, e.g.
    │                         generated with `conda-lock lock -f environment.yml`
    │
    │
    ├── environment.yml    <- The environment file for reproducing this project, e.g.
    │                         generated with `conda env export --from-history -f environment.yml -c conda-forge`
    │
    ├── src                <- Source code for use in this project.
    |   ├── old_script     <- Original scripts to download data
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    |   |   └── gather_magazines.py
    |   |   └── kmeans.py
    |   |   └── run_gather_magazines.py
    |   |   └── run_kmeans.py
    │   │
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── gif_maker.py
    │       └── visualize.py

Get Started
--------
Clone the repository

- HTTPS: `git clone https://github.com/Adrianf23/Colors-of-Cooks-Illustrated.git`
- SSH: `git clone git@github.com:Adrianf23/Colors-of-Cooks-Illustrated.git`

Create an environment with conda-lock. I use micromamba, but you can substitute conda or mamba. 

- `micromamba create -n [ENV_NAME] -c conda-forge conda-lock --yes`

Download the necessary packages using conda-lock

- `conda-lock install --name [ENV_NAME_2] conda-lock.yml`


--------

Disclaimer: This project contains copyrighted material, the use of which has not been endorsed by America's Test Kitchen/Marquee Branchs. I believe my exploratory use meets the “fair use” prerequisite provided for in section 107 of the US Copyright Law. I do not claim ownership of any images and no images are for sale. The cover images shown are copyright by the original publisher.


<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>

