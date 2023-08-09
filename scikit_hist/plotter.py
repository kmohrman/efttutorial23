import os
import matplotlib.pyplot as plt
import topcoffea.modules.utils as utils

import hist
from topcoffea.modules.histEFT import HistEFT

WCPT_EXAMPLE = {
    "ctW"  : -0.74,
    "ctZ"  : -0.86,
    "ctp"  : 24.5,
    "cpQM" : -0.27,
    "ctG"  : -0.81,
    "cbW"  : 3.03,
    "cpQ3" : -1.71,
    "cptb" : 0.13,
    "cpt"  : -3.72,
    "cQl3i": -4.47,
    "cQlMi": 0.51,
    "cQei" : 0.05,
    "ctli" : 0.33,
    "ctei" : 0.33,
    "ctlSi": -0.07,
    "ctlTi": -0.01,
    "cQq13": -0.05,
    "cQq83": -0.15,
    "cQq11": -0.15,
    "ctq1" : -0.20,
    "cQq81": -0.50,
    "ctq8" : -0.50,
}

# Takes a hist with one sparse axis and one dense axis, overlays everything on the sparse axis
def make_single_fig(histo,unit_norm_bool):
    #print("\nPlotting values:",histo.values())
    fig, ax = plt.subplots(1, 1, figsize=(7,7))
    histo.plot1d(
        stack=False,
        density=unit_norm_bool,
    )
    ax.autoscale(axis='y')
    return fig


def main():

    histo_in = "histos_multilepeft.pkl.gz"

    # Get the histograms
    hin_dict = utils.get_hist_from_pkl(histo_in,allow_empty=False)

    histo = hin_dict["j0pt"]

    # Values
    #print("Values with overflow:",histo.values(overflow="over")[('ttHJet_privateUL17',)])
    #print("Sum:",sum(histo.values(overflow="over")[('ttHJet_privateUL17',)]))

    #histo.set_wilson_coefficients(**WCPT_EXAMPLE)

    fig = make_single_fig(histo, unit_norm_bool=False)
    title = "ttH_2l_histo"
    fig.savefig(os.path.join(".",title))



main()

