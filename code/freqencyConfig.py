
from channelraster import Channelraster
from syncraster import Syncraster

def freqConfig(FreqBandIndicator, ChannelBandwidthLow, ChannelBandwidthHigh, rbNum, offsetToCarrier, subcarrierSpacing, coreset0RBnum, minChBandwidth):
    channelFreq = Channelraster(FreqBandIndicator, ChannelBandwidthLow, ChannelBandwidthHigh, rbNum, offsetToCarrier, subcarrierSpacing)
    tranBandwidthLow = channelFreq.getTranmissionBandwidthLow(0)
    tranBandwidthHigh = channelFreq.getTranmissionBandwidthHigh(0)
    ssbFreq = Syncraster(FreqBandIndicator, tranBandwidthLow, tranBandwidthHigh, subcarrierSpacing, coreset0RBnum, minChBandwidth)
    channelFreq.infoPrint()
    ssbFreq.infoPrint()

if __name__ == '__main__':

    freqConfig("n41", 2515, 2615, 273, 0, 30, 48, 10)   # ChinaMobile2p6
    freqConfig("n79", 4800, 4900, 273, 0, 30, 48, 40)  # ChinaMobile4p9
    freqConfig("n78", 3400, 3500, 273, 0, 30, 48, 10)   # ChinaTelecom3p5
    freqConfig("n78", 3500, 3600, 273, 0, 30, 48, 10)   # ChinaUnicom3p5
