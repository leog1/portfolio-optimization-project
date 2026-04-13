"""
main.py – Huvudskript för portföljoptimeringsprojektet.

Knyter ihop alla moduler och kör den kompletta analysen.
Byggs ut successivt genom fas 1–3.
"""

from src.data_loader import fetch_prices, save_prices, load_prices


def main():
    """Kör den kompletta analyskedjan."""

    # ------------------------------------------------------------------
    # Steg 1: Hämta kursdata
    # ------------------------------------------------------------------
    prices = fetch_prices()
    save_prices(prices)

    print("\n✅ Fas 1a klar – kursdata hämtad och sparad.")
    print("Nästa steg: beräkna daglig avkastning i analysis.py\n")


if __name__ == "__main__":
    main()