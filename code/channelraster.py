class Channelraster(object):

    def __init__(self, FreqBandIndicator, ChannelBandwidthLow, ChannelBandwidthHigh, rbNum, offsetToCarrier,
                 subcarrierSpacing):
        self.FreqBandIndicator = FreqBandIndicator
        self.ChannelBandwidthLow = ChannelBandwidthLow
        self.ChannelBandwidthHigh = ChannelBandwidthHigh
        self.rbNum = rbNum
        self.offsetToCarrier = offsetToCarrier
        self.subcarrierSpacing = subcarrierSpacing

    def getChannelArrangement(self):
        freqBandData = [["n41", 499200, 537996, 6],
                        ["n77", 620000, 680000, 2],
                        ["n78", 620000, 653332, 2],
                        ["n79", 693334, 733332, 2]]
        for freqInfo in freqBandData:
            if(self.FreqBandIndicator == freqInfo[0]):
                arfcnLow = freqInfo[1]
                arfcnHigh = freqInfo[2]
                step = freqInfo[3]
        freqList = []
        for arfcn in range(arfcnLow, arfcnHigh + 1, step):
            freq = self.arfcn2Freq(arfcn)
            freqList.append(freq)
        return freqList

    def getReferenceFrequecy(self, valueType):
        Freftmp = (self.ChannelBandwidthLow + self.ChannelBandwidthHigh) / 2
        channelArrangement = self.getChannelArrangement()
        for freq in channelArrangement:
            if (Freftmp <= freq):
                break
        if (valueType == 0):
            return freq
        if (valueType == 1):
            return self.freq2Arfcn(freq)

    def getTranmissionBandwidthLow(self, valueType):
        referenceFrequecy = self.getReferenceFrequecy(0)
        tranBandwidthLowFreq = referenceFrequecy - (self.rbNum * 12) / 2 * self.subcarrierSpacing / 1000
        if (valueType == 0):
            return tranBandwidthLowFreq
        if (valueType == 1):
            return self.freq2Arfcn(tranBandwidthLowFreq)

    def getTranmissionBandwidthHigh(self, valueType):
        referenceFrequecy = self.getReferenceFrequecy(0)
        tranBandwidthHighFreq = referenceFrequecy + (self.rbNum * 12 / 2 - 1) * self.subcarrierSpacing / 1000
        if (valueType == 0):
            return tranBandwidthHighFreq
        if (valueType == 1):
            return self.freq2Arfcn(tranBandwidthHighFreq)

    def getGuardBandLow(self):
        tranBandwidthLowFreq = self.getTranmissionBandwidthLow(0)
        guardBandLow = (tranBandwidthLowFreq - self.ChannelBandwidthLow) * 1000 - self.subcarrierSpacing / 2  # kHz
        return guardBandLow

    def getGuardBandHigh(self):
        tranBandwidthHighFreq = self.getTranmissionBandwidthHigh(0)
        guardBandHigh = (self.ChannelBandwidthHigh - tranBandwidthHighFreq) * 1000 - self.subcarrierSpacing / 2  # kHz
        return guardBandHigh

    def getPointA(self, valueType):
        tranBandwidthLowFreq = self.getTranmissionBandwidthLow(0)
        pointAFreq = tranBandwidthLowFreq - self.offsetToCarrier * 12 * self.subcarrierSpacing / 1000
        if (valueType == 0):
            return pointAFreq
        if (valueType == 1):
            return self.freq2Arfcn(pointAFreq)

    def freq2Arfcn(slef, freq):
        if ((freq >= 0) and (freq < 3000)):
            arfcn = (freq - 0) / (5 / 1000) + 0
        if ((freq >= 3000) and (freq <= 24250)):
            arfcn = (freq - 3000) / (15 / 1000) + 600000
        return int(arfcn)

    def arfcn2Freq(self, arfcn):
        if ((arfcn >= 0) and (arfcn <= 599999)):
            Fref = 0 + 5 / 1000 * (arfcn - 0)
        if ((arfcn >= 600000) and (arfcn <= 2016666)):
            Fref = 3000 + 15 / 1000 * (arfcn - 600000)
        return Fref

    def infoPrint(self):
        print("频段范围：", self.ChannelBandwidthLow, "-", self.ChannelBandwidthHigh, "MHz")
        print("传输带宽：", self.rbNum)
        print("offsetToCarrier：", self.offsetToCarrier)
        print("子载波间隔：", self.subcarrierSpacing, "kHz")

        print("中心频点：", format(self.getReferenceFrequecy(0),'.3f'), self.getReferenceFrequecy(1))
        print("最低频点：", format(self.getTranmissionBandwidthLow(0), '.3f'), self.getTranmissionBandwidthLow(1))
        print("最高频点：", format(self.getTranmissionBandwidthHigh(0), '.3f'), self.getTranmissionBandwidthHigh(1))
        print("下保护带：", format(self.getGuardBandLow(), '.2f'), "kHz")
        print("上保护带：", format(self.getGuardBandHigh(), '.2f'), "kHz")
        print("point A：", format(self.getPointA(0), '.3f'), self.getPointA(1))