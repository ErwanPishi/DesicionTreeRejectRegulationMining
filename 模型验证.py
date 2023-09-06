import toad
import numpy as np
import pandas as pd
from pypmml import Model
import matplotlib.pyplot as plt
from toad.metrics import KS,KS_bucket,PSI

dt_model = Model.fromFile('DecTree_ver3.1.pmml')
#验证集
test_df=pd.read_csv('test.csv',index_col=0).reset_index(drop=True)
#查看模型使用的变量
dt_model.inputNames
#预测结果
tmp = dt_model.predict(test_df[dt_model.inputNames])
test_df['seg_id'] = tmp.values
#查看分布和缺失
test_df['seg_id'].value_counts()
test_df.seg_id.isnull().sum()
#分箱结果 聚合函数
test_df.groupby('seg_id').agg(total=('flag','count'),bads=('flag','sum'),br=('flag','mean'))
'''
        total  bads        br
seg_id                       
1        2171    63  0.029019
2        3512   144  0.041002
3        4254   197  0.046309
4        4456   277  0.062163
5         247    28  0.113360
''' 
#训练集
train_df=pd.read_excel('/Users/ziyan/Desktop/short_time_self_noxrh.xlsx')[:34159]
train_df.drop(columns=['crdt_seq_id', 'dubil_num', 'ln_distr_dt', 'crdt_appl_dt',
       'crdt_appl_m', 'crtf_num', 'max_ovd', 'repay_dt', 'mob','age',
       'addr', 'marr', 'edu', 'cust_cn_nm', 'cust_mblphn_no', 'serial_num'],
        inplace=True)
train_df.fillna(-99,inplace=True)
tmp = dt_model.predict(train_df[dt_model.inputNames])
train_df['seg_id'] = tmp.values
train_df.groupby('seg_id').agg(total=('flag','count'),bads=('flag','sum'),br=('flag','mean'))
'''
        total  bads        br
seg_id                       
1        5393   139  0.025774
2        9981   384  0.038473
3        9706   506  0.052133
4        8526   624  0.073188
5         553    78  0.141049
'''









