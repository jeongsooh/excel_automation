import pandas as pd
import os
import openpyxl

# 각 충전기 별로 사용한 이력이 있는 충전기 및 id에 대해서 상태를 수집한 통계를
# con_per_cpstats.csv 화일에 기록

path_dir = './data_org'

def watching_used_cp(file_list):

  stats_list = []

  for file in file_list:
    filename = path_dir + "/" + file + ".csv"
    xlsx = pd.read_csv(filename, usecols=[1,3,6,15,10])
    condition = (xlsx.chgertype == 2) & (xlsx.stat == 3)
    cp = xlsx[condition]
    numofused = len(cp)
    print("충전한 완속충전기 숫자: ", numofused)
    index_list = [item for item in cp.statid]
    stats_list = stats_list + index_list

  stats_list = list(set(stats_list))
  print ("충전한 충전기 id 숫자", len(stats_list))
  return stats_list


def ext_cpstat_df(csvfile):
  filename = path_dir + "/" + csvfile + ".csv"
  df_xlsx = pd.read_csv(filename, usecols=[1,2,3,6,15,10])

  condition = (df_xlsx.chgertype == 2) & (df_xlsx['statid'].isin(watched_cplist))
  used_cp = df_xlsx[condition]
  numofslow = len(used_cp.index)
  print("충전이력이 있는 완속 숫자: ", numofslow)
  print(used_cp)

  return used_cp

# 사용한 충전기 id 추출
file_list = os.listdir(path_dir)
file_list_csv = [file[0:13] for file in file_list if file.endswith(".csv")]
watched_cplist = watching_used_cp(file_list_csv)
# print(watched_cplist)

file_list_csv = [file[0:13] for file in file_list if file.endswith(".csv")]

con_cpstats = pd.DataFrame()
counter = 1
for csvfile in file_list_csv:
  con_cpstat = ext_cpstat_df(csvfile)
  if counter == 1:
    df_stats = con_cpstat['stat']
    con_cpstat = con_cpstat.drop(['stat'], axis=1)
    con_cpstats = pd.concat([con_cpstats, con_cpstat], axis=1)
    con_cpstats = pd.concat([con_cpstats, df_stats], axis=1)
  else:
    con_cpstats = pd.merge(con_cpstats, con_cpstat, how='outer', on=['statid', 'chgerid', 'chgertype', 'busiid', 'output'])
    # con_cpstats = pd.concat([con_cpstats, df_stats], axis=1)
  con_cpstats.rename(columns={'stat': csvfile}, inplace=True)
  print("csv 화일: " + csvfile + " 완료: ",  counter, " of ", len(file_list_csv))
  counter += 1

print(con_cpstats)
con_cpstats.to_csv('./con_per_cpstats.csv')