# -*- coding: utf-8 -*-
"""
Time series
"""
from statsmodels.tsa.holtwinters import SimpleExpSmoothing
import math
import numpy as np

turfu=[]
for i in range(10,len(wonderframe)):
    print(i)
    fit=SimpleExpSmoothing(wonderframe['Historique'][i][-i-1:]).fit(smoothing_level=0.6,optimized=True)
    turfu.append(fit.forecast(1)[0])

diff=0
for i in range(10,len(turfu)):
    diff+=(wonderframe["Livraisons réelles"][10+i]-turfu[i])**2
diff=math.sqrt(diff)

turfuDeBase=[]
for i in range(len(wonderframe)):
    a=np.mean(wonderframe['Historique'][i][-i-1:])
    turfuDeBase.append(a)

diffDeBase=0
for i in range(len(turfuDeBase)):
    diffDeBase+=(wonderframe["Livraisons réelles"][i]-turfuDeBase[i])**2
diffDeBase=math.sqrt(diff)