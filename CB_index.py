# -*- coding: UTF-8 -*-
import pandas as pd
import numpy as np
from WindPy import *
w.start()
start_date = '2004-01-01'
end_date = '2018-11-23'

# 读取全部可转债的Wind代码
df = pd.read_csv('C:\\Users\\yz283\\Desktop\\cb.csv')
cb = ','.join(df.iloc[:,0].tolist())
# 单一Wind账号不足以导出全部数据，期间需切换至另一账号。故预存好数据后直接读取。
# close = np.nan_to_num(np.array(w.wsd(cb, "close", start_date, end_date).Data))
# amt = np.array(w.wsd(cb, "amt", start_date, end_date).Data)
# rating = np.array(w.wsd(cb, "rate_ratebond", start_date, end_date, "ratingAgency=101;unit=1").Data)
# out_amount = np.array(w.wsd(cb, "outstandingbalance", start_date, end_date).Data)
close = np.array(pd.read_csv('C:\\Users\\yz283\\Desktop\\close.csv').iloc[:,1:])
amt = np.array(pd.read_csv('C:\\Users\\yz283\\Desktop\\amt.csv').iloc[:,1:])
rating = np.array(pd.read_csv('C:\\Users\\yz283\\Desktop\\rating.csv').iloc[:,1:])
out_amount = np.array(pd.read_csv('C:\\Users\\yz283\\Desktop\\out.csv').iloc[:,1:])
# pd.Series(pd.DataFrame(rating).values.ravel()).unique()

cb_index = []
num = []
amnt = []
ticker = []
for i in range(close.shape[1]):
    weight = np.array([out_amount[j, i] if (out_amount[j, i] > 0.3 and amt[j, i] > 0) else 0
              for j in range(close.shape[0])])
    weight_AAA = np.array([out_amount[j, i] if (out_amount[j, i] > 0.3 and amt[j, i] > 100000 and
                                                rating[j, i] == 'AAA') else 0
              for j in range(close.shape[0])])
    weight_AAAd = np.array([out_amount[j, i] if (out_amount[j, i] > 0.3 and amt[j, i] > 100000 and
                                                rating[j, i] == 'AAA-') else 0
                           for j in range(close.shape[0])])
    weight_AAu = np.array([out_amount[j, i] if (out_amount[j, i] > 0.3 and amt[j, i] > 100000 and
                                                rating[j, i] == 'AA+') else 0
                           for j in range(close.shape[0])])
    weight_AA = np.array([out_amount[j, i] if (out_amount[j, i] > 0.3 and amt[j, i] > 100000 and
                                                rating[j, i] == 'AA') else 0
                           for j in range(close.shape[0])])
    weight_AAd = np.array([out_amount[j, i] if (out_amount[j, i] > 0.3 and amt[j, i] > 100000 and
                                                rating[j, i] == 'AA-') else 0
                           for j in range(close.shape[0])])
    weight_Au = np.array([out_amount[j, i] if (out_amount[j, i] > 0.3 and amt[j, i] > 100000 and
                                                rating[j, i] == 'A+') else 0
                           for j in range(close.shape[0])])
    cb_index.append([sum(close[:,i] * weight/sum(weight)),sum(close[:,i] * weight_AAA/sum(weight_AAA)),
                    sum(close[:, i] * weight_AAAd / sum(weight_AAAd)),sum(close[:,i] * weight_AAu/sum(weight_AAu)),
                    sum(close[:, i] * weight_AA / sum(weight_AA)),sum(close[:,i] * weight_AAd/sum(weight_AAd)),
                    sum(close[:, i] * weight_Au / sum(weight_Au))])
    num.append([len(weight[weight > 0]), len(weight_AAA[weight_AAA > 0]), len(weight_AAAd[weight_AAAd > 0]),
           len(weight_AAu[weight_AAu > 0]), len(weight_AA[weight_AA > 0]), len(weight_AAd[weight_AAd > 0]),
           len(weight_Au[weight_Au > 0])])
    amnt.append([weight.sum(), weight_AAA.sum(), weight_AAAd.sum(), weight_AAu.sum(),
                 weight_AA.sum(), weight_AAd.sum(), weight_Au.sum()])
    ticker.append([np.array(df.iloc[:,0])[weight > 0], np.array(df.iloc[:,0])[weight_AAA > 0],
                   np.array(df.iloc[:, 0])[weight_AAAd > 0],np.array(df.iloc[:,0])[weight_AAu > 0],
                   np.array(df.iloc[:, 0])[weight_AA > 0],np.array(df.iloc[:,0])[weight_AAd > 0],
                   np.array(df.iloc[:, 0])[weight_Au > 0]])
pd.DataFrame(cb_index, columns = ['Index','AAA','AAA-','AA+','AA','AA-','A+']).\
    to_csv('C:\\Users\\yz283\\Desktop\\cb_index.csv')
pd.DataFrame(num, columns = ['Index','AAA','AAA-','AA+','AA','AA-','A+']).\
    to_csv('C:\\Users\\yz283\\Desktop\\cb_num.csv')
pd.DataFrame(amnt, columns = ['Index','AAA','AAA-','AA+','AA','AA-','A+']).\
    to_csv('C:\\Users\\yz283\\Desktop\\cb_amnt.csv')