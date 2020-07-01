import re

# https://regex101.com/

# O que queremos encontrar?
variaveis = ['diam', 'setup']
declaradores = [r'\*set,', r'\*get,']
proibidos = ['/clear', 'eof', '/exit', r'\*ask']

# Monta pattern do Regex
# Une o que procuramos
pattVars = '|'.join(variaveis)
pattDecl = '|'.join(declaradores)
pattProib = '|'.join(proibidos)

# Declara o pattern
# O primeiro trecho ^[^!]* faz com que o código seja interpretado até encontrar algum ! (comentário em fortran90/ansys)
# O segundo  trecho ((?<=({0}))\s*({1})\s*(?=,)) considera comandos ALGO,VARIAVEL, 
# O terceiro trecho ((?<![a-zA-Z_0-9])\s*({1})\s*(?=[=+]))) considera variavel=
# O quarto   trecho ({2}) apenas procura por comandos que devem ser evitados (/clear, por exemplo)
rex = re.compile(r"^[^!]*(((?<=({0}))\s*({1})\s*(?=,))|((?<![a-zA-Z_0-9])\s*({1})\s*(?=[=+]))|({2}))".format(pattDecl, pattVars, pattProib), flags=re.IGNORECASE)

# Le arquivo original
with open('texto.txt', 'r') as f:
    txt = f.readlines()

# Salvando novo arquivo filtrado
with open('filtrado.txt', 'w') as f:
    for line in txt:
        # Se der algum match na linha torna ela um comentário
        if rex.search(line):
            f.write('! Line Removed by PARANSYS, old content: ')
        f.write(line)


"""
Catar linhas que já são comentários: a=3 !b=5
Ver o que acontece com /CLEAR
Remover /EXIT e EOF
"""
