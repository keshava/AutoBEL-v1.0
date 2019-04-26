#Author: David Zhen Yin
#Contact: yinzhen@stanford.edu
#Date: Apr 12, 2018


import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import sys
sys.path.insert(0, 'source_code/')
from grdecl_read_plot import *
import seaborn as sns

def GIIP_cal(m_poro, m_sw, m_thc_coef, bulk_vol, plt_flg):
    '''
    This is the function for the calculation of GIIP
    arg:
        m_poro: the ndarary  of porosity model realizations
        m_sw: the ndarary  of sw model realizations
        m_thc_coef: the ndarray of thickness coeff model realizations
        bulk_vol: the grdecl file of reservoir bulk volume per cell.
    '''
    
    bulk_vol = grdecl_read(bulk_vol,200,100,75)[0].flatten()    
    sg = 1-m_sw
    GIIP = (bulk_vol*m_poro*m_thc_coef*sg).sum(axis=1)/0.6767

    GIIP = np.array(GIIP)
    if plt_flg == True:
        fig, ax1 = plt.subplots(figsize=(7,4.5))
        ax1.hist(GIIP, 24, edgecolor='black', facecolor='aqua')
        plt.xticks(fontsize = 18, fontname='calibri')    
        plt.yticks(fontsize = 18, fontname='calibri') 
        plt.ylabel('count', fontsize = 20, fontname='calibri', weight ='bold')
        plt.xlabel('GIIP', fontsize = 20, fontname='calibri', weight ='bold')
        plt.title('Prior prediction', fontsize=18, loc='left', weight='bold')
        ax2 = ax1.twinx()
        kde = stats.gaussian_kde(GIIP)
        xx = np.linspace(GIIP.min()*0.95, GIIP.max()*1.05, 1000) 
        ax2.plot(xx, kde(xx), '--', linewidth = 2, c='red')
        fig.tight_layout()     
    
    return GIIP
	

def giip_compare(giip_a, giip_b):
    sns.set(style="white",palette='deep', font_scale=1.9)
    plt.subplots(figsize=(8,4.5))
    sns.distplot(giip_a, bins=int(len(giip_a)/10), \
                kde_kws={'linewidth': 2,"color":"blue"}, \
                hist_kws={'color':'aqua',"edgecolor":'black','linewidth':0.6,'alpha':0.95})

    sns.distplot(giip_b, bins=int(len(giip_b)/12.5), \
                kde_kws={'linewidth': 3,  "color":"red", }, \
                hist_kws={'color':'tomato',"edgecolor":'black','linewidth':0.6, 'alpha':0.7})
    return