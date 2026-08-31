import serial
import csv
import time
import numpy as np

PORT = "/dev/cu.usbserial-0001"
BAUD = 460800
DURATION_SECONDS = 10
OUTPUT_FILE = "raw_data.csv"

print("Opening ESP32 serial port...")

ser = serial.Serial(PORT, BAUD, timeout=1)

# Allow ESP32 serial connection to initialise
time.sleep(2)

# Remove any old data already waiting in the serial buffer
ser.reset_input_buffer()

# Discard first line
ser.readline()

print("Recording for 10 seconds...")

start_time = time.time()

rows = []
previous_timestamp = None

while time.time() - start_time < DURATION_SECONDS:

    try:
        line = ser.readline().decode("utf-8", errors="ignore").strip()

        if not line:
            continue

        parts = line.split(",")

        if len(parts) != 4:
            continue

        timestamp_us = int(parts[0])
        raw = float(parts[1])
        moving_average = float(parts[2])
        iir = float(parts[3])

        # Check timestamp spacing after the first valid sample
        if previous_timestamp is not None:

            dt = timestamp_us - previous_timestamp

            # Expected interval is approximately 2000 us
            if dt < 1500 or dt > 2500:
                previous_timestamp = timestamp_us
                continue

        rows.append([
            timestamp_us,
            raw,
            moving_average,
            iir
        ])

        previous_timestamp = timestamp_us

    except ValueError:
        continue

ser.close()

with open(OUTPUT_FILE, "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow([
        "timestamp_us",
        "raw",
        "moving_average",
        "iir"
    ])

    writer.writerows(rows)

print()
print("Capture complete!")
print("Samples collected:", len(rows))
print("Saved to:", OUTPUT_FILE)

if len(rows) > 2:

    timestamps = np.array([row[0] for row in rows])

    dt = np.diff(timestamps)

    median_dt = np.median(dt)

    measured_fs = 1_000_000.0 / median_dt

    duration = (
        timestamps[-1] - timestamps[0]
    ) / 1_000_000.0

    print("Median sampling interval:", round(median_dt, 2), "us")
    print("Measured sampling frequency:", round(measured_fs, 2), "Hz")
    print("Recorded timestamp duration:", round(duration, 3), "seconds")