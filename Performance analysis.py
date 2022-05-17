# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.8
#   kernelspec:
#     display_name: Python [conda env:forte_benchmarking] *
#     language: python
#     name: conda-env-forte_benchmarking-py
# ---

# # Preview of IonQ Forte gate performance
#
# In this notebook, we perform the analysis presented in "Unveiling IonQ Forte: First Software-Configurable Quantum Computer".

# ## 2Q gate survey

# As noted in the [blog post](https://ionq.com/posts/may-17-2022-ionq-forte), we perform a broad survey of our two-qubit gates by repeated concatenation, as detailed in [this](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.125.150505) recent paper. This gives us a coarse sense of overall gate performance.

# First, we load in the data:

import pandas
with open('data/survey_data.csv','r') as file:
    survey_data = pandas.read_csv(file,index_col=0)
survey_data

# Here, we store the first qubit index in q0 and the second in q1, with the infidelity recorded in parts per ten thousand (pptt).

# We generate the histogram and summary statistics from the blog post:

# +
import matplotlib.pyplot as plt
import numpy as np

plt.figure(figsize=(10,8))
infidelity_vec = np.array(survey_data['infidelity'])
bins = np.logspace(np.log10(min(infidelity_vec)/2), np.log10(max(infidelity_vec)*2), 30)
plt.hist(infidelity_vec,bins=bins)
plt.xscale('log')
plt.xlabel('Infidelity [pptt]')
plt.ylabel('Occurrence')
plt.title(f'XX gate survey, IonQ Forte, 31-qubit configuration')
fmean = np.mean(infidelity_vec)
fstd = np.std(infidelity_vec)
plt.text(0.05,0.95,f'Avg. Infidelity = {fmean:.0f}({fstd:.0f}) pptt', 
         horizontalalignment='left', verticalalignment='top', fontsize=14,
         bbox=dict(facecolor='orange', alpha=0.8), transform=plt.gca().transAxes)
plt.grid(which='both')
plt.ylim(0, 100)
plt.show()
# -


# We see that our infidelity is $36 \pm 27$ pptt. In addition, we see that we are missing one data point (7,29), as described in the blog post. 

# ## GST analysis

# Now that we have extablished an overall performance baseline, we would like to diagnose what is phsyically going in. We use [Gate set tomography](https://quantum-journal.org/papers/q-2021-10-05-557/), which is a well-established technique in the literature for examining the detailed performance of quantum gates. 
#
# The downside of gate set tomography is that all the detail it reports comes at a cost of requiring many experiments. For this initial performance characterization, we picked one pair of qubits (10 and 21), chosen arbitrarily. From the survey data, we see that they have performance near the middle of the pack:

survey_data[(survey_data.q0 == 10)*(survey_data.q1 == 21)]

# We load the appropriate 2-qubit model from pygsti and run it. Note that this will take a while depending on your system.

# +
import pygsti
from pygsti.modelpacks import smq2Q_XYXX

data = pygsti.io.read_data_from_dir(f"data/smq2Q_XYXX")
protocol = pygsti.protocols.StandardGST("CPTP", optimizer={'tol': 1e-3}, verbosity=4)
results = protocol.run(data, memlimit=12*(1024)**3,)
# -

# Write the results to disk as a report:

report = pygsti.report.construct_standard_report(
    results, title="XX GST IonQ Forte", verbosity=2)
report.write_html('gst_resport', verbosity=2)
results.write()
