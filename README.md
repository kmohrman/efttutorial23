# efttutorial23

Example scripts for the Fermilab EFT tutorial 2023 (DRAFT VERSION). 

## Setting up 

Download the example root file:
```
wget -nc http://www.crc.nd.edu/~kmohrman/files/root_files/for_ci/ttHJet_UL17_R1B14_NAOD-00000_10194_NDSkim.root
```

Set up the repository:
```
git clone https://github.com/kmohrman/efttutorial23.git
cd efttutorial23/scikit_hist
```
The processor depends on `topcoffea`, so that should be installed into your conda environment. 

## Running the processor

Example of running the processor over just the example root file we downloaded.
```
python run_multilepeft.py UL17_ttH_example.json
```
This will create a `histos_multilepeft.pkl.gz` file with an EFT histogram. 

## Plotting the histograms

Run the plotting script:
```
python plotter.py
```
