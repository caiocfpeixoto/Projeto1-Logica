import pandas as pd
import entrada

df = pd.read_csv(r'C:\\Users\Luciano\Desktop\Workspace\Python\Projeto I\\Arquivos - Pacientes\column_bin_3a_3p.csv')

m = entrada.contagem(df.columns)

print('rest1 - > ')
print( entrada.ret1(df.columns, m))
print('rest2 - > ')
print(entrada.ret2(df.columns, entrada.contagem(df.columns)))
print('rest3 - > ')
#print(entrada.ret3(df.columns, entrada.regra2))
print('rest4 - > ')
#print(+entrada.ret4(df.columns, entrada.regra2))
print('rest5 - > ')
print(entrada.ret5(df.columns, entrada.contagem(df.columns)))

