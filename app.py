

from flask import Flask
import asyncio
import requests
from flask_cors import CORS
import pandas as pd
import aiohttp
from flask import Flask, render_template, request, jsonify
from api_master.cfg import YOUR_API_KEY
from api_master.examples.webull_webull_data import Webull
from api_master.sdks.webull_sdk.webull_sdk import AsyncWebullSDK
from api_master.sdks.polygon_sdk.masterSDK import MasterSDK
from api_master.sdks.polygon_sdk.async_polygon_sdk import AsyncPolygonSDK
from static.py.api_functions import get_top_gainers_data, volume_analysis_endpoint, financial_statement_endpoint,balance_sheet_endpoint, cash_flow_endpoint, balance_sheet_endpoint
from static.py.api_functions import financial_ratios_endpoint, capital_flow_endpoint, process_data, institutional_holdings_endpoint,short_interest_endpoint
from static.py.api_functions import analyst_ratings_endpoint, stock_data_endpoint,get_top_gainers_data, earnings_calendar_endpoint, get_fifty_twos_endpoint

import asyncio
poly = AsyncPolygonSDK(YOUR_API_KEY)
webull = AsyncWebullSDK()
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
app = Flask(__name__)
CORS(app)
master = MasterSDK()
@app.route('/')
async def index():
    return render_template('index.html')


@app.route('/api/volume_analysis/<string:ticker>', methods=['GET', 'POST'])
async def volume_analysis(ticker):
    return await volume_analysis_endpoint(ticker)

@app.route('/ball', methods=['GET', 'POST'])
async def ball():
    return render_template('bouncy_ball.html')


@app.route('/skew', methods=['GET', 'POST'])
async def skew():
     
     table = await master.tabulate_options()  # assuming this function now returns current prices too
     return render_template('skew.html', table=table.to_html(index=False, classes='table table-striped'))


@app.route('/fudstop', methods=['GET','POST','PUT'])
async def fudstop():
    
    return render_template('fudstop.html')


@app.route('/ticker_cards')
def ticker_cards():
    return render_template('ticker_cards.html')
@app.route('/api/top_gainers', methods=['GET'])
async def get_top_gainers_endpoint():
    return await get_top_gainers_data()






@app.route('/api/fifty_twos', methods=['GET', 'POST'])
async def get_fifty_twos_endpoint():
    fifty_twos = await webull.fifty_two_high_and_lows()
    return fifty_twos

   

@app.route("/snippets", methods=['GET'])
def snippets():
    return render_template('snippets.html')


@app.route("/commands", methods=['GET', 'POST'])
def discord_commands():
    return render_template('discord_commands.html')

@app.route('/api/financial_statement/<string:ticker>', methods=['GET', 'POST'])
async def financial_statement(ticker):
    data = await financial_statement_endpoint(ticker=ticker)
    return data


@app.route('/api/earnings_calendar', methods=['GET', 'POST'])
async def earnings():
    data = await earnings_calendar_endpoint()
    return data

@app.route('/test', methods=['GET', 'POST'])
async def test():

    return render_template('test_template.html')

@app.route('/api/stock_data/<string:ticker>', methods=['GET', 'POST'])
async def stock_data(ticker):
    data = await stock_data_endpoint(ticker=ticker)
    return data


@app.route('/api/institutional_holdings/<string:ticker>', methods=['GET', 'POST'])
async def institutional_holdings(ticker):
    data = await institutional_holdings_endpoint(ticker=ticker)
    return data


@app.route('/api/analyst_ratings/<string:ticker>', methods=['GET', 'POST'])
async def analyst_ratings(ticker):
    data = await analyst_ratings_endpoint(ticker)
    return data


@app.route('/api/short_interest/<string:ticker>', methods=['GET', 'POST'])
async def short_interest(ticker):
    data = await short_interest_endpoint(ticker=ticker)
    return data


@app.route('/api/cash_flow/<string:ticker>', methods=['GET', 'POST'])
async def cash_flow(ticker):

    return await cash_flow_endpoint(ticker=ticker)


@app.route('/api/balance_sheet/<string:ticker>', methods=['GET', 'POST'])
async def balance_sheet(ticker):
    

    return await balance_sheet_endpoint(ticker)



@app.route('/api/financial_ratios/<string:ticker>', methods=['GET', 'POST'])
async def get_financial_ratios(ticker):

    return await(financial_ratios_endpoint(ticker=ticker))

@app.route('/api/capital_flow/<string:ticker>', methods=['GET', 'POST'])
async def get_capital_flow(ticker):
    

    return await(capital_flow_endpoint(ticker))





@app.route('/api/fetch_data', methods=['GET', 'POST'])
async def fetch_data():
    result = await process_data()
    return jsonify(result)


@app.route('/api/home', methods=['GET'])
def apihome():
    ticker = request.args.get('ticker', '')  # Get the ticker from the query string
    return render_template('api_home.html', ticker=ticker)






@app.route("/signals", methods=['GET'])
def home():
    return render_template('technical_signals.html')




@app.route("/api/stock-data/<string:ticker>", methods=['GET', 'POST'])
async def api_stock_data():
    ticker = ''
    data = await Webull(ticker=ticker).process_data(ticker)
    return jsonify(data)



@app.route('/api_master/home')
def apimaster():
    return render_template('api_master.html')

if __name__ == '__main__':
    import asyncio

    loop = asyncio.get_event_loop()
    app.run(debug=True, use_reloader=False)
    loop.close()