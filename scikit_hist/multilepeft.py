#!/usr/bin/env python
import numpy as np
import awkward as ak
np.seterr(divide='ignore', invalid='ignore', over='ignore')
from coffea import processor
from coffea.analysis_tools import PackedSelection

from topcoffea.modules.GetValuesFromJsons import get_lumi
#from topcoffea.modules.HistEFT import HistEFT
import topcoffea.modules.eft_helper as efth
import topcoffea.modules.objects as obj

import hist
from topcoffea.modules.histEFT import HistEFT

class AnalysisProcessor(processor.ProcessorABC):
    def __init__(self, samples, wc_names_lst=[]):
        self._samples = samples
        self._wc_names_lst = wc_names_lst


        # Create the histograms with new scikit hist
        self._histo_dict = {
            "j0pt": HistEFT(
                hist.axis.StrCategory([], growth=True, name="process"),
                hist.axis.Regular(name="j0pt",label="Leading jet $p_{T}$ (GeV)", bins=10, start=0, stop=600, flow=True),
                wc_names = self._wc_names_lst,
                label="Events",
            )
        }


    @property
    def columns(self):
        return self._columns

    def process(self, events):

        # Dataset parameters
        dataset = events.metadata['dataset']
        hist_axis_name = self._samples[dataset]["histAxisName"]
        year   = self._samples[dataset]['year']
        xsec   = self._samples[dataset]['xsec']
        sow    = self._samples[dataset]['nSumOfWeights' ]

        # Extract the EFT quadratic coefficients and optionally use them to calculate the coefficients on the w**2 quartic function
        # eft_coeffs is never Jagged so convert immediately to numpy for ease of use.
        eft_coeffs = ak.to_numpy(events['EFTfitCoefficients']) if hasattr(events, "EFTfitCoefficients") else None
        if eft_coeffs is not None:
            # Check to see if the ordering of WCs for this sample matches what want
            if self._samples[dataset]['WCnames'] != self._wc_names_lst:
                eft_coeffs = efth.remap_coeffs(self._samples[dataset]['WCnames'], self._wc_names_lst, eft_coeffs)

        # Initialize objects
        ele  = events.Electron
        mu   = events.Muon
        jets = events.Jet


        ######## Lep selection  ########

        e_selec = ((ele.pt>20) & (abs(ele.eta)<2.5))
        m_selec = ((mu.pt>20) & (abs(mu.eta)<2.5))
        leps = ak.concatenate([ele[e_selec],mu[m_selec]],axis=1)


        ######## Jet selection  ########

        jets = jets[(jets.pt>30) & (abs(jets.eta)<2.5)]
        jets_clean = jets[obj.isClean(jets, leps, drmin=0.4)]
        j0 = jets_clean[ak.argmax(jets.pt,axis=-1,keepdims=True)]


        ######## Event selections ########

        nleps = ak.num(leps)
        njets = ak.num(jets_clean)

        at_least_two_leps = ak.fill_none(nleps>=2,False)
        at_least_two_jets = ak.fill_none(njets>=2,False)

        selections = PackedSelection()
        selections.add('2l2j', at_least_two_leps & at_least_two_jets)


        ######## Normalization ########

        # Normalize by (xsec/sow)
        lumi = 1000.0*get_lumi(year)
        norm = (xsec/sow)*lumi
        wgts = norm*np.ones_like(events['event'])


        ######## Fill histos ########

        j0pt = j0.pt

        hout = {"j0pt": self._histo_dict["j0pt"]}

        event_selection_mask = selections.all("2l2j")
        hout["j0pt"].fill(
            process   = hist_axis_name,
            j0pt      = j0pt[event_selection_mask],
            eft_coeff = eft_coeffs[event_selection_mask],
        )

        return hout

    def postprocess(self, accumulator):
        return accumulator

