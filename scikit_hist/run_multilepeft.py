#!/usr/bin/env python
import json
import cloudpickle
import gzip
import os

from coffea import processor
from coffea.nanoevents import NanoAODSchema

import multilepeft

if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser(description='You can customize your run')
    parser.add_argument('jsonfile'       , nargs='?', default=''           , help = 'Json file(s) containing files and metadata')
    parser.add_argument('--nworkers','-n' , default=8  , help = 'Number of workers')
    parser.add_argument('--chunksize','-s', default=100000  , help = 'Number of events per chunk')
    parser.add_argument('--nchunks','-c'  , default=None  , help = 'You can choose to run only a number of chunks')
    parser.add_argument('--outname','-o'  , default='histos_multilepeft', help = 'Name of the output file with histograms')
    parser.add_argument('--treename'      , default='Events', help = 'Name of the tree inside the files')
    parser.add_argument('--wc-list'       , action='extend', nargs='+', help = 'Specify a list of Wilson coefficients to use in filling histograms.')

    args = parser.parse_args()
    nworkers  = int(args.nworkers)
    chunksize = int(args.chunksize)
    nchunks   = int(args.nchunks) if not args.nchunks is None else args.nchunks
    json_file = args.jsonfile
    outname   = args.outname
    treename  = args.treename

    # Load samples from json and setup the inputs to the processor
    samplesdict = {}
    json_file_name = json_file.split(".json")[0] # Drop the .json
    with open(json_file) as jf:
        samplesdict[json_file_name] = json.load(jf)
    flist = {json_file_name: samplesdict[json_file_name]["files"]}

    #wc_lst = args.wc_list if args.wc_list is not None else []
    wc_lst = samplesdict[json_file_name]["WCnames"]

    # Run the processor and get the output
    processor_instance = multilepeft.AnalysisProcessor(samplesdict,wc_lst)
    exec_instance      = processor.FuturesExecutor(workers=nworkers)
    runner             = processor.Runner(exec_instance, schema=NanoAODSchema, chunksize=chunksize, maxchunks=nchunks)
    output             = runner(flist, treename, processor_instance)

    # Save the output
    outpath = "."
    if not os.path.isdir(outpath): os.system("mkdir -p %s"%outpath)
    out_pkl_file = os.path.join(outpath,outname+".pkl.gz")
    print(f"\nSaving output in {out_pkl_file}...")
    with gzip.open(out_pkl_file, "wb") as fout:
        cloudpickle.dump(output, fout)
    print("Done!")
