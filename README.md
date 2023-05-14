# data-apps
Data Apps


# Create Conda Virtualenv
```
CONDA_SUBDIR=osx-64 conda create -n snowpark python=3.8 numpy pandas --override-channels -c https://repo.anaconda.com/pkgs/snowflake
conda activate snowpark
conda config --env --set subdir osx-64
```