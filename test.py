import os
import pandas as pd

path_dir = './data'

def cpstats_df(csvfile):
  filename = path_dir + "/" + csvfile + ".csv"
  xlsx = pd.read_csv(filename, usecols=[1,3,6,15,10])

  numofall = len(xlsx.index)
  condition = (xlsx.chgertype == 2) & (xlsx.stat == 3)
  cp = xlsx[condition]
  numofused = len(cp)
  print("충전한 충전기 대수: ", numofused)
  index_list = [item for item in cp.statid]
  return index_list

file_list = os.listdir(path_dir)
file_list_csv = [file[0:13] for file in file_list if file.endswith(".csv")]
# file_list_csv = ['220310-022031', '220310-030036']
# df_cpstats = pd.DataFrame()
stats_list = []
for csvfile in file_list_csv:
  df_cpstat = cpstats_df(csvfile)
  # df_cpstats = pd.concat([df_cpstats, df_cpstat], axis=1)
  stats_list = stats_list + df_cpstat

# print(df_cpstats)
  # stat_list = cpstats_df(csvfile)
  stats_list = list(set(stats_list))
# print (stats_list)
  print("csv 화일: " + csvfile + " 완료")
print("충전한 스테이션 id 개수: ",len(stats_list))

df_cpstats = pd.DataFrame()

for csvfile in file_list_csv:
  filename = path_dir + "/" + csvfile + ".csv"
  xlsx = pd.read_csv(filename, usecols=[1,2,3,10])
  condition = (xlsx.chgertype == 2)
  slowstat = xlsx[condition]
  print(slowstat)
  cpindex = slowstat.index
  print(cpindex)

  df_stat = []
  for index in cpindex:
    if slowstat.loc[index]['statid'] in stats_list:
      slowstat.drop(index)
  # print(len(df_stat))
  print(len(df_stat))
  # if df_cpstats.empty:
  #   condition = slowstat['statid'].isin(stats_list)
  #   usedstat = slowstat[condition]
  #   print("충전한 충전기 대수: ", len(usedstat))
  #   df_cpstats = pd.concat([df_cpstats, usedstat], axis=1)
  #   df_cpstats.rename(columns={'stat': csvfile}, inplace=True)
  # else:
  #   new_col = [slowstat.stat for slowstat.stat in slowstat]
  #   print(new_col)
    # df_cpstats = pd.concat([df_cpstats, usedstat.stat], axis=1)
    # df_cpstats.rename(columns={'stat': csvfile}, inplace=True)
# print(len(df_cpstats))
# print(df_cpstats)
# df_cpstats.to_excel('./used_cpstats.xlsx')



