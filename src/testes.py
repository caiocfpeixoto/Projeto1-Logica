import pandas as pd
import entrada

# print(entrada.sem_patologia)

# print('###############################################')
# print('rest1 - > ')

# print( entrada.ret1(entrada.df.columns, entrada.contagem(entrada.df.columns)))

# print('###############################################')
# print('rest2 - > ')

# print(entrada.ret2(entrada.df.columns, entrada.contagem(entrada.df.columns)))

# print('###############################################')
# print('rest3 - > ')

# print(entrada.ret3(entrada.sem_patologia, entrada.contagem(entrada.df.columns)))

# print('###############################################')
# print('rest4 - > ')

# print(entrada.ret4(entrada.com_patologia, entrada.contagem(entrada.df.columns)))

# print('###############################################')
# print('rest5 - > ')

# print(entrada.ret5(entrada.com_patologia, entrada.contagem(entrada.df.columns)))

# print('###############################################')
# print('solução: ')

# print(entrada.patologia_solucao(entrada.df, entrada.contagem(entrada.df.columns)))

sol = entrada.patologia_solucao(entrada.df, entrada.contagem(entrada.df.columns))

print (entrada.regras(sol))