#solscan API
import requests
import json
import datetime
import pandas as pd
from bokeh.plotting import figure, show
from bokeh.models import Range1d

# NFT Collections

def get_daily_volumes(collectionId, mintDate):
    params = {
        'collectionId': collectionId,
        'offset': 0,
        'limit': 100000
    }

    response = requests.get('https://api.solscan.io/collection/trade', params=params)
    data = json.loads(response.content.decode())['data']

    l = ['mint', 'name', 'symbol', 'price', 'collectionId', 'tradeTime', 'signature']
    df = pd.DataFrame(columns=l)
    for d in data:
        try:
            data2 = {k: d[k] for k in l}
            df = df.append(data2, ignore_index=True)
        except:
            pass  # doing nothing on exception

    df['trade_datetime'] = df.tradeTime.apply(lambda x: datetime.datetime.fromtimestamp(x))
    df['trade_date'] = df.trade_datetime.dt.date
    df['days_from_mint'] = (df.trade_date - datetime.datetime.strptime(mintDate, '%Y-%m-%d').date()).apply(
        lambda x: x.days)

    df['price'] = df.price.apply(lambda x: x * 0.000000001)
    df = df.groupby(['days_from_mint']).agg({'symbol': 'first', 'price': 'sum', 'signature': 'count'}, asIndex=False)

    return df


monkelabs = get_daily_volumes('f19329dcc67edd63f5545891fd3b383dde2cdc91b7ed49257add1c995bb6dd7c', '2022-01-29')
mhac = get_daily_volumes('a89007ce9eb8ac11b511272d4b9b98c6c1476314d5888047003d8204bcdff662','2022-02-12')
monke_rejects = get_daily_volumes('44c3d8fbe8eb2d17607a6fbf2b9d211060176fd5b195d09a30ab3035c86abf21','2022-02-05')
best_buds = get_daily_volumes('86f1da0e7d33d2895b309d39cab4ffbeefaa947cb10ee8f7fb74e8bf3ec9828e','2022-01-28')
dazed_ducks = get_daily_volumes('eb4c33fa2a1a6abd74d36a614459dc0a46ab7a846f793b0466c5b530aa903f78','2022-01-01')
fff = get_daily_volumes('b562eb85c5e04c87b741c617cfe6bcdaad505041ec3aa7257f801971278c8999',)
degods = get_daily_volumes('a38e8d9d1a16b625978803a7d4eb512bc20ff880c8fd6cc667944a3d7b5e4acf','2021-10-08')
pesky_penguins = get_daily_volumes('938f73df4a3b6222461276e90f8feb6e1fc621e1bb22b759738a0b26b598d93f','2021-10-09')
bored_ape_solana_club = get_daily_volumes('5f1c944e909495cf69096f4fdb27915f71e481b0186c5a5ebf4b551655f80665', '2022-01-14')

mhac = mhac.reset_index()
monke_rejects = monke_rejects.reset_index()
best_buds = best_buds.reset_index()
dazed_ducks = dazed_ducks.reset_index()
dazed_ducks = dazed_ducks[dazed_ducks.days_from_mint >= 0]
bored_ape_solana_club = bored_ape_solana_club.reset_index()


p1 = figure( title="Daily volume in SOL from mint date")
p1.grid.grid_line_alpha=0.3
p1.xaxis.axis_label = 'Days from mint'
p1.yaxis.axis_label = 'Daily volume (SOL)'

p1.line(mhac.days_from_mint, mhac.price, color='#E83845', legend_label='MHAC', line_width=3)
p1.line(monke_rejects.days_from_mint, monke_rejects.price, color='#746AB0', legend_label='MonkeRejects', line_width=3)
p1.line(best_buds.days_from_mint, best_buds.price, color='#33A02C', legend_label='BestBuds', line_width=3)
p1.line(dazed_ducks.days_from_mint,dazed_ducks.price, color='#FFCE30', legend_label='DDMC',line_width=3)
p1.line(bored_ape_solana_club.days_from_mint,bored_ape_solana_club.price, color='#288BA8', legend_label='BASC', line_width=3)


p1.legend.location = "top_right"

show(p1)

p2 = figure( title="Daily volume in # of NFTs traded from mint date")
p2.grid.grid_line_alpha=0.3
p2.xaxis.axis_label = 'Days from mint'
p2.yaxis.axis_label = 'Daily volume (SOL)'

p2.line(mhac.days_from_mint, mhac.signature, color='#E83845', legend_label='MHAC', line_width=3)
p2.line(monke_rejects.days_from_mint, monke_rejects.signature, color='#746AB0', legend_label='MonkeRejects', line_width=3)
p2.line(best_buds.days_from_mint, best_buds.signature, color='#33A02C', legend_label='BestBuds', line_width=3)
p2.line(dazed_ducks.days_from_mint,dazed_ducks.signature, color='#FFCE30', legend_label='DDMC',line_width=3)
p2.line(bored_ape_solana_club.days_from_mint,bored_ape_solana_club.signature, color='#288BA8', legend_label='BASC', line_width=3)

p2.y_range = Range1d(0, 500)
p2.legend.location = "top_right"