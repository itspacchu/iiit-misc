# The MIT License (MIT)

# Copyright (c) 2015 Prashant Nandipati (prashantn@riseup.net)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
    