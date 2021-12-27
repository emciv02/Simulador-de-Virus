#%%

import turtle
import random
import math
import time
import matplotlib.pyplot as plt

# Aluna Victória C. de Medeiros

# Variáveis iniciais

# Número de pessoas na simulação
numero_pessoas = 150

# Número de pessoas inicialmente contaminadas
ini_contaminadas = 10

# Agressividade do vírus, 30%
agressividade_virus = 3

# Duração da imunidade, 52 semanas/iterações
duracao_imunidade = 52

# Auxilia na contagem do estado dos indivíduos
contaminados = 0
imunes = 0
mortos = 0

# Variável tempo para o gráfico
tempo = 0

# Lista que vai armazenar os objetos de cada pessoa
pessoas = []

# Dicionário que mantém o controle dos estados de cada pessoa
tabela_geral = {'contaminado':[], 'imune':[], 'morto':[]}

class Pessoa:
    ''' Classe que define os atributos que cada pessoa tem.'''
    def __init__(self, t, imagem, tamanho):
        
        # Cria a pessoa
        self.imagem = imagem
        self.tamanho = tamanho
        self.t = t

        # Gera posição aleatória
        self.posicaox = random.randint(-230,230)
        self.posicaoy = random.randint(-210,210)

        # Idade da pessoa
        self.idade = random.uniform(0, 50)

        # Verifica se tá morto
        self.morta = False

        #Verifica se tá imune
        self.imune = False

        # Tempo que a pessoa está infectada
        self.tempo = 0

        # Duração total da infecção, cada pessoa tem um tempo aleatório
        self.tempo_infec = random.randint(0, 5) # Tem que ser 100

        # Tempo que a pessoa está imune
        self.tempo_imune = 0

        # Chance que cada pessoa tem de reproduzir outra pessoa
        self.reproduzir = random.randint(1, 100)

    def desenha_pessoa(self):
        '''Cria o turtle da pessoa'''
        self.t.penup()
        self.t.shape(self.imagem)
        self.t.setpos(self.posicaox, self.posicaoy)

    def update(self):
        '''Movimenta pessoa:'''
        self.t.penup()
        self.t.right(random.randint(-50,50))
        if(self.morta == False):
            self.t.forward(5)
        else:
            self.t.forward(0)
        self.t.speed(0)
        if(self.t.xcor() > 230 or self.t.xcor() < -230):
            heading = self.t.heading() # 0 ou 180
            self.t.setheading(180 - heading) # Volta 180 ou 0              
        elif(self.t.ycor() > 210 or self.t.ycor() < -210):
            heading = self.t.heading() # 90 ou 270 
            self.t.setheading(heading - 270) #Volta 180 ou 0 
        
def configura_tela():
    ''' Realiza a configuração do display. '''
    screen = turtle.Screen()
    screen.setup(500,500)
    screen.bgcolor("black")
    screen.title("Infection simulation")
    screen.addshape('pgreen.gif')
    screen.addshape('pred.gif')
    screen.addshape('pgray.gif')
    screen.addshape('ghost.gif')
                            
def contamina_pessoa(lista_pessoas, contador_contaminados):
    ''' Faz a lógica de contaminação de pessoas.'''
    lista_pessoas[j].imagem = 'pred.gif' # O indice 'j' deve ser passado como argumento da função. Dessa forma funciona, contudo não é recomendado fazer assim.
    lista_pessoas[j].desenha_pessoa()
    tabela_geral['contaminado'][j] = True
    tabela_geral['imune'][j] = False
    tabela_geral['morto'][j] = False
    contador_contaminados += 1

def mata_pessoa(lista_pessoas, contador_morte, contador_contaminado):
    ''' Faz a lógica de morte de pessoas.'''
    lista_pessoas[j].imagem = 'ghost.gif'
    lista_pessoas[j].desenha_pessoa()
    lista_pessoas[j].t.hideturtle() # Se comentar, aparece os mortos.
    lista_pessoas[j].morta = True                            
    tabela_geral['morto'][j] = True
    tabela_geral['contaminado'][j] = False                                                        
    tabela_geral['imune'][j] = False
    contador_morte += 1  
    contador_contaminado -= 1

def imuniza_pessoa(lista_pessoas, contador_imune, contador_contaminado):
    ''' Faz a lógica de imunização de pessoas.'''
    lista_pessoas[j].imagem = 'pgray.gif'                                    
    lista_pessoas[j].desenha_pessoa()
    lista_pessoas[j].imune = True
    tabela_geral['imune'][j] = True
    tabela_geral['contaminado'][j] = False
    tabela_geral['morto'][j] = False
    contador_imune += 1
    contador_contaminado -= 1

def fim_imunidade(lista_pessoa):
    ''' Faz a lógica do término da imunidade.'''
    lista_pessoa[j].imagem = 'pgreen.gif' # Significa que perdeu a imunidade                                   
    lista_pessoa[j].desenha_pessoa() 
    tabela_geral['imune'][j] == False
    tabela_geral['contaminado'][j] = False
    tabela_geral['morto'][j] = False
    lista_pessoa[j].imune = False

def plota_grafico(x, y1, y2, y3):
    ''' Plota o gráfico.'''   
    plt.plot(x, y1, "red", label = "Doentes")
    plt.plot(x, y2, "blue", label = "Imunes")
    plt.plot(x, y3, "black", label = "Mortos")
    #plt.plot(x, y4, "green", label = "Saudaveis" ) # Comentei apenas para aparecer melhor os outros no gráfico.
    plt.xlabel('Semanas')
    plt.ylabel('Número de pessoas')

# Dicionário que vai armazenar informações para a construção do gráfico
grafico = {"tempo": [],
           "doentes": [],
           "imunes": [],
           "mortos":[],
           "saudaveis": []
           }

# Variável usada para pegar as informações do gráfico, serve como um intervalo.
pausa = 1

configura_tela()

turtle.reset()
turtle.tracer(0,0)
turtle.hideturtle()

# Define as pessoas saudáveis
for i in range(numero_pessoas-ini_contaminadas):
    tabela_geral['contaminado'].append(False)

for i in range(numero_pessoas):

    # Adiciona o objeto de cada pessoa inicialmente contaminada na lista de pessoas.
    for i in range(ini_contaminadas):
        pessoas.append(Pessoa(t = turtle.Turtle(), imagem ='pred.gif', tamanho = (0.3, 0,3)))
        tabela_geral['contaminado'].append(True)
        pessoas[i].desenha_pessoa()
        contaminados += 1
        pessoas[i].tempo += 1
    
    # Adiciona o objeto de cada pessoa que não está contaminada na lista de pessoas.
    for i in range(numero_pessoas):
        pessoas.append(Pessoa(t = turtle.Turtle(), imagem ='pgreen.gif', tamanho = (0.3, 0,3)))
        tabela_geral['contaminado'].append(False)
        tabela_geral['imune'].append(False)
        tabela_geral['morto'].append(False)
        pessoas[i].desenha_pessoa()    
    

    # Aqui começa a lógica para a contaminação, imunidade e morte.
    
    while True:

        tempo += 1 # Seria o eixo X do gráfico

        # Faz as pessoas aparecerem juntas na tela.
        turtle.reset()
        turtle.tracer(0,0)
        turtle.hideturtle()

        # Faz cada pessoa/ objeto se mover.
        for pessoa in pessoas:
            pessoa.update()
            
        for i in range(numero_pessoas):

            # Incrementa idade de cada pessoa, a cada 52 iterações, passou 1 ano, soma 1 na idade
            pessoas[i].idade += 0.01923
            
            # Taxa de reprodução do modelo 
            if ((pessoas[i].reproduzir == 1) and (tabela_geral['contaminado'][i] == False) and (len(pessoas) <= 300)):
                pessoas.append(Pessoa(t = turtle.Turtle(), imagem ='pgreen.gif', tamanho = (0.3, 0,3)))
                pessoa.desenha_pessoa()
                pessoas[i].idade = 0

            # Define [i] como pessoa contaminada
            if(tabela_geral['contaminado'][i] == True):
                
                # Define [j] como pessoa saudavel
                for j in range(numero_pessoas):
                    
                    # É a probabilidade de morrer se pegar o vírus
                    chance_morte = random.random()  

                    # Não comparar mesma pessoa
                    if (i != j):
                        
                        # Analisa distância de pessoa saudavel[j] a uma pessoa contaminada[i]
                        if (math.sqrt((pessoas[i].t.xcor() - pessoas[j].t.xcor())**2) + ((pessoas[i].t.ycor() - pessoas[j].t.ycor())**2) <= 10):
                            
                            # Probabilidade da pessoa se contaminar quando tiver contato com alguém contaminado
                            chance_contaminacao = random.randint(1,10)                   

                            # Contamina uma pessoa saudavel
                            if (chance_contaminacao <= agressividade_virus and tabela_geral['imune'][j] != True and tabela_geral['morto'][j] != True):
                                contamina_pessoa(pessoas, contaminados)
                            
                            if tabela_geral['contaminado'][j] == True:
                                # Conta as semanas que a pessoa fica infectada
                                pessoas[j].tempo += 1          

                            # Verifica se a pessoa morre
                            if (((chance_morte <= 0.1 and tabela_geral['contaminado'][j] == True and pessoas[j].tempo <= pessoas[j].tempo_infec)) or (pessoas[j].idade >= 50)):
                                mata_pessoa(pessoas, mortos, contaminados)                                                         

                            # Verifica se a pessoa vai ficar imune
                            if (pessoas[j].tempo > pessoas[j].tempo_infec and tabela_geral['contaminado'][j] == True): # Se o tempo em que a pessoa está infectada for maior que o tempo que uma pessoa fica com o vírus até se recuperar, e ela não morrer, significa que ficou imune
                                imuniza_pessoa(pessoas, imunes, contaminados)

                            # Faz o controle do tempo de imunidade da pessoa
                            if (pessoas[j].imune == True):
                                # Conta os dias de imunidade
                                pessoas[j].tempo_imune += 1 
  
                            # Fim da imunidade depois de 1 ano/52 iterações
                            if (pessoas[j].imune == True and pessoas[j].tempo_imune >= duracao_imunidade): 
                                fim_imunidade(pessoas)   

        # A partir daqui começa a lógica para o gráfico

        # A cada 10 iterações os dados do gráfico são atualizados
        if int(tempo) == pausa:
            pausa += 10
            grafico["tempo"].append(tempo)
            grafico["doentes"].append(tabela_geral["contaminado"].count(True))
            grafico["mortos"].append(tabela_geral["morto"].count(True))
            grafico["imunes"].append(tabela_geral["imune"].count(True))
            #grafico["saudaveis"].append((len(pessoas)-(tabela_geral["contaminado"].count(True))-(tabela_geral["morto"].count(True))))

        plota_grafico(grafico["tempo"], grafico["doentes"],grafico["imunes"], grafico["mortos"])

        # Controla a velocidade de movimentação das pessoas                                                
        time.sleep(0.01)
        turtle.update()

plt.show()

# %%
