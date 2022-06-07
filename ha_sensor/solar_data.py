from onem2m import *

NodeList = [
    ["AE-SL","SL-NI03-01"],
    ["AE-SL","SL-VN02-01"],
    ["AE-SL","SL-NI03-00"],
    ["AE-SL","SL-VN95-00"],
    ["AE-SL","SL-VN03-00"],
    ["AE-SL","SL-VN02-00"]
]

SolarNodes = []
TotalEnergy = 0
AverageVoltage = 0
AverageCurrent = 0
PowerGenerated = 0

def isnan(val):
    if(str(val) == 'nan'):
        return True
    return False

for node,subnode in NodeList:
    SolarNodes.append(SolarNode(node,subnode))

for node in SolarNodes:
    data = node.getData()
    thisEnergy = data['energy']
    thisVoltage = data['voltage']
    thisCurrent = data['current']
    thisPower = data['power']
    if(not isnan(thisPower)):
        PowerGenerated += thisPower
    if(not isnan(thisVoltage)):
        AverageVoltage += thisVoltage
    if(not isnan(thisEnergy)):
        TotalEnergy += thisEnergy
    if(not isnan(thisCurrent)):
        AverageCurrent += thisCurrent

print({
        "total_energy":TotalEnergy,
        "total_power":PowerGenerated,
        "avg_voltage":AverageVoltage,
        "avg_current":AverageCurrent
})
    