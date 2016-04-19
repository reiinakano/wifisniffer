import AccessPoint
import CommPair

APList = []
APList.append(AccessPoint.AccessPoint("22313", 1))
APList.append(AccessPoint.AccessPoint("212114", 1))
CommPairList = []
CommPairList.append(CommPair.CommunicatingPair(APList[0], "sasa", 44))

print CommPairList[0].AP == APList[0]
print CommPairList[0].AP is APList[0]