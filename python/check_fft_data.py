import pandas as pd
import numpy as np

df = pd.read_csv("fft_data.csv")

t = df["timestamp_us"].to_numpy()

dt = np.diff(t)

print("Samples:", len(df))
print("First timestamp:", t[0])
print("Last timestamp:", t[-1])

print()
print("Median dt:", np.median(dt), "us")
print("Mean dt:", np.mean(dt), "us")
print("Minimum dt:", np.min(dt), "us")
print("Maximum dt:", np.max(dt), "us")

print()
print("Intervals around 2000 us:",
      np.sum((dt >= 1900) & (dt <= 2100)),
      "out of",
      len(dt))

print("Intervals > 10000 us:",
      np.sum(dt > 10000))

print("Intervals <= 0:",
      np.sum(dt <= 0))

# Show biggest timestamp gaps
largest = np.argsort(dt)[-10:][::-1]

print("\nLargest gaps:")

for index in largest:
    print(
        f"Row {index} -> {index+1}: "
        f"{dt[index]} us"
    )