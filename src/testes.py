import pandas as pd
import entrada

df = pd.read_csv(r'C:\\Users\Luciano\Desktop\Workspace\Python\Projeto I\\Arquivos - Pacientes\column_bin_3a_2p.csv')

#print(entrada.ret1(df.columns, entrada.regra2))
#print(entrada.ret2(df.columns, entrada.regra2))

m = entrada.contagem(df.columns)
print(f'nmr -> {m}')

