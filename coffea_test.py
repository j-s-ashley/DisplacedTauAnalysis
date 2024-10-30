import uproot
import scipy
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
import awkward as ak
import math
import ROOT
import array
import pandas as pd
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
from leptonPlot import *

NanoAODSchema.warn_missing_crossrefs = False

file = "/eos/user/d/dally/DisplacedTauAnalysis/SMS-TStauStau_MStau-100_ctau-100mm_mLSP-1_TuneCP5_13p6TeV_NanoAOD.root"

events = NanoEventsFactory.from_root({file:"Events"}).events()

gpart = events.GenPart
electrons = events.Electron
muons = events.Muon
staus = gpart[(abs(gpart.pdgId) == 1000015) & (gpart.hasFlags("isLastCopy"))]

staus_taus = staus.distinctChildren[(abs(staus.distinctChildren.pdgId) == 15) & (staus.distinctChildren.hasFlags("isLastCopy"))]
staus_taus = ak.flatten(staus_taus, axis=2)

gen_mus = staus_taus.distinctChildren[(abs(staus_taus.distinctChildren.pdgId) == 13)]
gen_electrons = staus_taus.distinctChildren[(abs(staus_taus.distinctChildren.pdgId) == 11)]
RecoElectronsFromGen = electrons[(abs(electrons.matched_gen.distinctParent.distinctParent.pdgId) == 1000015)]

gen_electrons = gen_electrons[(gen_electrons.pt > 20) & (abs(gen_electrons.eta) < 2.4)]
RecoElectronsFromGen = RecoElectronsFromGen.matched_gen[(RecoElectronsFromGen.matched_gen.pt > 20) & (abs(RecoElectronsFromGen.matched_gen.eta) < 2.4)]

makeEffPlot("e", "coffea_100GeV_100mm", [""], "pt", 16, 20, 100, 5, "[GeV]", [gen_electrons.pt.compute()], [RecoElectronsFromGen.pt.compute()], 0, file) 
