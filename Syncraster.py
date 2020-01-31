class Syncraster():
    
    def __init__(self, FreqBandIndicator, tranBandwidthLowFreq, tranBandwidthHighFreq, subcarrierSpacing):
        self.FreqBandIndicator = FreqBandIndicator
        self.tranBandwidthLowFreq = tranBandwidthLowFreq
        self.tranBandwidthHighFreq = tranBandwidthHighFreq
        self.subcarrierSpacing = subcarrierSpacing
        
    def getSyncArrangement(self):
        if(self.FreqBandIndicator == "n41"):
            gscnLow = 6252
            gscnHigh = 6714
            step = 3
        freqList = []
        for GSCN in range(gscnLow, gscnHigh + 1,  step):
            freq = self.GSCN2freq(GSCN)
            freqList.append(freq)
        return freqList
        
    def getSSrefList(self):
        
        # 
        SSrefLow = self.tranBandwidthLowFreq + (10 + 12) * 12 * 0.03
        SSrefHigh = self.tranBandwidthHighFreq - ((10 + 12) * 12 - 1)*0.03
        GSCNstep = 1 
        
        syncArrangement = self.getSyncArrangement()
        for idx in range(len(syncArrangement)):
            if(SSrefLow <= syncArrangement[idx]):
                SSrefLowIdx = idx
                break
        for idx in range(len(syncArrangement)):
            idx = len(syncArrangement) - idx - 1
            if(SSrefHigh >= syncArrangement[idx]):
                SSrefHighIdx = idx
                break
                
        SSrefList = []
        for idx in range(SSrefLowIdx, SSrefHighIdx + 1, GSCNstep):
            freq = syncArrangement(idx)
            SSrefList.append(freq)
        return SSrefList
    
    def getOffset(self):
        SSrefList = self.getSSrefList()
        SSrefLow = SSrefList[0]
        
        deltaRB = floor(SSrefLow - 10 * 12 * 0.03 - self.tranBandwidthLowFreq)/(12 * 0.03)
        deltaRE = mod((SSrefLow - self.tranBandwidthLowFreq)*1000, 15)
        offsetList = [12, 14, 16]
        for offset in offsetList:
            if(deltaRB >= offset):
                break
        rbStartCoreset0 = deltaRB - offset
        
        self.deltaRE = deltaRE
        self.offset = offset
        self.rbStartCoreset0 = rbStartCoreset0             
        
    def freq2GSCN(slef, freq):
        M = 3
        if((freq >= 0)and(freq < 3000)):
            N = (freq - M * 0.05)/1.2
            GSCN = 3 * N + (M - 3)/2
        if((freq >= 3000)and(freq <= 24250)):
            N = (freq - 3000)/1.44
            GSCN = 7499 + N
        return GSCN

    def GSCN2freq(self, GSCN):
        if((GSCN >= 0)and(GSCN <= 7498)):
            M = 3
            N = (GSCN - (M - 3)/2)/3            
            freq = N * 1.2 + M * 0.05
        if((GSCN >= 7499)and(GSCN <= 22255)):
            N = GSCN - 7499
            freq = 3000 + N * 1.44
        return freq
