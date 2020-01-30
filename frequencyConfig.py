import numpy as np

## channel raster

F_ref # RF reference frequecy
N_ref # NR Absolute Radio Frequency Channel Number (NR-ARFCN) range:[0:2016666]
deltaF_global # granularity of the global frequency raster


F_ref = F_refoffs + deltaF_global * (N_ref - N_refoffs)

# n41 deltaF_raster = 30kHz
N_ref = 499200:6:537996
    
# n79 deltaF_raster = 30kHz
N_ref = 693334:2:733332

## 

F_CBlow = 2515
F_CBhigh = 2615
N_RB = 273
offsetToCarrier = 0
subcarrierSpacing = 30
F_ref = (F_CBlow + F_CBhigh)/2 # 需满足上述关系
F_low = F_ref - (N_RB * 12)/2 * scs/1000 # 可转化为ARFCN
pointA = F_low - offsetToCarrier * 12 * scs/1000
guardBandLow = (F_low - F_CBlow) - 30/2  # kHz
F_high = F_ref + (N_RB * 12 - 1) / 2 * scs/1000
guardBandHigh = (F_CBhigh - F_high) - 30/2  # kHz

def freq2Arfcn(freq):
  pass

def arfcn2Freq(arfcn):
  pass
