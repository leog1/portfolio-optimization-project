"""
data_loader.py – Hämtar historisk kursdata från Yahoo Finance.

Denna modul ansvarar för att ladda ner justerade stängningskurser
för utvalda aktier och spara dem lokalt som CSV-filer.
"""

import yfinance as yf
import pandas as pd
from pathlib import Path


# ---------------------------------------------------------------------------
# Konfiguration – aktier och tidsperiod
# ---------------------------------------------------------------------------

# Tickers för ett urval av stora Stockholmsbörsaktier.
# Suffixet ".ST" talar om för Yahoo Finance att det gäller Stockholmsbörsen.
TICKERS = [
    "VOLV-B.ST",   # Volvo
    "ERIC-B.ST",   # Ericsson
    "SEB-A.ST",    # SEB
    "HEXA-B.ST",   # Hexagon
    "ASSA-B.ST",   # Assa Abloy
    "SAND.ST",     # Sandvik
    "INVE-B.ST",   # Investor
    "ABB.ST",      # ABB
    "ATCO-A.ST",   # Atlas Copco
    "SHB-A.ST",    # Handelsbanken
]

# Tidsperiod: 5 år ger ca 1 250 handelsdagar – tillräckligt för att
# uppskatta kovariansmatrisen men inte så långt att marknadsregimer
# förändrats drastiskt.
START_DATE = "2020-01-01"
END_DATE = "2024-12-31"

# Sökväg till data-mappen (relativ till projektets rot)
DATA_DIR = Path(__file__).resolve().parent.parent / "data"


# ---------------------------------------------------------------------------
# Funktioner
# ---------------------------------------------------------------------------

def fetch_prices(
    tickers: list[str] = TICKERS,
    start: str = START_DATE,
    end: str = END_DATE,
) -> pd.DataFrame:
    """
    Hämtar justerade stängningskurser från Yahoo Finance.

    Parametrar
    ----------
    tickers : list[str]
        Lista med Yahoo Finance-tickersymboler.
    start : str
        Startdatum i formatet "YYYY-MM-DD".
    end : str
        Slutdatum i formatet "YYYY-MM-DD".

    Returnerar
    ----------
    pd.DataFrame
        DataFrame med datum som index och en kolumn per aktie,
        innehållande justerade stängningskurser (SEK).

    Varför "Adj Close"?
    --------------------
    Yahoo Finance rapporterar flera kurser per dag (Open, High, Low, Close).
    "Adjusted Close" justerar stängningskursen för utdelningar och splittar
    så att avkastningsberäkningar blir korrekta.  Om vi använde vanlig
    "Close" skulle en aktiesplit se ut som en kurskrasch — helt missvisande.
    """
    print(f"Hämtar data för {len(tickers)} aktier från {start} till {end}...")

    # yf.download returnerar en DataFrame med MultiIndex-kolumner
    # om man anger flera tickers. Vi väljer "Close" (yfinance ≥0.2.18
    # returnerar justerade värden i "Close" som standard).
    raw = yf.download(tickers, start=start, end=end, auto_adjust=True)

    # Om flera tickers → MultiIndex med ("Close", ticker). Vi plockar ut "Close".
    if isinstance(raw.columns, pd.MultiIndex):
        prices = raw["Close"]
    else:
        # En enda ticker → enkel kolumn
        prices = raw[["Close"]]
        prices.columns = tickers

    # Rensa bort rader där ALLA värden saknas
    prices.dropna(how="all", inplace=True)

    print(f"Hämtade {len(prices)} handelsdagar, {prices.shape[1]} aktier.")
    print(f"Saknade datapunkter per aktie:\n{prices.isna().sum()}\n")

    return prices


def save_prices(prices: pd.DataFrame, filename: str = "prices.csv") -> Path:
    """
    Sparar kursdatan som en CSV-fil i data-mappen.

    Vi sparar lokalt så att vi inte behöver ladda ner från Yahoo Finance
    varje gång vi kör analysen. Det gör utvecklingsloopen snabbare
    och minskar risken att API-anrop misslyckas mitt i arbetet.
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    filepath = DATA_DIR / filename
    prices.to_csv(filepath)
    print(f"Sparade kursdata till {filepath}")
    return filepath


def load_prices(filename: str = "prices.csv") -> pd.DataFrame:
    """
    Laddar tidigare sparad kursdata från CSV.
    """
    filepath = DATA_DIR / filename
    prices = pd.read_csv(filepath, index_col=0, parse_dates=True)
    print(f"Laddade {len(prices)} rader från {filepath}")
    return prices


# ---------------------------------------------------------------------------
# Kör modulen direkt för att testa
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    prices = fetch_prices()
    save_prices(prices)

    # Snabbkontroll: skriv ut de fem första raderna
    print("\nFörsta 5 raderna:")
    print(prices.head())

    print("\nSista 5 raderna:")
    print(prices.tail())