import requests
import json
import datetime
import pandas as pd

params = {
    'address': 'Gzo5eNAnqeG4nKASrQQjd8LVvNxAxQnMHkHj2MHHjRMD'
}

response = requests.get('https://api.solscan.io/account/transaction', params=params)
data = json.loads(response.content.decode())['data']

l = ['blockTime', 'slot', 'txHash', 'fee', 'status', 'signer']

df = pd.DataFrame(columns=l)
for d in data:
    try:
        data2 = {k: d[k] for k in l}
        df = df.append(data2, ignore_index=True)
    except:
        pass  # doing nothing on exception

for i in range(5):
    params = {
        'address': 'Gzo5eNAnqeG4nKASrQQjd8LVvNxAxQnMHkHj2MHHjRMD',
        'before': data[-1].get('txHash')
    }
    response = requests.get('https://api.solscan.io/account/transaction', params=params)
    data = json.loads(response.content.decode())['data']

    for d in data:
        try:
            data2 = {k: d[k] for k in l}
            df = df.append(data2, ignore_index=True)
        except:
            pass  # doing nothing on exception