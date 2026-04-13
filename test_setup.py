# test_setup.py – Testar att miljön fungerar

# Först: installera bibliotek genom att köra detta i terminalen (Ctrl+ö):
# pip install yfinance pandas matplotlib

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Hämta kursdata för Volvo B, senaste året
aktie = yf.download("VOLV-B.ST", period="1y")

# Beräkna daglig procentuell avkastning
aktie["Daglig avkastning"] = aktie["Close"].pct_change()

# Skriv ut lite grundläggande info
print("=== Volvo B – Senaste året ===")
print(f"Antal handelsdagar: {len(aktie)}")
print(f"Högsta stängningskurs: {aktie['Close'].max().item():.2f} SEK")
print(f"Lägsta stängningskurs: {aktie['Close'].min().item():.2f} SEK")
print(f"Genomsnittlig daglig avkastning: {aktie['Daglig avkastning'].mean().item():.4%}")
print(f"Volatilitet (std daglig): {aktie['Daglig avkastning'].std().item():.4%}")

# Plotta stängningskursen
plt.figure(figsize=(10, 5))
plt.plot(aktie.index, aktie["Close"])
plt.title("Volvo B – Stängningskurs senaste året")
plt.xlabel("Datum")
plt.ylabel("SEK")
plt.grid(True)
plt.tight_layout()
plt.show()