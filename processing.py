import pandas as pd
import os
import openpyxl

# 매일 데이터 중에서 완속충전기 상태를 받아서 아래 상태 데이터 추출
# cpstat = {
#   "comm_error" : 0,   # 통신이상  1
#   "Ready" : 0,        # 충전대기  2
#   "Charging" : 0,     # 충전 중   3
#   "Stop" : 0,         # 운전중지  4
#   "Checking" : 0,     # 점검 중   5
#   "Unknown" : 0       # 상태미확인 9
# }
# 임의의 시간에 전체 CP status를 csv 화일로 다운받아서stat의 통계를 7kWm 3kW로 나누어서 출력
#     Unnamed: 0  220301-025227  220301-032100  220301-034510  ...  220328-110219  220328-114230  220328-122241  220328-130252
# 0    num_of_cp  100540.000000  100540.000000  100540.000000  ...  105404.000000  105404.000000  105404.000000  105404.000000
# 1      slow_cp   84966.000000   84966.000000   84966.000000  ...   89634.000000   89634.000000   89634.000000   89634.000000
# 2       cp_7kW   75610.000000   75610.000000   75610.000000  ...   79861.000000   79861.000000   79861.000000   79861.000000
# 3       cp_3kW    9356.000000    9356.000000    9356.000000  ...    9773.000000    9773.000000    9773.000000    9773.000000
# 4   Comm_error    2503.000000    2518.000000    2508.000000  ...    4640.000000    4587.000000    4594.000000    4640.000000
# 5        Ready   54579.000000   54931.000000   55250.000000  ...   61874.000000   61896.000000   61886.000000   61644.000000
# 6     Charging   11566.000000   11187.000000   10850.000000  ...    6326.000000    6360.000000    6358.000000    6362.000000
# 7         Stop     166.000000     166.000000     166.000000  ...     200.000000     202.000000     203.000000     202.000000
# 8     Checking     753.000000     758.000000     775.000000  ...     806.000000     802.000000     801.000000     998.000000
# 9      Unknown    6043.000000    6050.000000    6061.000000  ...    6015.000000    6014.000000    6019.000000    6015.000000
# 10  Comm_error       0.000000       0.000000       0.000000  ...       0.000000       0.000000       0.000000       0.000000
# 11       Ready    8564.000000    8653.000000    8748.000000  ...    8529.000000    8528.000000    8527.000000    8523.000000
# 12    Charging     268.000000     179.000000      86.000000  ...     139.000000     141.000000     141.000000     145.000000
# 13        Stop     422.000000     422.000000     420.000000  ...    1044.000000    1043.000000    1044.000000    1044.000000
# 14    Checking       0.000000       0.000000       0.000000  ...       0.000000       0.000000       0.000000       0.000000
# 15     Unknown     102.000000     102.000000     102.000000  ...      61.000000      61.000000      61.000000      61.000000


path_dir = './data_used'


def cpstat_refining(cpstats, cpstats_refined):
  cpstats_refined[0] = cpstats[1]
  cpstats_refined[1] = cpstats[2]
  cpstats_refined[2] = cpstats[3]
  cpstats_refined[3] = cpstats[4]
  cpstats_refined[4] = cpstats[5]
  cpstats_refined[5] = cpstats[9]

  return cpstats_refined


def cpstats_from(xlsx):
  cpstats = [0,0,0,0,0,0,0,0,0,0]
  cpstats_refined = [0,0,0,0,0,0]

  for index in xlsx.index:
    cpstats[xlsx.loc[index].stat] +=1 
  
  cpstats_refined = cpstat_refining(cpstats, cpstats_refined)

  return pd.DataFrame(cpstats_refined, index=['Comm_error', 'Ready', 'Charging', 'Stop', 'Checking', 'Unknown'], columns=[csvfile])

def cpstats_df(csvfile):
  filename = path_dir + "/" + csvfile + ".csv"
  xlsx = pd.read_csv(filename, usecols=[1,3,6,15,10])

  numofall = len(xlsx.index)
  condition = xlsx.chgertype == 2
  cp = xlsx[condition]
  numofslow = len(cp.index)
  condition = (xlsx.chgertype == 2) & (xlsx.busiid != "SF")
  cp_7 = xlsx[condition]
  numof7kW = len(cp_7.index)

  condition = (xlsx.chgertype == 2) & (xlsx.busiid == "SF")
  cp_3 = xlsx[condition]
  numof3kW = len(cp_3.index)


  df7_cpstats = cpstats_from(cp_7)
  df3_cpstats = cpstats_from(cp_3)

  df_head = [numofall, numofslow, numof7kW, numof3kW]
  df_head_cpstats = pd.DataFrame(df_head, index=['num_of_cp', 'slow_cp', 'cp_7kW', 'cp_3kW'], columns=[csvfile])

  df_cpstats = pd.concat([df_head_cpstats, df7_cpstats, df3_cpstats])

  return df_cpstats


file_list = os.listdir(path_dir)
file_list_csv = [file[0:13] for file in file_list if file.endswith(".csv")]
# file_list_csv = ['220310-022031', '220310-030036']
counter = 1
df_cpstats = pd.DataFrame()
for csvfile in file_list_csv:
  df_cpstat = cpstats_df(csvfile)
  df_cpstats = pd.concat([df_cpstats, df_cpstat], axis=1)
  
  print("csv 화일: " + csvfile + " 완료: ",  counter, " of ", len(file_list_csv))
  counter += 1

print(df_cpstats)
df_cpstats.to_csv('./cpstats.csv')

