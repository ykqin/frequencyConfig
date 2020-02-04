import math


class Syncraster(object):

    def __init__(self, FreqBandIndicator, tranBandwidthLowFreq, tranBandwidthHighFreq, subcarrierSpacing, coreset0RBnum, minChBandwidth):
        self.FreqBandIndicator = FreqBandIndicator
        self.tranBandwidthLowFreq = tranBandwidthLowFreq
        self.tranBandwidthHighFreq = tranBandwidthHighFreq
        self.subcarrierSpacing = subcarrierSpacing
        self.minChBandwidth = minChBandwidth
        self.coreset0RBnum = coreset0RBnum

    def getSyncArrangement(self):
        freqBandData = [["n41", 6252, 6714, 3],
                        ["n77", 7711, 8329, 1],
                        ["n78", 7711, 8051, 1],
                        ["n79", 8480, 8880, 16]]
        for freqInfo in freqBandData:
            if(self.FreqBandIndicator == freqInfo[0]):
                gscnLow = freqInfo[1]
                gscnHigh = freqInfo[2]
                step = freqInfo[3]
        freqList = []
        for GSCN in range(gscnLow, gscnHigh + 1, step):
            freq = self.GSCN2freq(GSCN)
            freqList.append(freq)
        return freqList

    def getSSrefLow(self, valueType):
        offsetList = self.getOffsetList()
        rbTmp = offsetList[0]
        SSrefLow = self.tranBandwidthLowFreq + (10 + rbTmp) * 12 * 0.03
        syncArrangement = self.getSyncArrangement()
        for idx in range(len(syncArrangement)):
            if (SSrefLow <= syncArrangement[idx]):
                SSrefLowIdx = idx
                break
        if(valueType == 0):
            return syncArrangement[SSrefLowIdx]
        if(valueType == 1):
            return self.freq2GSCN(syncArrangement[SSrefLowIdx])

    def getSSrefHigh(self, valueType):
        offsetList = self.getOffsetList()
        rbTmp = self.coreset0RBnum - offsetList[len(offsetList)-1] - 20
        SSrefHigh = self.tranBandwidthHighFreq - ((10 + rbTmp) * 12 - 1) * 0.03
        syncArrangement = self.getSyncArrangement()
        for idx in range(len(syncArrangement)):
            idx = len(syncArrangement) - idx - 1
            if (SSrefHigh >= syncArrangement[idx]):
                SSrefHighIdx = idx
                break
        if(valueType == 0):
            return syncArrangement[SSrefHighIdx]
        if(valueType == 1):
            return self.freq2GSCN(syncArrangement[SSrefHighIdx])

    def getOffset(self):
        SSrefLow = self.getSSrefLow(0)
        deltaRB = math.floor((SSrefLow - 10 * 12 * 0.03 - self.tranBandwidthLowFreq) / (12 * 0.03))
        offsetList = self.getOffsetList()
        for idx in range(len(offsetList)):
            if (deltaRB < offsetList[idx]):
                break
        offsetRB = offsetList[idx-1]
        rbStartCoreset0 = deltaRB - offsetRB
        offsetRE = math.floor((SSrefLow - (10 + deltaRB)*12*0.03 - self.tranBandwidthLowFreq) * 1000 / 15)
        return offsetRB, offsetRE, rbStartCoreset0

    def freq2GSCN(slef, freq):
        M = 3
        if ((freq >= 0) and (freq < 3000)):
            N = (freq - M * 0.05) / 1.2
            GSCN = 3 * N + (M - 3) / 2
        if ((freq >= 3000) and (freq <= 24250)):
            N = (freq - 3000) / 1.44
            GSCN = 7499 + N
        return int(GSCN)

    def GSCN2freq(self, GSCN):
        if ((GSCN >= 0) and (GSCN <= 7498)):
            M = 3
            N = (GSCN - (M - 3) / 2) / 3
            freq = N * 1.2 + M * 0.05
        if ((GSCN >= 7499) and (GSCN <= 22255)):
            N = GSCN - 7499
            freq = 3000 + N * 1.44
        return freq

    def getOffsetList(self):
        if ((self.minChBandwidth == 5) or (self.minChBandwidth == 10)):
            if (self.coreset0RBnum == 24):
                offsetList = [0, 1, 2, 3, 4]
            if (self.coreset0RBnum == 48):
                offsetList = [12, 14, 16]
        if (self.minChBandwidth == 40):
            if (self.coreset0RBnum == 24):
                offsetList = [0, 4]
            if (self.coreset0RBnum == 48):
                offsetList = [0, 28]
        return offsetList

    def infoPrint(self):
        offsetRB, offsetRE, rbStartCoreset0 = self.getOffset()
        print("SSB中心频点范围：", format(self.getSSrefLow(0), '.2f'), "-", format(self.getSSrefHigh(0), '.2f'), "MHz")
        print("SSB中心频点范围：", self.getSSrefLow(1), "-", self.getSSrefHigh(1))
        print("SSB中心频点：", format(self.getSSrefLow(0),'.2f'), self.getSSrefLow(1))
        print("RB级偏移：", offsetRB)
        print("RE级偏移：", offsetRE)
        print("CORESET0起始RB：", rbStartCoreset0)
        print("\n")