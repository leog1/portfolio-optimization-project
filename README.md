# portfolio-optimization-project
Quantitative portfolio analysis and Markowitz mean-variance optimization

# Portfolio Optimization – Stockholm Stock Exchange

A Python-based portfolio optimization tool applying **Markowitz mean-variance analysis** to stocks listed on Nasdaq Stockholm (OMXS30).

> 🚧 **Work in progress** — this project is being built as part of a quantitative finance learning journey.

## Features (planned)

- [x] Fetch historical price data via Yahoo Finance
- [ ] Compute returns, volatility, correlation, and Sharpe ratios
- [ ] Mean-variance optimization (efficient frontier)
- [ ] Backtest optimized portfolio vs. OMXS30 index
- [ ] Discussion of limitations (overfitting, estimation error, etc.)

## Project Structure

```
src/
  data_loader.py   – Data fetching and storage
  analysis.py      – Return & risk calculations
  optimizer.py     – Markowitz optimization
  backtest.py      – Portfolio backtesting
  visualize.py     – Plotting functions
main.py            – Entry point
data/              – Cached CSV files
```

## Quickstart

```bash
pip install -r requirements.txt
python main.py
```

## Tech Stack

Python 3.13 · pandas · NumPy · SciPy · matplotlib · yfinance

## License

MIT