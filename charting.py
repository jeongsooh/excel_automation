# processing.py에서 추출한 통계데이터 cpstats.csv 화일을 기반으로 
# 7kW, 3kW 각각의 순간이용율을 charging / (chargign + ready)로 환산해서
# 데이터프레임에 추가하고 기간 내 트렌드를 chart로 나타냄
# 10  Comm_error       0.000000       0.000000       0.000000  ...       0.000000       0.000000       0.000000       0.000000
# 11       Ready    8564.000000    8653.000000    8748.000000  ...    8529.000000    8528.000000    8527.000000    8523.000000
# 12    Charging     268.000000     179.000000      86.000000  ...     139.000000     141.000000     141.000000     145.000000
# 13        Stop     422.000000     422.000000     420.000000  ...    1044.000000    1043.000000    1044.000000    1044.000000
# 14    Checking       0.000000       0.000000       0.000000  ...       0.000000       0.000000       0.000000       0.000000
# 15     Unknown     102.000000     102.000000     102.000000  ...      61.000000      61.000000      61.000000      61.000000
# 16      avg_7k       0.174858       0.169197       0.164145  ...       0.092757       0.093179       0.093166       0.093551
# 17      avg_3k       0.030344       0.020267       0.009735  ...       0.016036       0.016265       0.016267       0.016728


import matplotlib.pyplot as plt
import os
import pandas as pd

filename = './cpstats.xlsx'
xlsx = pd.read_excel(filename)

avg_7k_data = {}
avg_3k_data = {}
avg_7k = [item for item in xlsx if item]
for item in xlsx:
  if item == "Unnamed: 0":
    avg_7k_data[item] = "avg_7k"
    avg_3k_data[item] = "avg_3k"
  else:
    avg_7k_data[item] = xlsx[item].loc[6]/(xlsx[item].loc[6]+xlsx[item].loc[5])
    avg_3k_data[item] = xlsx[item].loc[12]/(xlsx[item].loc[12]+xlsx[item].loc[11])
# print(avg_7k_data)
# print(avg_3k_data)
xlsx = xlsx.append(avg_7k_data, ignore_index=True)
xlsx = xlsx.append(avg_3k_data, ignore_index=True)
print(xlsx)
print("number of sample data", len(xlsx))
df_7k_trend = xlsx.loc[16]
df_3k_trend = xlsx.loc[17]

df_7k_chart = df_7k_trend[1:]
df_3k_chart = df_3k_trend[1:]
# df_3k = xlsx.loc[12]
# print(df_3k)

# df_7k_sum = df_7k[1:]
# df_3k_sum = df_3k[1:]


# filename = './cpstats.xlsx'
# xlsx = pd.read_excel(filename)
# print(xlsx)
# df_7k = xlsx.loc[6]
# df_3k = xlsx.loc[12]

# df_7k_sum = pd.concat([df_7k_sum, df_7k[1:]]) 
# df_3k_sum = pd.concat([df_3k_sum, df_3k[1:]])

df_7k_chart.plot()
df_3k_chart.plot()

plt.show()
plt.show()