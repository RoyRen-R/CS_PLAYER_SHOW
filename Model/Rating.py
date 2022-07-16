#!/usr/bin/env python
# coding: utf-8

# In[7]:


def predict(ADR, KAST, IMPACT, KillsRound, DeathsRound):
    # 导包-------------------------------------------------------------------------------------------------------------------------------------
    import pandas as pd
    import pickle
    model = pickle.load(open('G:/ProJect/Model/Rating_predict_model.dat', 'rb'))

    # 封装输入数据-----------------------------------------------------------------------------------------------------------------------------
    data_input = pd.DataFrame(columns=['ADR', 'KAST', 'IMPACT', 'KillRating', 'SurvivalRating'])
    data_input.at[0, 'ADR'] = ADR
    data_input.at[0, 'KAST'] = KAST
    data_input.at[0, 'IMPACT'] = IMPACT
    data_input.at[0, 'KillRating'] = KillsRound
    data_input.at[0, 'SurvivalRating'] = 1 - DeathsRound

    # 预测Rating-------------------------------------------------------------------------------------------------------------------------------
    result = model.predict(data_input)
    result = result.round(decimals=2)
    return result
