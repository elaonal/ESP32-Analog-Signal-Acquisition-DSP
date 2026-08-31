import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# LOAD FFT DATA
# ==========================================

FILE = "fft_data.csv"

df = pd.read_csv(FILE)

print("======================================")
print("FFT FREQUENCY ANALYSIS")
print("======================================")

print("Samples loaded:", len(df))


# ==========================================
# CALCULATE ACTUAL SAMPLING FREQUENCY
# ==========================================

timestamps = df["timestamp_us"].to_numpy()

dt_us = np.diff(timestamps)

median_dt_us = np.median(dt_us)

fs = 1_000_000.0 / median_dt_us

print(
    "Median sampling interval:",
    round(median_dt_us, 2),
    "us"
)

print(
    "Measured sampling frequency:",
    round(fs, 2),
    "Hz"
)


# ==========================================
# PREPARE SIGNAL
# ==========================================

signal = df["raw"].to_numpy()

# Remove DC offset / 1.65 V bias component
signal_centered = signal - np.mean(signal)

N = len(signal_centered)


# ==========================================
# APPLY HANN WINDOW
# ==========================================

window = np.hanning(N)

windowed_signal = signal_centered * window


# ==========================================
# FFT
# ==========================================

fft_values = np.fft.rfft(windowed_signal)

frequencies = np.fft.rfftfreq(
    N,
    d=1.0 / fs
)

magnitude = np.abs(fft_values)


# ==========================================
# FIND DOMINANT FREQUENCY
# ==========================================

# Ignore DC bin
magnitude[0] = 0

dominant_index = np.argmax(magnitude)

dominant_frequency = frequencies[dominant_index]

dominant_magnitude = magnitude[dominant_index]

print()
print(
    "Dominant frequency:",
    round(dominant_frequency, 2),
    "Hz"
)

print(
    "Dominant FFT magnitude:",
    round(dominant_magnitude, 2)
)


# ==========================================
# FREQUENCY RESOLUTION
# ==========================================

frequency_resolution = fs / N

print(
    "FFT frequency resolution:",
    round(frequency_resolution, 4),
    "Hz"
)


# ==========================================
# PLOT FFT
# ==========================================

plt.figure(figsize=(12, 6))

plt.plot(
    frequencies,
    magnitude
)

# Focus on useful low-frequency range
plt.xlim(0, 100)

plt.xlabel("Frequency (Hz)")
plt.ylabel("FFT Magnitude")

plt.title(
    "Frequency Spectrum of ESP32 ADC Signal"
)

plt.grid(True)

# Mark detected frequency
plt.axvline(
    dominant_frequency,
    linestyle="--",
    label=f"Peak = {dominant_frequency:.2f} Hz"
)

plt.legend()

plt.tight_layout()

plt.savefig(
    "fft_spectrum.png",
    dpi=300
)

plt.show()

print()
print("FFT graph saved as: fft_spectrum.png")