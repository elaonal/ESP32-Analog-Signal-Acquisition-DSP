from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Project folders
ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT / "data" / "raw_data.csv"
OUTPUT = ROOT / "results" / "raw_vs_filtered.png"

# Load data
df = pd.read_csv(FILE)

timestamps = df["timestamp_us"].to_numpy()
raw = df["raw"].to_numpy()
moving_average = df["moving_average"].to_numpy()
iir = df["iir"].to_numpy()

# Sampling analysis
dt_us = np.diff(timestamps)
median_dt_us = np.median(dt_us)
fs = 1_000_000.0 / median_dt_us

duration = (timestamps[-1] - timestamps[0]) / 1_000_000.0

print("======================================")
print("ANALOG SIGNAL & DSP ANALYSIS")
print("======================================")

print()
print("Samples in CSV:", len(df))

print()
print("--- Sampling ---")
print("Median sampling interval:", round(median_dt_us, 2), "us")
print("Measured sampling frequency:", round(fs, 2), "Hz")
print("Recorded signal duration:", round(duration, 3), "seconds")


def print_stats(name, signal):
    print()
    print(f"--- {name} ---")
    print("Mean:", round(np.mean(signal), 2))
    print("Standard deviation:", round(np.std(signal), 2))
    print("Minimum:", round(np.min(signal), 2))
    print("Maximum:", round(np.max(signal), 2))
    print("Peak-to-peak:", round(np.ptp(signal), 2))


print_stats("Raw ADC", raw)
print_stats("Moving Average", moving_average)
print_stats("IIR", iir)

# Time axis beginning at zero
time_s = (timestamps - timestamps[0]) / 1_000_000.0

plt.figure(figsize=(12, 6))

plt.plot(time_s, raw, label="Raw ADC", alpha=0.6)
plt.plot(time_s, moving_average, label="Moving Average")
plt.plot(time_s, iir, label="IIR α=0.3")

plt.xlabel("Time (s)")
plt.ylabel("ADC Value")
plt.title("ESP32 Raw vs Filtered ADC Signal")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig(OUTPUT, dpi=300)
plt.show()

print()
print("Plot saved to:", OUTPUT)