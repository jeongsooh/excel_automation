import pandas as pd

df1 = pd.DataFrame({
  'statid':
  ['BN01', 'BN02', 'BN02', 'BN03'],
  'chgerid':
  [1, 1, 2, 1],
  'chgertype':
  [2, 2, 2, 2],
  'stat':
  [2, 3, 3, 9]
})

df2 = pd.DataFrame({
  'statid':
  ['BN01', 'BN02', 'BN02', 'BN03'],
  'chgerid':
  [2, 1, 2, 1],
  'chgertype':
  [2, 2, 2, 2],
  'stat':
  [2, 3, 3, 3]
})
print(df1)
print(df2['statid'])
df_merge = pd.merge(df1, df2, how='outer', on=['statid', 'chgerid', 'chgertype'])
print(df_merge)