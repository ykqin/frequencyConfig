

# channel raster

F_ref # RF reference frequecy
N_ref # NR Absolute Radio Frequency Channel Number (NR-ARFCN) range:[0:2016666]
deltaF_global # granularity of the global frequency raster


F_ref = F_refoffs + deltaF_global * (N_ref - N_refoffs)
