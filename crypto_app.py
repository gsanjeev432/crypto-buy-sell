# Data Source
import yfinance as yf
# Data viz
import plotly.graph_objs as go
import streamlit as st

st.title("Crypto App Buy and Sell Decision")
crypto_mapping = {"DOGE": "DOGE-INR", "ETHEREUM": "ETH-INR", "BITCOIN": "BTC-INR", "KUSAMA": "KSM-INR", "BINANCE": "BNB-INR", "LITECOIN": "LTC-INR", "FILECOIN": "FIL-INR",
                  "SOLANA": "SOL1-INR", "BITTORRENT": "BTT1-INR", "TRON": "TRX-INR", "RIPPLE": "XRP-INR", "VECHAIN": "VET-INR", "MATIC": "MATIC-INR", "CARDANO": "ADA-INR", "EOS": "EOS-INR"}

crypto_list = [None, "DOGE", "ETHEREUM", "BITCOIN", "KUSAMA", "BINANCE", "LITECOIN", "FILECOIN",
               "SOLANA", "BITTORRENT", "TRON", "RIPPLE", "VECHAIN", "MATIC", "CARDANO", "EOS"]
selected_crypto = st.selectbox('Select Crypto', crypto_list)

if selected_crypto:
    crypto = crypto_mapping[selected_crypto]
    # Importing market data
    data = yf.download(tickers=crypto, period='8d', interval='90m')

    # Adding Moving average calculated field
    data['MA5'] = data['Close'].rolling(5).mean()
    data['MA20'] = data['Close'].rolling(20).mean()

    # declare figure
    fig = go.Figure()

    # Candlestick
    fig.add_trace(go.Candlestick(x=data.index,
                                 open=data['Open'],
                                 high=data['High'],
                                 low=data['Low'],
                                 close=data['Close'], name='market data'))

    # Add Moving average on the graph
    fig.add_trace(go.Scatter(x=data.index, y=data['MA20'], line=dict(
        color='blue', width=1.5), name='Long Term MA'))
    fig.add_trace(go.Scatter(x=data.index, y=data['MA5'], line=dict(
        color='orange', width=1.5), name='Short Term MA'))

    # Updating X axis and graph
    # X-Axes
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=3, label="3d", step="day", stepmode="backward"),
                dict(count=5, label="5d", step="day", stepmode="backward"),
                dict(count=7, label="WTD", step="day", stepmode="todate"),
                dict(step="all")
            ])
        )
    )
    fig.update_layout(
        title={
            'text': crypto,
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    # Show
    # fig.show()
    st.plotly_chart(fig)
