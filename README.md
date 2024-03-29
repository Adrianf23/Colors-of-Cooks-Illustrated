The Covers of Cook's Illustrated
==============================

A color analysis of the covers of Cook's Illustrated from 1992-2024 using k-means clustering.

![Animated gif of magazines with their kmeans representation](https://github.com/Adrianf23/Colors-of-Cooks-Illustrated/blob/main/reports/figures/compressed-magazine-covers.gif)

*The design changes in later years, so the pattern breaks. Wabi-sabi!

Get Started
--------
Clone the repository

- HTTPS: `git clone https://github.com/Adrianf23/Colors-of-Cooks-Illustrated.git`
- SSH: `git clone git@github.com:Adrianf23/Colors-of-Cooks-Illustrated.git`

Create an environment with conda-lock. I use micromamba, but you can substitute conda or mamba. 

- `micromamba create -n [ENV_NAME] -c conda-forge conda-lock --yes`

Download the necessary packages using conda-lock. 

> **Note**: this is cross-platform, but it will only work on linux-64, osx-64 and win-64. If you have osx-arm64 or another linux distro, then you cannot download this due to the _playwright_ dependency 

- `conda-lock install --name [ENV_NAME_2] conda-lock.yml`

Download the images, run the KMeans algorithm and export the images as one final gif

- `python (python3) src/data/run_gather_magazines.py`
- `python (python3) src/data/run_kmeans.py`
- `python (python3) src/visualization/visualize.py`

Overview
------------
This project taught me several aspects of data science and Python that I wanted a deeper understanding of.

- Webscraping/Cleaning Data: With **httpx**, **selectolax** and **playwright**, I scraped 200 magazine covers from the Cook's Illustrated website. 
  - I wanted to learn how to make asynchronous functions to decrease the time it took to extract the image links. After that, I made another asyn function to stream in all the images.
  - I also transformed the image data using predicate and projection pushdown in Polars. This was then loaded into parquet files.
- Machine Learning: I employed the KMeans clustering algorithm to gather the top 10 most common colors used on the magazine covers. I reduced the processing time by about 30% with the **Intel® Extension for Scikit-learn**.
- Data Structures: I utilized **Polars** dataframes, **Parquet** files, **NumPy** arrays and **Python** dataclasses to organize my image data.
- Visualization: I created, converted, and compressed the image squares to .gif with **Pillow** and **Matplotlib**. 
- Environment/Package Management: I wanted to create a reproducible build for this project. I decided to use **conda-lock**, which created 3 cross-platform versions of this project (linux-64, osx-64 and win-64).
- System Processes: I used **glob**, **shutil**, and **pathlib** to create folders and locate/copy files.  


Project Organization
------------
> Note: Data is treated as an immutable object in this project, so it is generated on command and processed later.

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
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
    │   └── visualization  <- Scripts to create exploratory and results-oriented visualizations
    │       └── gif_maker.py
    │       └── visualize.py


Acknowledgments
--------
Thank you to <a target="_blank" href="https://github.com/jwilber">Jared Wilber</a> and <a target="_blank" href="https://github.com/jwilber">Jacob Levernier</a> for helping me think through some of the pain points of the project.

Disclaimer
--------

This project contains copyrighted material, the use of which has not been endorsed by America's Test Kitchen/Marquee Brands. I believe my exploratory use meets the “fair use” prerequisite provided for in section 107 of the US Copyright Law. I do not claim ownership of any images and no images are for sale. The cover images shown are copyrighted by the original publisher.


<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>

