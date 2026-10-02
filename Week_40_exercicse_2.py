import json
import pandas as pd

sensor_values = {}

with open("config.yml", mode="r", encoding="utf-8") as config:
    # Open the YAML file and extract the relevant information
    for lines in config:
        line = lines.split(": ")
        # If the value is the calibration assign to a value and other wanted values to other variables
        if line[0] == "max_days_since_calibration":
            m_calib = line[1].strip("\n")
        elif line[0] == "output_file":
            o_file = line[1].strip("\n").strip('"')
# print(f"{m_calib} and {o_file}")

sensor_info = pd.read_excel("sensors.xlsx")
# Open the file with pandas and put sensor_info in a dictionary with the sensor_id as a key
for sensor in sensor_info.itertuples():
    print(sensor.sensor_id)
    sensor_values[sensor.sensor_id] = {"location": sensor.lab_room, "owner": sensor.owner}
# print(sensor_values)

relevant_sensors = []

with open("calibrations.csv", mode="r", encoding="utf-8") as calib:
    # Open the csv file and put the relevant values in a dictionary
    line_number = 0
    for lines in calib:
        # Skip the first line
        if line_number == 0:
            line_number += 1
            continue
        line = lines.split(",")
        # print(line)
        # Look up the relevant information in the dictionary and extract it
        s_id = line[0]
        sensor_owner_info = sensor_values[s_id]
        # print(f"{s_id}: {sensor_owner_info['owner']}")
        # Filter out the sensors bellow the threshold
        if int(m_calib) < int(line[1]):
            print(f"{s_id}: {sensor_owner_info['owner']}")
            relevant_sensors.append(
                {
                    "sensor_id": s_id,
                    "lab": sensor_owner_info["location"],
                    "owner": sensor_owner_info["owner"],
                    "days_since_calibration": line[1].strip("\n"),
                }
            )

with open(o_file, mode="w", encoding="utf-8") as data_file:
    # Put the dictionary into a JSON file and give it the wanted name
    json.dump(relevant_sensors, fp=data_file, indent=2)
