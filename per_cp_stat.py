import pandas as pd

filename = 'con_per_cpstats.csv'
cpstats = [0,0,0,0,0,0,0,0,0,0]
stat_col = ['s0', 's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9']

df = pd.read_csv(filename)
df = df.fillna(0)
# print(df)
check_point = [item for num, item in enumerate(df.columns) if num > 5]
# print(check_point)
result = pd.DataFrame({
  'statid':
  df['statid'],
  'chgerid':
  df['chgerid'],
  'chgertype':
  df['chgertype'],
  'busiid':
  df['busiid'],
  'output':
  df['output'],
})
print(result)

result_list = []

for cpindex in df.index:
  for point in check_point:
    cpstats[int(df.loc[cpindex][point])] +=1
  # for num, col in enumerate(stat_col):
  #   print(result.loc[cpindex][col])
  #   print(cpstats[num])
  result_list.append(cpstats)
  print("cpindex = ",  cpindex, " from ", len(df.index))
  cpstats = [0,0,0,0,0,0,0,0,0,0]
# print(result_list)

df_result = pd.DataFrame(result_list, columns=[
  'nd0', 'comm_error', 'ready', 'charging', 'stop', 'checking', 'nd6', 'nd7', 'nd8', 'unknown'
], dtype= int)
# print(df_result)
con_result = pd.concat([result, df_result], axis=1)
print(con_result)
con_result.to_csv('./con_per_cpresult.csv')