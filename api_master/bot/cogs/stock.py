import disnake
import datetime
from disnake.ext import commands
import requests
from views.learnviews import LeverageDropdown
from autocomp import ticker_autocomp
import stocksera
from sdks.polygon_sdk.async_polygon_sdk import AsyncPolygonSDK
from cfg import YOUR_STOCKSERA_KEY, YOUR_NASDAQ_KEY, YOUR_FINNHUB_KEY, YOUR_IEX_CLOUD_KEY, YOUR_API_KEY
from autocomp import tickerlist_autocomp, ticker_autocomp
from utils.webull_tickers import ticker_list
from time import sleep
from datetime import timedelta
import finnhub
import pyEX as p

from datetime import date
import pandas as pd
intents = disnake.Intents.all()
bot = commands.Bot( command_prefix="!", intents=intents)
client = stocksera.Client(api_key=YOUR_STOCKSERA_KEY)
finnhub_client = finnhub.Client(api_key=f"{YOUR_FINNHUB_KEY}")
poly = AsyncPolygonSDK(YOUR_API_KEY)
class Stock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.slash_command()
    async def stock(self, inter):
        """Stock slash commands category."""
        pass
 

    @stock.sub_command()
    async def ipos(inter:disnake.AppCmdInter):
        """📊View the IPO Calendar!"""
        await inter.response.defer(with_message=True)
        r = client.ipo_calendar()
        date = [i['Date'] for i in r][:20]
        symbol = [i['Symbol'] for i in r][:20]
        name = [i['Name'] for i in r][:20]
        price = [i['Expected Price'] for i in r][:20]
        shares = [i['Number Shares'] for i in r][:20]
        mktcap = float(round([i['Mkt Cap'] for i in r][:20]) * 0.000001,ndigits=2)
        status = [i['Status'] for i in r][:20]
        exchange = [i['Exchange'] for i in r][:20]
        items = "\n".join(f"{i['Date']} {i['Symbol']} {i['Name']} {i['Expected Price']} {i['Number Shares']} {i['Mkt Cap']} {i['Status']} {i['Exchange']}" for i in r)
        list1 = [date, symbol, price, shares, mktcap, status]
        data = pd.DataFrame(list1)
        data.columns = ['Date', 'Sym',
                        'Price',
                        'Shares', 'Mkt Cap',
                        'Status']
        em = disnake.Embed(title="IPO Calendar", description=f"```py\n{data}```", color=disnake.Colour.dark_orange())
        await inter.edit_original_message(embed=em)

    @stock.sub_command()
    async def orderflow(inter:disnake.AppCmdInter, ticker: str=commands.Param(autocomp=tickerlist_autocomp)):
        """📊Returns order-flow data straight from the SIP Feed"""
        counter = 0
        await inter.response.defer(with_message=True, ephemeral=False)
        while True:
            counter = counter + 1
            ids = ticker_list[ticker.upper()]
            r1 = requests.get(f"https://quotes-gw.webullfintech.com/api/stock/capitalflow/stat?count=10&tickerId={ids}&type=0")
            d1 = r1.json()
            r2 = requests.get(f"https://quotes-gw.webullfintech.com/api/stock/capitalflow/stat?count=10&tickerId={ids}&type=1")
            d2 = r2.json()
            r3 = requests.get(f"https://quotes-gw.webullfintech.com/api/stock/capitalflow/stat?count=10&tickerId={ids}&type=2")
            d3 = r3.json()
            r4 = requests.get(f"https://quotes-gw.webullfintech.com/api/stock/capitalflow/stat?count=10&tickerId={ids}&type=3")
            d4 = r4.json()
            r5 = requests.get(f"https://quotes-gw.webullfintech.com/api/stock/capitalflow/stat?count=10&tickerId={ids}&type=4")
            d5 = r5.json()

            dateset = d1['dates']
            datelist = [i['date'] for i in dateset]

            date1 = datelist[0]
            sellvol1 = round(float(d1['sellVolume']) * 0.000001, ndigits=2)
            nvol1 = round(float(d1['nVolume']) * 0.000001, ndigits=2)
            buyvol1 = round(float(d1['buyVolume']) * 0.000001, ndigits=2)
            avg1 = d1['avePrice']
            max1 = round(float(d1['maxT']) * 0.000001, ndigits=2)

            date2 = datelist[1]
            sellvol2 = round(float(d2['sellVolume']) * 0.000001, ndigits=2)
            nvol2 = round(float(d2['nVolume']) * 0.000001, ndigits=2)
            buyvol2 = round(float(d2['buyVolume']) * 0.000001, ndigits=2)
            avg2 = d2['avePrice']
            max2 = round(float(d2['maxT']) * 0.000001, ndigits=2)

            date3 = datelist[2]
            sellvol3 = round(float(d3['sellVolume']) * 0.000001, ndigits=2)
            nvol3 = round(float(d3['nVolume']) * 0.000001, ndigits=2)
            buyvol3 = round(float(d3['buyVolume']) * 0.000001, ndigits=2)
            max3 = round(float(d3['maxT']) * 0.000001, ndigits=2)
            avg3 = d3['avePrice']

            date4 = datelist[3]
            sellvol4 = round(float(d4['sellVolume']) * 0.000001, ndigits=2)
            nvol4 = round(float(d4['nVolume']) * 0.000001, ndigits=2)
            buyvol4 = round(float(d4['buyVolume']) * 0.000001, ndigits=2)
            max4 = round(float(d4['maxT']) * 0.000001, ndigits=2)
            avg4 = d4['avePrice']

            date5 = datelist[4]
            sellvol5 = round(float(d5['sellVolume']) * 0.000001, ndigits=2)
            nvol5 = round(float(d5['nVolume']) * 0.000001, ndigits=2)
            buyvol5 = round(float(d5['buyVolume']) * 0.000001, ndigits=2)
            max5 = round(float(d5['maxT']) * 0.000001, ndigits=2)
            avg5 = d5['avePrice']

            view = disnake.ui.View()
            b1 = disnake.ui.Button(style=disnake.ButtonStyle.green, label=f"🟢Buy Volume: {buyvol1} million.",row=0)
            s1 = disnake.ui.Button(style=disnake.ButtonStyle.grey, label=f"⚪Neutral: {nvol1} million.",row=0)
            n1 = disnake.ui.Button(style=disnake.ButtonStyle.red, label=f"🔴Sell Volume: {sellvol1} million.",row=0)
            t1 = disnake.ui.Button(style=disnake.ButtonStyle.blurple, label=f"🎯Avg Price: ${avg1}",row=0)
            m1 = disnake.ui.Button(style=disnake.ButtonStyle.blurple, label=f"DATE: {date1}",row=0)
            b2 = disnake.ui.Button(style=disnake.ButtonStyle.green, label=f"🟢Buy Volume: {buyvol2} million.",row=1)
            s2 = disnake.ui.Button(style=disnake.ButtonStyle.grey, label=f"⚪Neutral: {nvol2} million.",row=1)
            n2 = disnake.ui.Button(style=disnake.ButtonStyle.red, label=f"🔴Sell Volume: {sellvol2} million.",row=1)
            t2 = disnake.ui.Button(style=disnake.ButtonStyle.blurple, label=f"🎯Avg Price: ${avg2}",row=1)
            m2 = disnake.ui.Button(style=disnake.ButtonStyle.blurple, label=f"DATE: {date2}",row=1)

            b3 = disnake.ui.Button(style=disnake.ButtonStyle.green, label=f"🟢Buy Volume: {buyvol3} million.",row=2)
            s3 = disnake.ui.Button(style=disnake.ButtonStyle.grey, label=f"⚪Neutral: {nvol3} million.",row=2)
            n3 = disnake.ui.Button(style=disnake.ButtonStyle.red, label=f"🔴Sell Volume: {sellvol3} million.",row=2)
            t3 = disnake.ui.Button(style=disnake.ButtonStyle.blurple, label=f"🎯Avg Price: ${avg3}",row=2)
            m3 = disnake.ui.Button(style=disnake.ButtonStyle.blurple, label=f"DATE: {date3}",row=2)

            b4 = disnake.ui.Button(style=disnake.ButtonStyle.green, label=f"🟢Buy Volume: {buyvol4} million.",row=3)
            s4 = disnake.ui.Button(style=disnake.ButtonStyle.grey, label=f"⚪Neutral: {nvol4} million.",row=3)
            n4 = disnake.ui.Button(style=disnake.ButtonStyle.red, label=f"🔴Sell Volume: {sellvol4} million.",row=3)
            t4 = disnake.ui.Button(style=disnake.ButtonStyle.blurple, label=f"🎯Avg Price: ${avg4}",row=3)
            m4 = disnake.ui.Button(style=disnake.ButtonStyle.blurple, label=f"DATE: {date4}",row=3)

            b5 = disnake.ui.Button(style=disnake.ButtonStyle.green, label=f"🟢Buy Volume: {buyvol5} million.",row=4)
            s5 = disnake.ui.Button(style=disnake.ButtonStyle.grey, label=f"⚪Neutral: {nvol5} million.",row=4)
            n5 = disnake.ui.Button(style=disnake.ButtonStyle.red, label=f"🔴Sell Volume: {sellvol5} million.",row=4)
            t5 = disnake.ui.Button(style=disnake.ButtonStyle.blurple, label=f"🎯Avg Price: ${avg5}",row=4)
            m5 = disnake.ui.Button(style=disnake.ButtonStyle.blurple, label=f"DATE: {date5}",row=4)

            em = disnake.Embed(title=f"Order Flow for {ticker} - Last 5 days.", description=f"```py\nDate: {date1} | 🎯AVG PRICE: {avg1}```",color=disnake.Colour.random())
            em.add_field(name="Buy Volume: ",value=f"```py\n🟩{buyvol1} million```")
            em.add_field(name="Neutral Volume: ", value=f"```py\n⬜{nvol1} million```")
            em.add_field(name="Sell Volume:", value=f"```py\n🟥Sell: {sellvol1} million```")
            await inter.edit_original_message(embed=em, view=view)
            if counter == 150:
                await inter.edit_original_message("Live session ended.", embed=em)
                break


    @stock.sub_command()
    async def shortinterest(inter: disnake.AppCmdInter, ticker: str=commands.Param(autocomplete=tickerlist_autocomp)):
        """📊Pulls short interest data straight from Webull."""
        ids = ticker_list[ticker.upper()]
        await inter.response.defer(with_message=True)
        r = requests.get(url=f"https://securitiesapi.webullfintech.com/api/securities/stock/{ids}/shortInterest")
        data = r.json()
        results = data[0]
        setdate = results['settlementDate']
        shortint = results['shortInterst']
        f = float(shortint)
        avgvol = results['avgDailyShareVolume']
        f2 = float(avgvol)
        averagevol = round(f2*0.000001, ndigits=2)
        shortinterst = round(f*0.000001, ndigits=2)
        dtc = results['daysToCover']
        em = disnake.Embed(title=f"Short Interest for {ticker}", description=f"```py\n Settlement Date: {setdate}``` ```py\n Short Interest: {shortinterst} million shares``` ```py\nAverage Volume: {averagevol} million. \n\n Days to Cover: {dtc}```", color=disnake.Colour.dark_red())
        em.set_footer(text="FUDSTOP Trading")
        await inter.edit_original_message(embed=em)
        await inter.send(f"To run this command, click --> </stock shortinterest:1122243463862300760>")
    @shortinterest.error
    async def shortinterror(inter: disnake.AppCmdInter, error):
        if isinstance(error, commands.CheckAnyFailure):
            await inter.send("```py\n No Short Interest Data Found```")

    @stock.sub_command()
    async def institutions(inter: disnake.AppCmdInter, ticker: str=commands.Param(autocomplete=tickerlist_autocomp)):
        """📊Pulls ownership data straight from Webull."""
        ids = ticker_list[ticker.upper()]
        await inter.response.defer(with_message=True)
        r = requests.get(url=f"https://securitiesapi.webullfintech.com/api/securities/stock/{ids}/holdersDetail?tickerId={ids}&type=2&hasNum=0&pageSize=10")
        d = r.json()
        company1 = d[0]
        name1 = company1['ownerName']
        date1 = company1['date']
        shares1 = company1['sharedHeld']
        f1 = float(shares1)
        holdings1 = round(f1*0.000001, ndigits=2)
        change1 = company1['shareChange']
        ratio1 = company1['changeRatio']
        type1 = company1['type']
        holdingratio1 = company1['holdingRatio']



        company2=d[1]
        name2 = company2['ownerName']
        date2 = company2['date']
        shares2 = company2['sharedHeld']
        f2 = float(shares2)
        holdings2 = round(f2*0.000001, ndigits=2)
        change2 = company2['shareChange']
        ratio2 = company2['changeRatio']
        type2 = company2['type']
        holdingratio2 = company2['holdingRatio']



        company3=d[2]
        name3 = company3['ownerName']
        date3 = company3['date']
        shares3 = company3['sharedHeld']
        f3 = float(shares3)
        holdings3 = round(f3*0.000001, ndigits=2)
        change3 = company3['shareChange']
        ratio3 = company3['changeRatio']
        type3 = company3['type']
        holdingratio3 = company3['holdingRatio']

        company4=d[3]
        name4 = company4['ownerName']
        date4 = company4['date']
        shares4 = company4['sharedHeld']
        f4 = float(shares4)
        holdings4 = round(f4*0.000001, ndigits=2)
        change4 = company4['shareChange']
        ratio4 = company4['changeRatio']
        type4 = company4['type']
        holdingratio4 = company4['holdingRatio']

        company5=d[4]
        name5 = company5['ownerName']
        date5 = company5['date']
        shares5 = company5['sharedHeld']
        f5 = float(shares5)
        holdings5 = round(f5*0.000001, ndigits=2)
        change5 = company5['shareChange']
        ratio5 = company5['changeRatio']
        type5 = company5['type']
        holdingratio5 = company5['holdingRatio']

        company6=d[5]
        name6 = company6['ownerName']
        date6 = company6['date']
        shares6 = company6['sharedHeld']
        f6 = float(shares6)
        holdings6 = round(f6*0.000001, ndigits=2)
        change6 = company6['shareChange']
        ratio6 = company6['changeRatio']
        type6 = company6['type']
        holdingratio6 = company6['holdingRatio']

        company7=d[6]
        name7 = company7['ownerName']
        date7 = company7['date']
        shares7 = company7['sharedHeld']
        f7 = float(shares7)
        holdings7 = round(f7*0.000001, ndigits=2)
        change7 = company7['shareChange']
        ratio7 = company7['changeRatio']
        type7 = company7['type']
        holdingratio7 = company7['holdingRatio']

        company8=d[7]
        name8 = company8['ownerName']
        date8 = company8['date']
        shares8 = company8['sharedHeld']
        f8 = float(shares8)
        holdings8 = round(f8*0.000001, ndigits=2)
        change8 = company8['shareChange']
        ratio8 = company8['changeRatio']
        type8 = company8['type']
        holdingratio8 = company8['holdingRatio']

        company9=d[8]
        name9 = company9['ownerName']
        date9 = company9['date']
        shares9 = company9['sharedHeld']
        f9 = float(shares9)
        holdings9 = round(f9*0.000001, ndigits=2)
        change9 = company9['shareChange']
        ratio9 = company9['changeRatio']
        type9 = company9['type']
        holdingratio9 = company9['holdingRatio']

        company10=d[9]
        name10 = company10['ownerName']
        date10 = company10['date']
        shares10 = company10['sharedHeld']
        f10 = float(shares10)
        holdings10 = round(f10*0.000001, ndigits=2)
        change10 = company10['shareChange']
        ratio10 = company10['changeRatio']
        type10 = company10['type']
        holdingratio10 = company10['holdingRatio']
        em = disnake.Embed(title=f"Top 1 Institutional Ownership for {ticker}",description=f"```py\n{name1}\n{date1}\n\nHOLDINGS: {holdings1}million\nChange: {change1}\nChange Ratio: {ratio1}\nType: {type1}\nHolding Ratio: {holdingratio1}```", color=disnake.Colour.dark_gold())
        em.add_field(name=f"#2 {name2}\n{date2}", value=f"```py\nHOLDINGS: {holdings2}million\nChange: {change2}\nChange Ratio: {ratio2}\nType: {type2}\nHolding Ratio: {holdingratio2}```", inline=True)
        em.add_field(name=f"#3 {name3}\n{date3} ", value=f"```py\nHOLDINGS: {holdings3}million\nChange: {change3}\nChange Ratio: {ratio3}\nType: {type3}\nHolding Ratio: {holdingratio3}```", inline=True)
        em.add_field(name=f"#4 {name4}\n{date4}", value=f"```py\nHOLDINGS: {holdings4}million\nChange: {change4}\nChange Ratio: {ratio4}\nType: {type4}\nHolding Ratio: {holdingratio4}```", inline=True)
        em.add_field(name=f"#5 {name5}\n{date5}", value=f"```py\nHOLDINGS: {holdings5}million\nChange: {change5}\nChange Ratio: {ratio5}\nType: {type5}\nHolding Ratio: {holdingratio5}```", inline=True)
        em.add_field(name=f"#6 {name6}\n{date6}", value=f"```py\nHOLDINGS: {holdings6}million\nChange: {change6}\nChange Ratio: {ratio6}\nType: {type6}\nHolding Ratio: {holdingratio6}```", inline=True)
        em.add_field(name=f"#7 {name7}\n{date7}", value=f"```py\nHOLDINGS: {holdings7}million\nChange: {change7}\nChange Ratio: {ratio7}\nType: {type7}\nHolding Ratio: {holdingratio7}```", inline=True)
        em.add_field(name=f"#8 {name8}\n{date8}", value=f"```py\nHOLDINGS: {holdings8}million\nChange: {change8}\nChange Ratio: {ratio8}\nType: {type8}\nHolding Ratio: {holdingratio8}```", inline=True)
        em.add_field(name=f"#9 {name9}\n{date9}", value=f"```py\nHOLDINGS: {holdings9}million\nChange: {change9}\nChange Ratio: {ratio9}\nType: {type9}\nHolding Ratio: {holdingratio9}```", inline=True)
        em.add_field(name=f"#10 {name10}\n{date10}", value=f"```py\nHOLDINGS: {holdings10}million\nChange: {change10}\nChange Ratio: {ratio10}\nType: {type10}\nHolding Ratio: {holdingratio10}```", inline=True)

        await inter.edit_original_message(embed=em)
    @institutions.error
    async def instinterror(inter: disnake.AppCmdInter, error):
        if isinstance(error, commands.CheckAnyFailure):
            await inter.send("```py\n USE CAPS```")
    @stock.sub_command()
    async def capitalflow(inter:disnake.AppCmdInter, ticker:str=commands.Param(autocomplete=tickerlist_autocomp)):
        """📊Returns an overall picture of orderflow based on player size."""
        counter = 0
        await inter.response.defer(with_message=True)
        while True:
            counter = counter + 1
            ids = ticker_list[ticker.upper()]
            r = requests.get(url=f"https://quotes-gw.webullfintech.com/api/stock/capitalflow/ticker?tickerId={ids}&showHis=true")
            d = r.json()
            latest = d['latest']
            date = latest['date']
            item = latest['item']
            superlgin=round(float(item["superLargeInflow"]*0.000001), ndigits=2)
            superlgout=round(float(item["superLargeOutflow"]*0.000001), ndigits=2)
            superlgnet=round(float(item["superLargeNetFlow"]*0.000001), ndigits=2)
            lgin = round(float(item["largeInflow"]*0.000001), ndigits=2)
            lgout =round(float(item["largeOutflow"]*0.000001), ndigits=2)
            lgnet = round(float(item["largeNetFlow"]*0.000001), ndigits=2)
            newlgin =round(float(item["newLargeInflow"]*0.000001), ndigits=2)
            newlgout = round(float(item["newLargeOutflow"]*0.000001), ndigits=2)
            newlgnet = round(float(item["newLargeNetFlow"]*0.000001), ndigits=2)
            medin = round(float(item["mediumInflow"]*0.000001), ndigits=2)
            medout = round(float(item["mediumOutflow"]*0.000001), ndigits=2)
            mednet = round(float(item["mediumNetFlow"]*0.000001), ndigits=2)
            smallin = round(float(item["smallInflow"]*0.000001), ndigits=2)
            smallout = round(float(item["smallOutflow"]*0.000001), ndigits=2)
            smallnet = round(float(item["smallNetFlow"]*0.000001), ndigits=2)
            majorin = round(float(item["majorInflow"]*0.000001), ndigits=2)
            majorout = round(float(item["majorOutflow"]*0.000001), ndigits=2)
            majornet = round(float(item["majorNetFlow"]*0.000001), ndigits=2)
            retailin = round(float(item["retailInflow"]*0.000001), ndigits=2)
            retailout = round(float(item["retailOutflow"]*0.000001), ndigits=2)
            retailinratio =round(float(item["retailInflowRatio"]*100), ndigits=2)
            retailoutratio = round(float(item["retailOutflowRatio"]*100), ndigits=2)
            newlginratio =round(float(item["newLargeInflowRatio"]*100), ndigits=2)
            newlgoutratio = round(float(item["newLargeOutflowRatio"]*100), ndigits=2)
            mediuminratio =round(float(item["mediumInflowRatio"]*100),ndigits=2)
            mediumoutratio = round(float(item["mediumOutflowRatio"]*100),ndigits=2)
            smallinratio =round(float(item["smallInflowRatio"]*100),ndigits=2)
            smalloutratio = round(float(item["smallOutflowRatio"]*100),ndigits=2)
            majorinratio =round(float(item["majorInflowRatio"]*100),ndigits=2)
            majoroutratio = round(float(item["majorOutflowRatio"]*100),ndigits=2)
            sleep(0.5)
            em = disnake.Embed(title=f"Order Flow - By Player Size for {ticker}", description=f"```py\nThis command returns orderflow for the following player types:\n 'Super Large' 'Major' 'Large' 'Medium' 'Small' 'Retail' and 'New'```", color=disnake.Colour.random())
            em.add_field(name="Super Large", value=f"```py\nInflow: {superlgin} million\n\nOutflow: {superlgout} million\n\nNetflow: {superlgnet} million```", inline=True)
            em.add_field(name="Retail", value=f"```py\nInflow: {retailin} million\n\nOutflow: {retailout} million```", inline=True)
            em.add_field(name="Large", value=f"```py\nInflow: {lgin} million\n\nOutflow: {lgout} million\n\nNetflow: {lgnet} million```", inline=True)
            em.add_field(name="Medium", value=f"```py\nInflow: {medin} million\n\nOutflow: {medout} million\n\nNetflow: {mednet} million```", inline=True)
            em.add_field(name="Small", value=f"```py\nInflow: {smallin} million\n\nOutflow: {smallout} million\n\nNetflow: {smallnet} million```", inline=True)
            em.add_field(name="Major", value=f"```py\nInflow: {majorin} million\n\nOutflow: {majorout} million\n\nNetFlow: {majornet} million```", inline=True)
            em.add_field(name="New", value=f"```py\nInflow: {newlgin} million\n\nOutflow: {newlgout} million\n\nNetflow: {newlgnet} million```", inline=True)
            em.add_field(name="Ratios", value=f"```py\nMedium Inflow %: {mediuminratio}\nMedium Outflow %: {mediumoutratio}``` ```py\nSmall Inflow %: {smallinratio}%\nSmall Outflow %: {smalloutratio}%``` ```py\nMajor Inflow %: {majorinratio}%\nMajor Outflow %: {majoroutratio}%``` ```py\nRetail Inflow %: {retailinratio}%\nRetail Outflow%: {retailoutratio}%``` ```py\nNew Large Inflow %: {newlginratio}%\nNew Large Outflow %: {newlgoutratio}%```", inline=True)
            view = disnake.ui.View()
            select = disnake.ui.Select(
                placeholder=f"🔎  🇷  🇪  🇸  🇺 🇱  🇹  🇸 for {ticker}🔍",
                min_values=1,
                max_values=1,
                custom_id=f"select_{str(disnake.Member)}",
                row=1,
                options = [
                disnake.SelectOption(label=f"New Large IN: {newlgin}", description=f"Retail OUT: {newlgout} | New Large Net: {newlgnet}"),
                disnake.SelectOption(label=f"Super Large IN: {superlgin}", description=f"Super Large OUT: {superlgout} Super LG Net: {superlgnet}"),
                disnake.SelectOption(label=f"Major IN: {majorin}", description=f"Super Large OUT: {majorout} | Major Net: {majornet}"),
                disnake.SelectOption(label=f"Large IN: {lgin}", description=f"Large OUT: {lgout} Net Large: {lgnet}"),
                disnake.SelectOption(label=f"Medium IN: {medin}", description=f"Medium OUT: {medout} | Medium Net: {mednet}"),
                disnake.SelectOption(label=f"Small IN: {smallin}", description=f"Small OUT: {smallout} | Net Small: {smallnet}"),
                disnake.SelectOption(label=f"Retail IN: {retailin}", description=f"Retail OUT: {retailout}"),
                disnake.SelectOption(label=f"Major Inflow Ratio: {majorinratio}%", description=f"Medium Outflow Ratio: {majoroutratio}%"),
                disnake.SelectOption(label=f"Small Inflow Ratio: {smallinratio}%", description=f"Small Outflow Ratio: {smalloutratio}%"),
                disnake.SelectOption(label=f"Medium Inflow Ratio: {mediuminratio}%", description=f"Medium Outflow Ratio: {mediumoutratio}%"),
                disnake.SelectOption(label=f"New Large Inflow Ratio: {newlginratio}%", description=f"New Large Outflow Ratio: {newlgoutratio}%"),
                disnake.SelectOption(label=f"Retail Inflow Ratio: {retailinratio}%", description=f"Retail Outflow Ratio: {retailoutratio}%"),])
            view.add_item(select)
            await inter.edit_original_message(embed=em, view =view)
            if counter == 50:
                break

    @capitalflow.error
    async def capitalflowerror(inter: disnake.AppCmdInter, error):
        if isinstance(error, commands.CheckAnyFailure):
            await inter.send("```py\n No capital flow data found```")

    @stock.sub_command()
    async def company_brief(inter:disnake.AppCmdInter, ticker: str=commands.Param(autocomplete = tickerlist_autocomp)):
        """📊Get detailed info for a ticker such as address, logo, description."""
        await inter.response.defer(with_message=True)
        ids = ticker_list[ticker.upper()]
        r = requests.get(url=f"https://quotes-gw.webullfintech.com/api/market/brief/queryCompanyBrief?tickerId={ids}")

        d = r.json()
        items = [i['items'] for i in d]
        title = [i['title'] for i in d]
        items1 = items[0]
        name = items1[0]['context']
        address = items1[1]['context']
        phone = items1[2]['context']
        fax = items1[3]['context']
        items2 = items[1]
        items3 = items[2]
        items4 = items[3]

        website = items4[0]['context']

        items5 = items[4]
        intro = items5[0]['context']


        industry = items2[0]['context']
        list_date = items3[0]['context']
        em = disnake.Embed(title=f"```py\nCompany Brief for: {ticker} | {name}", description=f"{intro}```", color=disnake.Colour.dark_gold())
        em.add_field(name="List Date & Industry", value=f"```py\nList Date:\n{list_date}  \n\n Industry:\n'{industry}'```", inline=True)
        em.add_field(name="Address & Website:", value=f"```py\nAddress: \n{address} \n\n Website:\n{website}```", inline=True)
        em.add_field(name="Phone & Fax #:", value=f"```py\nPhone:\n{phone}\n\n Fax:\n {fax}```", inline=True)

        em.set_footer( text="Data Provided by Webull / Cboe Hanweck")
        await inter.edit_original_message(embed=em)


   # @stock.sub_command()
    #async def logo(inter:disnake.AppCmdInter, symbol: str = commands.Param(autocomplete=ticker_autocomp)):
       # """🌟Returns the Logo of a Company - Downloadable"""
       # await inter.response.defer(ephemeral=False)
       # embed = disnake.Embed(title=f"```py\nLogo for {symbol.upper()}.```", color=disnake.Colour.random())
        #embed.set_image(url=f"{logo}")
        #await inter.edit_original_message(embed=embed)


    @stock.sub_command()
    async def insider_summary(inter:disnake.AppCmdInter):
        """📊Returns the latest and largest insider summary information."""
        await inter.response.defer(with_message=True, ephemeral=False)
        data = client.latest_insider_trading_summary()
        headers = "```py\n Symbol  | Amount  | Market Cap | % of Market Cap```"
        index1 = data[0]
        itsumsymbol1 = index1['Ticker']
        itsumamount1 = float(round(index1['Amount'] * 0.000001, ndigits=1))
        itsummktpct1 = index1['% of Mkt Cap']
        itmsummktcap1 = float(round(index1['Market Cap'] * 0.000000001, ndigits=1))



        index2 = data[1]
        itsumsymbol2 = index2['Ticker']
        itsumamount2 = float(round(index2['Amount'] * 0.000001, ndigits=1))
        itsummktpct2 = index2['% of Mkt Cap']
        itmsummktcap2 = float(index2['Market Cap'] * 0.000000001)
        itmsummktcap2 = float(round(index2['Market Cap'] * 0.000000001, ndigits=1))



        index3 = data[2]
        itsumsymbol3 = index3['Ticker']
        itsumamount3 = float(round(index3['Amount'] * 0.000001, ndigits=1))
        itsummktpct3 = index3['% of Mkt Cap']
        itmsummktcap3 = float(index3['Market Cap'] * 0.000000001)
        itmsummktcap3 = float(round(index3['Market Cap'] * 0.000000001, ndigits=1))


        index4 = data[3]
        itsumsymbol4 = index4['Ticker']
        itsumamount4 = float(round(index4['Amount'] * 0.000001, ndigits=1))
        itsummktpct4 = index4['% of Mkt Cap']
        itmsummktcap4 = float(index4['Market Cap'] * 0.000000001)
        itmsummktcap4 = float(round(index4['Market Cap'] * 0.000000001, ndigits=1))

        index5 = data[4]
        itsumsymbol5 = index5['Ticker']
        itsumamount5 = float(round(index5['Amount'] * 0.000001, ndigits=1))
        itsummktpct5 = index5['% of Mkt Cap']
        itmsummktcap5 = float(round(index5['Market Cap'] * 0.000000001, ndigits=1))


        index6 = data[5]
        itsumsymbol6 = index6['Ticker']
        itsumamount6 = float(round(index6['Amount'] * 0.000001, ndigits=1))
        itsummktpct6 = index6['% of Mkt Cap']
        itmsummktcap6 = float(round(index6['Market Cap'] * 0.000000001, ndigits=1))


        index7 = data[6]
        itsumsymbol7 = index7['Ticker']
        itsumamount7 = float(round(index7['Amount'] * 0.000001, ndigits=1))
        itsummktpct7 = index7['% of Mkt Cap']
        itmsummktcap7 = float(round(index7['Market Cap'] * 0.000000001, ndigits=1))


        index8 = data[7]
        itsumsymbol8 = index8['Ticker']
        itsumamount8 = float(round(index8['Amount'] * 0.000001, ndigits=1))
        itsummktpct8 = index8['% of Mkt Cap']
        itmsummktcap8 = float(round(index8['Market Cap'] * 0.000000001, ndigits=1))

        index9 = data[8]
        itsumsymbol9 = index9['Ticker']
        itsumamount9 = float(round(index9['Amount'] * 0.000001, ndigits=1))
        itsummktpct9 = index9['% of Mkt Cap']
        itmsummktcap9 = float(round(index9['Market Cap'] * 0.000000001, ndigits=1))

        index10 = data[9]
        itsumsymbol10 = index10['Ticker']
        itsumamount10 = float(round(index10['Amount'] * 0.000001, ndigits=1))
        itsummktpct10 = round(index10['% of Mkt Cap'], ndigits=1)
        itmsummktcap10 = float(round(index10['Market Cap'] * 0.000000001, ndigits=1))
        em = disnake.Embed(title="Latest Insider Trading Summary - Top 10", color=disnake.Colour.dark_purple())
        em.add_field(name=f"#1 - {itsumsymbol1}", value=f"```py\n Amount: {itsumamount1} million. Mkt Cap: {itmsummktcap1} billion or '{itsummktpct1}%'```", inline=True)
        em.add_field(name=f"#2 - {itsumsymbol2}", value=f"```py\n Amount: {itsumamount2} million. Mkt Cap: {itmsummktcap2} billion or '{itsummktpct2}%'```", inline=True)
        em.add_field(name=f"#3 - {itsumsymbol3}", value=f"```py\n Amount: {itsumamount3} million. Mkt Cap: {itmsummktcap3} billion or '{itsummktpct3}%'```", inline=True)
        em.add_field(name=f"#4 - {itsumsymbol4}", value=f"```py\n Amount: {itsumamount4} million. Mkt Cap: {itmsummktcap4} billion or '{itsummktpct4}%'```", inline=True)
        em.add_field(name=f"#5 - {itsumsymbol5}", value=f"```py\n Amount: {itsumamount5} million. Mkt Cap: {itmsummktcap5} billion or '{itsummktpct5}%'```", inline=True)
        em.add_field(name=f"#6 - {itsumsymbol6}", value=f"```py\n Amount: {itsumamount6} million. Mkt Cap: {itmsummktcap6} billion or '{itsummktpct6}%'```", inline=True)
        em.add_field(name=f"#7 - {itsumsymbol7}", value=f"```py\n Amount: {itsumamount7} million. Mkt Cap: {itmsummktcap7} billion or '{itsummktpct7}%'```", inline=True)
        em.add_field(name=f"#8 - {itsumsymbol8}", value=f"```py\n Amount: {itsumamount8} million. Mkt Cap: {itmsummktcap8} billion or '{itsummktpct8}%'```", inline=True)
        em.add_field(name=f"#9 - {itsumsymbol9}", value=f"```py\n Amount: {itsumamount9} million. Mkt Cap: {itmsummktcap9} billion or '{itsummktpct9}%'```", inline=True)
        em.add_field(name=f"#10 - {itsumsymbol10}", value=f"```py\n Amount: {itsumamount10} million. Mkt Cap: {itmsummktcap10} billion or '{itsummktpct10}%'```", inline=True)
        await inter.edit_original_message(embed=em)




    @stock.sub_command()
    async def leverage(inter:disnake.AppCmdInter, ticker: str=commands.Param(autocomplete=tickerlist_autocomp)):
        """📊Return overnight rates / short and long rates / short type for a ticker."""
        await inter.response.defer(with_message=True, ephemeral=False)

        em = disnake.Embed(title=f"Leverage for {ticker}", description=f"```py\nTrade Type: {LeverageDropdown(ticker).tradetype}``` ```py\nShort Type:\n{LeverageDropdown(ticker).shorttype}``` ```py\nTrade Policy: {LeverageDropdown(ticker).tradepolicy}```", color=disnake.Colour.dark_orange())
        em.add_field(name="Short/Long:", value=f"```py\n Short Interest Rate:\n{LeverageDropdown(ticker).shortintrate}%``` ```py\n Long Interest Rate:\n{LeverageDropdown(ticker).longintrate}%```  ```py\nShort Rate: {LeverageDropdown(ticker).srate}% Long Rate: {LeverageDropdown(ticker).lrate}%```")
        em.add_field(name="Overnight:", value=f"```py\nOvernight Long Leverage: {LeverageDropdown(ticker).overnightlonglever}``` ```py\nOvernight Short Leverage: {LeverageDropdown(ticker).overnightshortlever}``` ```py\n\nOvernight Short Rate: {LeverageDropdown(ticker).onshortrate}%``` ```py\nOvernight Long Rate:\n{LeverageDropdown(ticker).onlongrate}%```")
        em.add_field(name="Day Trade:", value=f"```py\n Day Trade Long Leverage: {LeverageDropdown(ticker).daytradelonglever}``` ```py\nDay Trade Short Leverage: {LeverageDropdown(ticker).daytradeshortlever}``` ```py\nDay Trade Short Rate: {LeverageDropdown(ticker).dayshortrate}%``` ```py\nDay Trade Long Rate:\n{LeverageDropdown(ticker).daylongrate}%```")
        em.add_field(name="Crypto Transferrable?", value=f"```py\n {LeverageDropdown(ticker).crypto}```", inline=True)
        em.add_field(name="Can Fract?", value=f"```py\n {LeverageDropdown(ticker).canfract}```", inline=True)
        em.set_thumbnail(await poly.get_polygon_logo(ticker))
        em.set_footer(text="Implemented by FUDSTOP Trading", )
        view = disnake.ui.View()
        view.add_item(LeverageDropdown(ticker))
        await inter.edit_original_message(embed = em, view=view)



    @stock.sub_command()
    async def ipo(inter:disnake.AppCmdInter):
        """📊A list of upcoming and recent IPOs as per Stocksera."""
        await inter.response.defer(with_message=True, ephemeral=False)
        data = client.ipo_calendar()[0:20]
        items = "\n\n".join(f"{i['Date']} {i['Symbol']} {i['Name']} Price: ${i['Expected Price']} Status: {i['Status']} #ofShares: {i['Number Shares']}" for i in data)
        em = disnake.Embed(title="Recent and Upcoming IPOs", description=f"```py\n{items}```", color=disnake.Colour.dark_gold())
        await inter.edit_original_message(embed = em)





def setup(bot:commands.Bot):
    bot.add_cog(Stock(bot))
    print(f"> Extension {__name__} is ready\n")