import pandas as pd
import streamlit as st
import yfinance as yf
import numpy as np
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

# Allow the user to enter data and save as a CSV file
def create_and_edit_csv():
    answer = st.selectbox("Would you like to create a new file or edit a previously downloaded file?", ["Create", "Edit"])
    expectedColumns = ["Ticker Symbol", "Cost Basis", "Amount of Shares"]

    if answer == "Create":
        # Create an empty dataframe
        emptyFrame = pd.DataFrame(columns = expectedColumns)

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
    else:
        # Prompt a user to upload a CSV file
        uploadedFile = st.file_uploader("Upload your CSV file", type = "csv", label_visibility = "collapsed")

        # If a CSV file is received, read it and replace the column headers and reformat "Ticker Symbol" values
        if uploadedFile:
            df = pd.read_csv(uploadedFile)
            df.columns = expectedColumns
            df["Ticker Symbol"] = df["Ticker Symbol"].str.replace(" ", "").str.upper()

            # Replace invalid values with NaN
            df["Ticker Symbol"] = df["Ticker Symbol"].apply(lambda x: x if x.isalpha() else np.nan)
            df["Cost Basis"] = pd.to_numeric(df["Cost Basis"], errors="coerce")
            df["Amount of Shares"] = pd.to_numeric(df["Amount of Shares"], errors="coerce")

            # Allow user to input/edit data and validate it
            st.data_editor(df, width = 1080, hide_index = True, num_rows = "dynamic", column_config = {
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

# Get the current price of a stock
def get_stock_price(df):
    currentPrices = []
    stocks = list(df["Ticker Symbol"])
     
    try:
        data = yf.download(stocks, period="1d", interval="1m", group_by="ticker")

        for stock in stocks:
            price = data[stock]["Close"].iloc[-1]
            currentPrices.append(round(price, 2))

        return currentPrices
   
    except IndexError:
        st.error(f'The ticker {stock} could not be found. Please go back and edit your file at the Download section.')

# Receive a CSV file and calculate and display data
def upload_csv():
    # Prompt a user to upload a CSV file
    uploadedFile = st.file_uploader("Upload your CSV file", type = "csv", label_visibility = "collapsed")

    # If a CSV file is received, read it and assign data types
    try:
        if uploadedFile:
            df = pd.read_csv(uploadedFile, dtype = {"Ticker Symbol": str, "Cost Basis": float, "Amount of Shares": float})

    # Catch invalid values in "Cost Basis" and "Amount of Shares" column
    except ValueError:
        st.error("The values of your file are incorrect. Please go back and edit your file at the Download section.")

    try:
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

        # Get current prices of stocks
        currentPrices = get_stock_price(df)

        # Calculate new columns
        df["Current Price"] = currentPrices
        df["Market Value"] = round((df["Current Price"] * df["Amount of Shares"]), 2)
        totalMktVal = round(sum(df["Market Value"]), 2)
        df["Portfolio Allocation"] = (df["Market Value"] / totalMktVal) * 100
        df["P&L"] = ((df["Current Price"] - df["Cost Basis"]) * df["Amount of Shares"])

        # Display the data
        display_data(df)

    # Catch invalid column headers
    except KeyError:
        st.error("The column headers of your file are incorrect. Please go back and edit your file at the Download section.")
        
    # Pass both because ValueError in upload_csv and IndexError in get_stock_price will cover
    except UnboundLocalError:
        pass
    except TypeError:
        pass

# Helper function that formats P&L column into US currency
def format_currency(value):
    if value > 0:
        return f"+${value:,.2f}"  
    elif value < 0:
        return f"-${abs(value):,.2f}"
    else:
        return f"${value:.2f}"

# Helper function that makes positive values green and negative red
def color_text(value):
    if value > 0:
        color = "green"  
    elif value < 0:
        color = "red"
    else:
        color = "gray"
    return f"color: {color};"

# Helper function for upload_csv that displays data
def display_data(df):
        # Display and return the dataframe
        st.dataframe(df.style.format({
            "Cost Basis": "${:,.2f}",
            "Total Cost": "${:,.2f}",
            "Amount of Shares": "{:,.4f}",
            "Current Price": "${:,.2f}",
            "Market Value": "${:,.2f}",
            "P&L": format_currency
        }).applymap(color_text, subset = ["P&L"]), width = 1080, hide_index = True, column_config = {"Portfolio Allocation": None})

        # Hide dataframe tools
        st.markdown(
                """
                <style>
                [data-testid="stElementToolbar"] {
                    display: none;
                }
                </style>
                """,
                unsafe_allow_html=True)
        
        # Create a pie chart
        fig = go.Figure(data=[go.Pie(labels = df["Ticker Symbol"], values = df["Market Value"], textinfo = "label + percent",
                        insidetextorientation = "horizontal",
                        hovertemplate = "Ticker: %{label} | Market Value: $%{value:,.2f}<extra></extra>")])
        
        # Change size of chart
        fig.update_layout(
            width = 750,
            height = 750
        )

        # Display chart
        st.plotly_chart(fig)

# Display contact information
def display_contact_info():
    contact_css = """<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.13.1/font/bootstrap-icons.min.css">
                        <p style="font-size: 32px;">
                            <i class="bi bi-github" style="font-size: 2rem; margin-right: 10px;"></i>
                            <a href="https://github.com/elau967">elau967</a>
                        </p>
                        <p style="font-size: 32px;">
                            <i class="bi bi-linkedin" style="color: #0A66C2; font-size: 2rem; margin-right: 10px;"></i>
                            <a href="https://www.linkedin.com/in/elau967">elau967</a>
                        </p>
                        <p style="color: black; font-size: 32px;">
                            <i class="bi bi-envelope" style="font-size: 2rem; margin-right: 10px"></i> 
                            <a href="mailto:elau967@gmail.com">elau967@gmail.com</a>
                        </p>"""
    return st.markdown(contact_css, unsafe_allow_html=True)

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
        upload_csv()
    elif selected == "Contact":
        st.header("Contact Me", divider = "blue", anchor = False)
        display_contact_info()
    
if __name__ == "__main__":
    main()