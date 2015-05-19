# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 09:24:45 2015

@author: zah
"""
from __future__ import division
import json

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D #analysis:ignore
from matplotlib import tri
import matplotlib.cm as cm
import pandas as pd
import palettable

plt.rc('font', size=25)

def load_data():
    with open('db3.json') as f:
        db = json.load(f)
    return db

if __name__ == '__main__':
    d = pd.DataFrame(load_data())
    #d = d[d.nparams>60]
    #d = d[d['eps'] > 0.15]
    x = d.nparams.as_matrix()
#    xu = np.unique(x)
    y = d.eps.as_matrix()
#    yu = np.unique(y)
    z2= d.erf.as_matrix()
    z = d.real_erf.as_matrix()
    blue_curve = d.ix[d.groupby('eps').erf.apply(np.argmin)]
    black_curve = d.ix[d.groupby('eps').real_erf.apply(np.argmin)]
    black_curve = black_curve[black_curve.nparams > 140]
    
            
#    cset = plt.contour(c, np.blackarangearange(0,5,.5), linewidth=2, colors='k')
#    plt.clabel(cset, inline=True, fmt="%1.1f%%", rotation='vertical' )
#    im = plt.imshow(c, cmap=palettable.colorbrewer.diverging.Spectral_11.mpl_colormap)#'RdBu')
#    plt.colorbar(im)
#    ax = plt.gca()
#    ax.get_xaxis().set_major_locator(LinearLocator(len(xu)), )
#    ax.get_yaxis().set_major_locator(LinearLocator(len(yu[::2])), )
#    ax.get_xaxis().set_major_formatter(FixedFormatter((xu)), )
#    ax.get_yaxis().set_major_formatter(FixedFormatter((yu[::2])), )
#    ax.set_aspect(len(xu)/len(yu))

   
   ##plt.xticks([1,2,3])
    
    
    
    #curve_ga = curve_ga[(curve_ga.eps != 0.2)]

        
        
    t = tri.Triangulation(x,y)
    reft,refz2 = tri.UniformTriRefiner(t).refine_field(z2)
    
    #s2 = ax.plot_trisurf(t, z1, cmap=cm.gray_r, antialiased=False,
    #                    linewidth=0, alpha=0.5)
    for cmap in (#cm.summer, cm.rainbow, 
                 #cm.terrain, 
                 #palettable.colorbrewer.diverging.Spectral_11_r.mpl_colormap,
                 palettable.colorbrewer.diverging.Spectral_11.mpl_colormap,):
        fig = plt.figure(figsize=(8*2.5,4.5*2.5))
        ax = fig.add_subplot(111,projection="3d")
        ax.plot_trisurf(t, z2 + 0.1, color='none', edgecolor='orange', 
                        linewidth=0.1)
        s1 = ax.plot_trisurf(reft, refz2, cmap=cmap, antialiased=False,
                            linewidth=0, alpha=1, 
                            vmin= z2.min(),
                            vmax= d.erf.quantile(.9)
                            )
        
        ax.scatter(x,y,z2 + 0.1,c='darkgrey', lw=0)
        
        
        
        eps25 = d[d['eps']==0.25].sort('nparams')
        plt.plot(eps25.nparams.as_matrix(), eps25.eps.as_matrix(), 
                 eps25.erf.as_matrix(), color='darkred')
        
        plt.plot(blue_curve.nparams.as_matrix(), blue_curve.eps.as_matrix(), 
                 blue_curve.erf.as_matrix(), color='blue', linewidth=2)
        
        #plt.plot(black_curve.nparams.as_matrix(), black_curve.eps.as_matrix(), 
        #         black_curve.erf.as_matrix(), color='black', linewidth=2)
        
        
       # s = ax.plot_trisurf(d.eps,d.real_erf, d.nparams, cmap=cm.rainbow, antialiased=False,linewidth=0)
        ax.set_xlabel("Number of eigenvectors")
        ax.set_ylabel(r"$\varepsilon$", fontsize=30)
        ax.set_zlabel(r"GA Estimator")
        ax.set_xlim(0,200)
        ax.set_zlim(0,600)
        ax.view_init(elev=39, azim=56)
        fig.colorbar(s1)
        #fig.colorbar(s2)
        fig.savefig("/home/zah/Desktop/colors/%s.png" % cmap.name)

plt.figure(figsize = (16,9))
plt.plot(eps25.nparams.as_matrix(), eps25.eps.as_matrix(), color='darkred')
plt.plot(blue_curve.nparams.as_matrix(), blue_curve.eps.as_matrix(), 
         color='blue', linewidth=2)
plt.plot(black_curve.nparams.as_matrix(), black_curve.eps.as_matrix(), 
         color='black', linewidth=2)
plt.xlabel("Number of eigenvectors")
plt.ylabel(r"$\varepsilon$", fontsize=30)

ax.set_xlim(0,200)
