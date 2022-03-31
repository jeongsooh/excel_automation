import pandas as pd
import os
import openpyxl

# processing.py와 다르게 기간 내 사용한 이력이 있는 충전기 만을 골라서 충전 기록을 통계로
# used_cpstats.csv 에 기록

# 매일 데이터 중에서 완속충전기 상태를 받아서 아래 상태 데이터 추출
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
  xlsx = pd.read_csv(filename, usecols=[1,2,3,6,10,15])
  print(xlsx)

  numofall = len(xlsx.index)

  condition = (xlsx.chgertype == 2) & (xlsx['statid'].isin(watched_cplist))
  cp = xlsx[condition]
  numofslow = len(cp.index)
  print("충전이력이 있는 완속 숫자: ", numofslow)

  condition = cp.busiid != "SF"
  cp_7 = cp[condition]
  numof7kW = len(cp_7.index)

  condition = cp.busiid == "SF"
  cp_3 = cp[condition]
  numof3kW = len(cp_3.index)


  df7_cpstats = cpstats_from(cp_7)
  df3_cpstats = cpstats_from(cp_3)

  df_head = [numofall, numofslow, numof7kW, numof3kW]
  df_head_cpstats = pd.DataFrame(df_head, index=['num_of_cp', 'slow_cp', 'cp_7kW', 'cp_3kW'], columns=[csvfile])

  df_cpstats = pd.concat([df_head_cpstats, df7_cpstats, df3_cpstats])

  return df_cpstats

def watching_used_cp(file_list):

  stats_list = []

  for file in file_list:
    filename = path_dir + "/" + file + ".csv"
    xlsx = pd.read_csv(filename, usecols=[1,3,6,15,10])
    condition = (xlsx.chgertype == 2) & (xlsx.stat == 3)
    cp = xlsx[condition]
    numofused = len(cp)
    print("충전한 충전기 대수: ", numofused)
    index_list = [item for item in cp.statid]
    stats_list = stats_list + index_list

  stats_list = list(set(stats_list))
  print (len(stats_list))
  return stats_list


file_list = os.listdir(path_dir)
file_list_csv = [file[0:13] for file in file_list if file.endswith(".csv")]
watched_cplist = watching_used_cp(file_list_csv)

file_list_csv = [file[0:13] for file in file_list if file.endswith(".csv")]
# file_list_csv = ['220310-022031', '220310-030036']
df_cpstats = pd.DataFrame()
counter = 1
for csvfile in file_list_csv:
  df_cpstat = cpstats_df(csvfile)
  df_cpstats = pd.concat([df_cpstats, df_cpstat], axis=1)

  print("csv 화일: " + csvfile + " 완료: ",  counter, " of ", len(file_list_csv))
  counter += 1

print(df_cpstats)
df_cpstats.to_csv('./used_cpstats.csv')



