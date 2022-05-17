# Benchmarking IonQ Forte
This notebook and associated data performs the analysis shown in the [blog post](https://ionq.com/posts/may-17-2022-ionq-forte). 

The entire gate set tomography output report can be viewed by opening `gst_report/main.html` in a web browser. To run the analysis yourself, ensure that you have [conda](https://www.anaconda.com) installed on your system. Then, navigate to your `forte_benchmarking` directory in a terminal and run

```
conda env create -f environment.yml
conda activate forte_benchmarking
```

which will install the required dependencies. 

We will be making use of the [pygsti](https://www.pygsti.info) software package to do gate set tomography. Since our gate set is not in pygsti's standard implementation, we will need to install a [modified version](https://github.com/colibri-coruscans/pyGSTi/tree/maunz/MSgates) that includes our native gate set. Navigate to a directory you use for repositories and run

```
git clone git@github.com:colibri-coruscans/pyGSTi.git
cd pyGSTi
git checkout maunz/MSgates
pip install -e .
```

which will clone the version of pygsti with our native gate set and set it up for use with our conda environment. 

The environment is now initialized, so you can now navigate to your `forte_benchmarking` directory and run 

```
jupyter-notebook
```

and a jupyter analysis environment will launch. Opening `Performance analysis.py` will start the analysis notebook.
