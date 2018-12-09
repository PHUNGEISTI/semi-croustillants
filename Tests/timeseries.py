# -*- coding: utf-8 -*-
"""
Time series
"""
from statsmodels.tsa.holtwinters import SimpleExpSmoothing
import math
import numpy as np
from formatage import wonderframe
from sklearn.metrics import mean_squared_error

turfu=[]
for i in range(10,len(wonderframe)):
    fit=SimpleExpSmoothing(wonderframe['Historique'][i][-i-1:]).fit(smoothing_level=0.6,optimized=True)
    turfu.append(fit.forecast(1)[0])

diff=0
for i in range(10,len(turfu)):
    diff+=(wonderframe["Livraisons réelles"][10+i]-turfu[i])**2
diff=math.sqrt(diff/len(turfu))

turfuDeBase=[]
for i in range(len(wonderframe)):
    a=np.mean(wonderframe['Historique'][i][-i-1:])
    turfuDeBase.append(a)

diffDeBase=0
for i in range(len(turfuDeBase)):
    diffDeBase+=(wonderframe["Livraisons réelles"][i]-turfuDeBase[i])**2
diffDeBase=math.sqrt(diffDeBase/len(turfuDeBase))
diffDeBase=math.sqrt(mean_squared_error(wonderframe['Livraisons réelles'].values,turfuDeBase))

turfuLourd=[]
for i in range(len(wonderframe)):
    a=np.average(wonderframe['Historique'][i][-i-1:],weights=[i+1 for i in range(i+1)])
    turfuLourd.append(a)

diffLourd=0
for i in range(len(turfuLourd)):
    diffLourd+=(wonderframe["Livraisons réelles"][i]-turfuLourd[i])**2
diffLourd=math.sqrt(diffLourd/len(turfuLourd))
