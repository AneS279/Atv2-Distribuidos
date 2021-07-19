from __future__ import print_function
import sys
from dataclasses import dataclass
import json
import Pyro4
import Pyro4.util
import rsa

sys.excepthook = Pyro4.util.excepthook

servidor = Pyro4.Proxy("PYRONAME:servidor.carona")


def consulta():
    destino = input("Para onde deseja ir? ").strip()
    origem = input("Aonde está? ").strip()
    data = input("Quando deseja ir? ").strip()

    if origem and destino and data:
        servidor.consultaCarona(origem, destino, data)
    interesse = input("Anotado! \n Deseja ser notificado quando houver uma carona disponível?\n 1 - SIM / 0 - NÃO").strip()


def cadastro ():
    print("Novo por aqui? Cadastre-se\n")
    nome = input("Qual seu nome? ").strip()
    telefone = input("Certo! \n Qual seu telefone? ").strip()
    senha = input("Insira uma senha: ").strip()
    key = rsa.key()
    f = open('mykey.pem', 'wb')
    (public_key, private_key) = rsa.newkeys(1024, accurate=True, poolsize=8)

    if nome and telefone:
        servidor.cadastroUsuario(nome, telefone, public_key, 1) #O ultimo campo - se 1 motorista, se 0 passageiro
        print(servidor.amostraALista())
#TODO
    #Registro de interesse em eventos (1,1)
    #Cancelamento de um registro de inte    resse (0,4)
    #Cada cliente tem um método para o recebimento de notificações de eventos do servidor (0,4)

escolha = ''
while escolha != 0:
    escolha = input("Olá, o que precisa hoje?\n "
    "1 - Cadastro \n"
    " 2 - Buscar viagem \n"
    " 0 - Sair\n").strip()
    cadastro() if escolha == '1' else consulta()
print("Até a próxima!")
