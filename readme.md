### What is this?
https://braucastelblanco-cryptowallet-cryptowallet-h28zlv.streamlit.app/
The  main goal of this project is to create an easy way to visualize my cryptoportfolio on [cryptomkt](https://www.cryptomkt.com/en/) exchange. Likewise, it provides a tool to see the stock prices of the coins in your portfolio for the last year.

*Disclaimer* This project has no relation or partnership with the company cryptomkt.com, it justs happens to be where I have my wallets.
### How does it work?
First, the information is extracted through the cryptomkt api (see documentation here: https://api.exchange.cryptomkt.com/), the extraction code is available in this repository as cryptomktETL.ipynb.
The API gets two different datasets from two different endpoints: 
- GET /api/3/public/price/history : Returns quotation prices history.
- GET /api/3/wallet/balance : Returns the user's wallet balances except zero balances

After the extraction process,I created the visualization tool you are looking at, the code is also available on github as cryptowallet.py

The main libraries used are: [pandas](https://pandas.pydata.org/), [plotly](https://plotly.com/), [streamlit](https://streamlit.io/), among others.
### Sample Data 
It should be noted that I removed my Apy Keys from the cryptomkt_api.ipynb code, so for it to works you must enter your information in the corresponding functions.

For the visualization tool to work, 3 csv files are available on this repository. I could have connected the api directly to streamlit, but it is not part of the scope of this project and I don't want to leave my accounts connected to a public platform.
Please feel free to reach me at braulioacc@gmail.com
