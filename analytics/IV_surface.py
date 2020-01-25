from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

import datetime
import py_vollib.black_scholes_merton.implied_volatility as BSM
import numpy as np
import quantsbin.derivativepricing as qbdp
import option_chain_get
import multiprocessing
import pandas as pd
from scipy.interpolate import griddata
pd.option_context('display.max_rows', None, 'display.max_columns', None)
import option_data
today = datetime.datetime.today().strftime('%Y%m%d')
print(today)

def greeks(target_value, flag, S, K,t1,t0, r, div,key=None):
    if flag == 'C':
        call_put = 'Call'
    else:
        call_put = "Put"

    d1 = datetime.datetime.strptime(t1,'%Y%m%d')
    d0 = datetime.datetime.strptime(t0,'%Y%m%d')



    delta = d1-d0
    delta_annual = delta.days / 365


    sigma = BSM.implied_volatility(target_value, S, K, delta_annual, r, div, flag.lower())

    risk_parameters = {'delta_spot': 0.02, 'delta_vol': 0.02, 'delta_rf_rate': 0.02,
                       'delta_time': 1}  # TODO Fix with next quantsbin release


    # equity_o = qbdp.EqOption(option_type=call_put, strike=K, expiry_date=t1, expiry_type='American')
    # engine = equity_o.engine(model="Binomial", spot0=S, pricing_date=t0,
    #                          rf_rate=r, yield_div=div, volatility=sigma)

    # greeks = engine.risk_parameters(**risk_parameters)

    # greeks['key'] = key
    # print(greeks)
    return sigma




r = 0.018
div = 0.0118
kind = 'C'
spot = 260
ticker = 'AAPL'

chain = option_chain_get.get_chain(ticker,['20200117', '20200221', '20200619', '20191206', '20191220', '20191227', '20191122', '20200918', '20191108', '20200320', '20191129', '20191213', '20200417'])

print(chain)

t0 = datetime.datetime.today()

dfs = []

inn = 0
for exp in chain.keys():

    # chain[exp] = chain[exp].iloc[:10]

    t1 = datetime.datetime.strptime(exp,'%Y%m%d')

    dte = t1-t0

    print(exp)
    chain[exp]['IV'] = 0
    chain[exp]['DTE'] = dte.days
    chain[exp] = chain[exp][chain[exp]['kind'] == kind]
    # print(chain[list(chain.keys())[0]]['strike'])
    # chain[exp]=chain[exp].loc[chain[exp]['strike'].isin(chain[list(chain.keys())[0]]['strike'])]
    # chain[exp] = chain[exp].merge(chain[list(chain.keys())[0]], on="strike", how='inner')
    # print(chain[exp])
    input_list =[]
    x = 0
    for i in range(len(chain[exp]['strike'])):
        if chain[exp]['close'].iloc[i] == 0.00:
            chain[exp]['close'][i] = 0.01
        elif chain[exp]['close'].iloc[i] == 'NaN':
            chain[exp]['close'][i] = 0.01
        # input_list.append([chain[exp]['close'].iloc[i],chain[exp]['kind'].iloc[i],36,chain[exp]['strike'].iloc[i],exp,today,r,div,x])

    # print(input_list)
    # with multiprocessing.Pool(processes=4) as pool:
    #     g = pool.starmap(greeks, input_list)
    #     print(g)
    #     for f in g:
    #         chain[exp]['IV'].iloc[f['key']] = f['IV']
    #     print('IV:', BSM.implied_volatility(chain[exp]['close'].iloc[i], spot, chain[exp]['strike'].iloc[i], dte.days, r, div, chain[exp]['kind'].iloc[i].lower()))
        try:
            iv =greeks(chain[exp]['close'].iloc[i],chain[exp]['kind'].iloc[i],spot,chain[exp]['strike'].iloc[i],exp,today,r,div)
            # iv = BSM.implied_volatility(chain[exp]['close'].iloc[i], spot, chain[exp]['strike'].iloc[i], dte.days, r, div, chain[exp]['kind'].iloc[i].lower())
            # print(chain[exp]['strike'].iloc[i],g)
        except:
            iv = 0
        chain[exp]['IV'].iloc[i] = iv

        x += 1
    chain[exp] = chain[exp].dropna(subset=['close', 'IV'])
    df =chain[exp][~(chain[exp]['IV'] <= 0.001)]

    if inn == 0:
        og_df = df
    else:
        dfs.append(df)

    inn +=1


df_3d = og_df
for innn in dfs:
    print(innn)
    df_3d = df_3d.append(innn)

df = df_3d
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(df)

# re-create the 2D-arrays
x1 = np.linspace(df['strike'].min(), df['strike'].max(), len(df['strike'].unique()))
y1 = np.linspace(df['DTE'].min(), df['DTE'].max(), len(df['DTE'].unique()))
x2, y2 = np.meshgrid(x1, y1)
z2 = griddata((df['strike'], df['DTE']), df['IV'], (x2, y2), method='cubic')

fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')
# %matplotlib

# surf = ax.plot_surface(x2, y2, z2, rstride=1, cstride=1, cmap=plt.cm.get_cmap('RdYlGn'),linewidth=0, antialiased=False)
# fig.colorbar(surf, shrink=0.5, aspect=5)

surf = ax.plot_wireframe(x2, y2, z2, rstride=1, cstride=1)


# ax.zaxis.set_major_locator(LinearLocator(10))
# ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
ax.view_init(15, 70)
ax.set_ylabel('DTE')
ax.set_xlabel('strike')
ax.set_zlabel('IV')
ax.set_facecolor('xkcd:white')
if kind== 'C':
    tit = 'IV Surface' +'\n'+ ticker + ' Calls'
else:
    tit = 'IV Surface' + '\n' + ticker + ' Puts'

plt.title(tit)
fig.tight_layout()
# ~~~~ MODIFICATION TO EXAMPLE ENDS HERE ~~~~ #

plt.show()