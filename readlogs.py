# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 14:05:54 2015

@author: zah
"""
import re
import glob

from mc2hessian import main
import json

eps_re = r".*eps(\d+)"
nparams_re = r".*hessian_(\d+)\.log"
info_re = r"\- Iteration\: (\d+)  ERF\: ([\d.]+)"


folders = glob.glob("logsN/*")


datapoints = []


class ParsingError(Exception):
    pass

def parse_eps(foldername):
    return float(re.search(eps_re, foldername).group(1))/100.

def parse_nparams(filename):
    return int(re.search(nparams_re, filename).group(1))

def parse_replicas_from_lines(lines):
    return [int(r) for r in re.findall('\d+', lines)]

def parse_infoline(infoline):
    match = re.search(info_re, infoline)
    it = int(match.group(1))
    erf = float(match.group(2))
    return it, erf
    
def get_last_results(filename):
    with open(filename) as f:
        linereplicas = []    
        for endline in reversed(f.readlines()):
            if endline.startswith(' [Error]'):
                raise ParsingError("Error in log File")
            if not endline.startswith("- Iteration:"):
                linereplicas += [endline]
            else:
                break
        infoline = endline
        replicas = parse_replicas_from_lines(' '.join(reversed(linereplicas)))
        it, erf = parse_infoline(infoline)
        return replicas, it, erf
                
            
def read_all_logs():
    for foldername in folders:
        #data = {}
        eps = parse_eps(foldername)
        filenames = glob.glob("%s/*.log"%foldername)
        for filename in filenames:
            nparams = parse_nparams(filename)
            try:
                replicas, it, erf = get_last_results(filename)
            except ParsingError:
                continue
            yield {'eps':eps, 
                   'nparams':nparams, 
                   'replicas':replicas, 
                   'it':it, 
                   'erf':erf,}

def compute_real_erf(flt = None):
    for d in read_all_logs():
        if flt and (d['eps'], d['nparams']) in flt:
            continue
        d['real_erf'] = main('1000rep', d['nparams'], Q=1, epsilon=100 ,
                        basis=d['replicas'], 
                        no_grid=True)
        yield d
if __name__ == '__main__':
    with open('db3.json') as f:
        db = json.load(f)
        s = {(d['eps'], d['nparams']) for d in db}
            
    with open('db3.json', 'w') as f:
        db += [stuff for stuff in compute_real_erf(flt=s)]
        json.dump(db, f, indent=4)
