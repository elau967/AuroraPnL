# Aurora PnL - A Stock Profit and Loss Calculator App

## Calculates the Profit and Loss (PnL) of individual stocks and showcases the total PnL across different platforms and accounts

This project's goal is to make the calculating of PnL across different brokerages (Robinhood, IBKR, Schwab, etc.) and account types (Standard, Roth IRA, Traditional IRA, etc.) much easier without having to log in to a service or share sensitive data. A CSV file will be read, which will provide the data for the calculating and showcasing of PnL. Although filling out a CSV file may be tedious, Aurora provides an alternative to logging into multiple accounts and having to import information. After filling out the CSV file, seeing the PnL will eventually just be a matter of a few clicks.

## Access the live app:
https://aurorapnl.streamlit.app/

## How to replicate this project:

### Prerequisites:
1. Python 3.11+
2. (OPTIONAL) Install uv by Astral: https://docs.astral.sh/uv/getting-started/installation/

### Set up:
1. Install and learn about Git if you haven't already: https://www.youtube.com/watch?v=hrTQipWp6co
2. Clone this project using "git clone https://github.com/elau967/AuroraPnL" or through VS Code's source control: https://youtu.be/i_23KUAEtUM?si=mEwXZ_-V_nAQnwGt&t=343
3. (OPTIONAL) Set up a virtual environment (follow uv docs if you installed uv): https://www.youtube.com/watch?v=GZbeL5AcTgw
4. Install all dependencies from pyproject.toml using "pip install dependency_name" or "uv add dependency_name" if you installed uv.
5. To run locally, enter in your terminal "streamlit run main.py" 
6. Learn more about streamlit here: https://docs.streamlit.io/get-started