import csv
import matplotlib.pyplot as plt

time = []
data = []
channel_num = 1 #
#collect_file = "/home/ii-lab/s4_sn1_testing_data/s4_idle_current.csv"
collect_file = "/home/ii-lab/keithley_test_scripts/data.csv"

with open(collect_file, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')

    for row in reader:
        if ("Time" in row[0]):
            print("header")
        else:
            time.append(float(row[0]))
            data.append(1000*float(row[channel_num]))

plt.plot(time,data)
plt.xlabel("Time (sec)")
plt.ylabel("Current (mA)")
plt.title("Idle Current Consumption Vs Time")
plt.show()
