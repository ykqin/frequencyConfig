class Channelraster():
    
    def __init__(self, FreqBandIndicator, ChannelBandwidthLow, ChannelBandwidthHigh, rbNum, offsetToCarrier, subcarrierSpacing):
        self.FreqBandIndicator = FreqBandIndicator
        self.ChannelBandwidthLow = ChannelBandwidthLow
        self.ChannelBandwidthHigh = ChannelBandwidthHigh
        self.rbNum = rbNum
        self.offsetToCarrier = offsetToCarrier
        self.subcarrierSpacing = subcarrierSpacing
        
    def getChannelArrangement(self):
        if(self.FreqBandIndicator == "n41"):
            arfcnLow = 499200
            arfcnHigh = 537996
            step = 6
        freqList = []
        for arfcn in range(arfcnLow, arfcnHigh+1,  step):
            freq = self.arfcn2Freq(arfcn)
            freqList.append(freq)
        return freqList
        
    def getReferenceFrequecy(self):
        Freftmp = (self.ChannelBandwidthLow + self.ChannelBandwidthHigh)/2
        channelArrangement = self.getChannelArrangement()
        for freq in channelArrangement:
            if(Freftmp <= freq):
                break
        return freq
    
    def getTranmissionBandwidthLow(self, valueType):
        referenceFrequecy = self.getReferenceFrequecy()
        tranBandwidthLowFreq = referenceFrequecy - (self.rbNum * 12)/2 * self.subcarrierSpacing/1000
        if(valueType == "Frequency"):
            return tranBandwidthLowFreq
        if(valueType == "ARFCN")
            return self.freq2Arfcn(tranBandwidthLowFreq)      
    
    def getTranmissionBandwidthHigh(self, valueType):
        referenceFrequecy = self.getReferenceFrequecy()
        tranBandwidthHighFreq = referenceFrequecy + (self.rbNum * 12 - 1)/2 * self.subcarrierSpacing/1000
        if(valueType == "Frequency"):
            return tranBandwidthHighFreq
        if(valueType == "ARFCN")
            return self.freq2Arfcn(tranBandwidthHighFreq)
    
    def getGuardBandLow(self):
        tranBandwidthLowFreq = self.getTranmissionBandwidthLow("Frequency")
        guardBandLow = (tranBandwidthLowFreq - self.ChannelBandwidthLow)*1000 - self.subcarrierSpacing/2  # kHz
        return guardBandLow
    
    def getGuardBandHigh(self):
        tranBandwidthHighFreq = self.getTranmissionBandwidthHigh("Frequency")
        guardBandHigh = (self.ChannelBandwidthHigh - tranBandwidthHighFreq)*1000 - self.subcarrierSpacing/2  # kHz
        return guardBandHigh  
    
    def getPointA(self, valueType):
        tranBandwidthLowFreq = self.getTranmissionBandwidthLow("Frequency")
        pointAFreq = tranBandwidthLowFreq - self.offsetToCarrier * 12 * self.subcarrierSpacing/1000
        if(valueType == "Frequency"):
            return pointAFreq
        if(valueType == "ARFCN")
            return self.freq2Arfcn(pointAFreq)
        
    def freq2Arfcn(slef, freq):
        if((freq >= 0)and(freq < 3000)):
            arfcn = (freq - 0)/(5/1000) + 0
        if((freq >= 3000)and(freq <= 24250)):
            arfcn = (freq - 3000)/(15/1000) + 600000
        return arfcn

    def arfcn2Freq(self, arfcn):
        if((arfcn >= 0)and(arfcn <= 599999)):
            Fref = 0 + 5/1000 * (arfcn - 0)
        if((arfcn >= 600000)and(arfcn <= 2016666)):
            Fref = 3000 + 15/1000 * (arfcn - 600000)
        return Fref
        
#a = Channelraster("n41",2515,2615,273,0,30)
#b = a.getReferenceFrequecy()
#print(b)
