import pandas as pd
import streamlit as st
import yfinance as yf
from streamlit_option_menu import option_menu

# Allow the user to enter data and save as a CSV file
def create_and_edit_csv():
    # Create an empty dataframe
    emptyFrame = pd.DataFrame(columns = ["Ticker Symbol", "Cost Basis", "Amount of Shares"])

    # Allow user to input data into dataframe and validate it
    st.data_editor(emptyFrame, width = 1080, hide_index = True, num_rows = "dynamic", column_config = {
        "Ticker Symbol": st.column_config.TextColumn(
            help = "Enter a ticker symbol such as AAPL", 
            required = True,
            max_chars = 5,
            validate = r"^[a-zA-Z]+$"),
        "Cost Basis": st.column_config.NumberColumn(
            help = "Enter the average price paid per share such as 98.21", 
            required = True, 
            min_value = 0.01,
            format = "%.2f"),
        "Amount of Shares": st.column_config.NumberColumn(
            help = "Enter the amount of shares you own such as 100", 
            required = True,
            min_value = 0.01)
        })

# Receive a CSV file and calculate and display data
def upload_csv():
    # Prompt a user to upload a CSV file
    uploadedFile = st.file_uploader("Upload your CSV file", type = "csv", label_visibility = "collapsed")

    # If a CSV file is received, read it and assign data types
    if uploadedFile:
        df = pd.read_csv(uploadedFile, dtype = {"Ticker Symbol": str, "Cost Basis": float, "Amount of Shares": float})

        # Get rid of whitespace
        df.columns = df.columns.str.strip()
        df["Ticker Symbol"] = df["Ticker Symbol"].str.replace(" ", "").str.upper()

        # Make a "Total Cost" column
        df["Total Cost"] = df["Cost Basis"] * df["Amount of Shares"]

        # Combine duplicate ticker symbols, sum columns, and calculate new cost basis
        df = df.groupby("Ticker Symbol").agg({
            "Total Cost": "sum",
            "Amount of Shares": "sum"
        }).reset_index()
        df["Cost Basis"] = df["Total Cost"] / df["Amount of Shares"]

        # Display and return the dataframe
        st.dataframe(df.style.format({
            "Cost Basis": "${:,.2f}",
            "Total Cost": "${:,.2f}",
            "Amount of Shares": "{:,.4f}"
        }), width = 1080, hide_index = True)
        return df

# Create a sidebar
def sidebar():
    with st.sidebar:
        selected = option_menu(
            menu_title = None, 
            options = ["Home", "Download", "Upload", "Contact"],
            icons = ["cast", "cloud-download", "cloud-upload", "person-badge"],
            default_index = 0
        )
        return selected

def main():
    selected = sidebar()

    if selected == "Home":
        st.header("Aurora PnL", divider = "blue", anchor = False)
    elif selected == "Download":
        st.header("Insert and download your data as a CSV file", divider = "blue", anchor = False)
        create_and_edit_csv()
    elif selected == "Upload":
        st.header("Upload and display your data", divider = "blue", anchor = False)
        df = upload_csv()
    elif selected == "Contact":
        st.header("TODO", divider = "blue", anchor = False)

if __name__ == "__main__":
    main()