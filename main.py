import pandas as pd
import streamlit as st
import yfinance as yf

# Prompt a user to upload a CSV file
def upload_csv():
    uploadedFile = st.file_uploader("Upload your CSV file", type = "csv")

    # If a CSV file is received, read it and make a "Total Value" column
    if uploadedFile:
        df = pd.read_csv(uploadedFile, dtype = {"Ticker Symbol": str, "Cost Basis": float, "Amount of Shares": float})
        df["Total Value"] = df["Cost Basis"] * df["Amount of Shares"]

        # Combine duplicate ticker symbols, sum columns, and calculate new cost basis
        df = df.groupby("Ticker Symbol").agg({
            "Total Value": "sum",
            "Amount of Shares": "sum"
        }).reset_index()
        df["Cost Basis"] = df["Total Value"] / df["Amount of Shares"]

        # Display and return the dataframe
        st.write(df)
        return df

def main():
    st.write("Aurora PnL")
    df = upload_csv()

if __name__ == "__main__":
    main()