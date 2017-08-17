import serial
import time
from Wiki_Bot import logHeartRate

dataStack = []
bpm_sum = 0
ibi_sum = 0
num_dataPoints = 0

heartPort = serial.Serial("/dev/cu.usbmodem1411", 115200)
while(heartPort.is_open):
    time_start = time.time()
    while(time.time() - time_start <= 30):
        data = heartPort.readline()
        data = data.strip().decode("utf-8")
        dataCSV = data.split(',')
        dataStack.append(dataCSV)
        #print(dataCSV)

    #average the values
    for dataPoint in dataStack:
        bpm_sum += float(dataPoint[0])
        ibi_sum += float(dataPoint[1])
        num_dataPoints += 1

    bpm_avg = round(bpm_sum/float(num_dataPoints), 2)
    ibi_avg = round(ibi_sum/float(num_dataPoints), 2) #TODO: Calculate Stdev of IBI and BPM

    print(bpm_avg, ibi_avg)

    logHeartRate(ibi_avg, bpm_avg) #send data to the wikibot to be logged

    #TODO: Add ability to stop sending data when HR monitor is taken off / stops sending HR data

#print(dataStack)