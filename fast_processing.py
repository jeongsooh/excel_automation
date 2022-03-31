import pandas as pd
import os
import openpyxl

# 매일 데이터 중에서 급속충전기 상태를 받아서 아래 상태 데이터 추출
# cpstat = {
#   "comm_error" : 0,   # 통신이상  1
#   "Ready" : 0,        # 충전대기  2
#   "Charging" : 0,     # 충전 중   3
#   "Stop" : 0,         # 운전중지  4
#   "Checking" : 0,     # 점검 중   5
#   "Unknown" : 0       # 상태미확인 9
# }

path_dir = './data'


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
  condition = xlsx.chgertype != 2
  cp = xlsx[condition]
  numoffast = len(cp.index)
  # condition = (xlsx.chgertype == 2) & (xlsx.busiid != "SF")
  # cp_7 = xlsx[condition]
  # numof7kW = len(cp_7.index)

  # condition = (xlsx.chgertype == 2) & (xlsx.busiid == "SF")
  # cp_3 = xlsx[condition]
  # numof3kW = len(cp_3.index)


  df50_cpstats = cpstats_from(cp)
  # df3_cpstats = cpstats_from(cp_3)

  df50_head = [numofall, numoffast]
  df50_head_cpstats = pd.DataFrame(df50_head, index=['num_of_cp', 'fast_cp'], columns=[csvfile])

  df_cpstats = pd.concat([df50_head_cpstats, df50_cpstats])

  return df_cpstats


file_list = os.listdir(path_dir)
file_list_csv = [file[0:13] for file in file_list if file.endswith(".csv")]
# file_list_csv = ['220310-022031', '220310-030036']
df_cpstats = pd.DataFrame()
for csvfile in file_list_csv:
  df_cpstat = cpstats_df(csvfile)
  df_cpstats = pd.concat([df_cpstats, df_cpstat], axis=1)
  print("csv 화일: " + csvfile + " 완료")

print(df_cpstats)
df_cpstats.to_excel('./fastcpstats.xlsx')

