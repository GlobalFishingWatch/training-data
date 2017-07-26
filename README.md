# About

This is a training dataset for machine learning solutions for detecting fishing events as well as gear type by analyzing AIS vessel tracks.

# Usage and data formats

We use the data as training data for our [vessel scoring library](https://github.com/GlobalFishingWatch/vessel-scoring), and you might find it usefull to check out that code to get started with the dataset.

The data is stored in [numpy format](http://www.numpy.org/). We recommend exploring the data using the jupyter/numpy/scipy/scikit-learn/tensorflow stack.

## Tools
Vessel tracks and labels are stored separately, and need to be
combined for some applications. This is done using a tool included in
the repo:

    ./prepare.sh
    
Some of the data is stored using [git-lfs](https://help.github.com/articles/installing-git-large-file-storage/),
so you'll need to install `git-lfs` before cloning the repo. This also means that downloading a zipped tarball
of the directory is unlikely to work.

# LICENSE

This dataset is licensed under a [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/).

<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a>
