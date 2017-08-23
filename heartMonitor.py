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
    while (time.time() - time_start <= 60):
        data = heartPort.readline()
        data = data.strip().decode("utf-8")
        if data == 'BEAT':
            print("Beat!")
        else:
            dataCSV = data.split(',')
            dataStack.append(dataCSV)


    #average the values
    for dataPoint in dataStack:
        if dataPoint[0] == 0:
            # ignore datapoints without valid BPM
            pass
        else:
            bpm_sum += float(dataPoint[0])
            ibi_sum += float(dataPoint[1])
            num_dataPoints += 1.0

    bpm_avg = round(bpm_sum / num_dataPoints, 2)
    ibi_avg = round(ibi_sum / num_dataPoints, 2)  #TODO: Calculate Stdev of IBI and BPM

    print(bpm_avg, ibi_avg)

    if bpm_avg < 40:
        # person probably isn't wearing it, so don't post
        print('Not posting b/c not a valid BPM!')
    else:
        logHeartRate(ibi_avg, bpm_avg)  # send data to the wikibot to be logged
        dataStack = []  # reset tracker
        num_dataPoints = 0
        bpm_sum = 0
        ibi_sum = 0

#print(dataStack)