import serial
import csv
import time
import numpy as np

PORT = "/dev/cu.usbserial-0001"
BAUD = 460800

DURATION_SECONDS = 10
OUTPUT_FILE = "fft_data.csv"

print("Opening ESP32 serial port...")

ser = serial.Serial(PORT, BAUD, timeout=1)

# Allow serial connection to settle
time.sleep(2)

# Remove any old buffered data
ser.reset_input_buffer()

# Discard first complete line in case it is partial/startup data
ser.readline()

print("Recording FFT dataset for 10 seconds...")

start_time = time.time()
rows = []

previous_timestamp = None

while time.time() - start_time < DURATION_SECONDS:

    try:
        line = ser.readline().decode(
            "utf-8",
            errors="ignore"
        ).strip()

        if not line:
            continue

        parts = line.split(",")

        if len(parts) != 2:
            continue

        timestamp_us = int(parts[0])
        raw = float(parts[1])

        # Reject obviously corrupted timestamp jumps
        if previous_timestamp is not None:

            dt = timestamp_us - previous_timestamp

            # Expected interval is ~2000 us.
            # Allow reasonable tolerance.
            if dt < 1500 or dt > 2500:
                previous_timestamp = timestamp_us
                continue

        rows.append([
            timestamp_us,
            raw
        ])

        previous_timestamp = timestamp_us

    except ValueError:
        continue

ser.close()

with open(OUTPUT_FILE, "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow([
        "timestamp_us",
        "raw"
    ])

    writer.writerows(rows)

print()
print("Capture complete!")
print("Samples collected:", len(rows))
print("Saved to:", OUTPUT_FILE)

if len(rows) > 2:

    timestamps = np.array(
        [row[0] for row in rows]
    )

    dt = np.diff(timestamps)

    median_dt = np.median(dt)

    measured_fs = 1_000_000 / median_dt

    print(
        "Median sampling interval:",
        round(median_dt, 2),
        "us"
    )

    print(
        "Measured sampling frequency:",
        round(measured_fs, 2),
        "Hz"
    )