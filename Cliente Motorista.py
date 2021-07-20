from __future__ import print_function
import sys
from dataclasses import dataclass
import json
import Pyro4
import Pyro4.util
import rsa
import Crypto
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP

sys.excepthook = Pyro4.util.excepthook

servidor = Pyro4.Proxy("PYRONAME:servidor.carona")

key = RSA.generate(2048)

privatekey = key.export_key()
publickey = key.publickey().export_key()

def consulta():
    destino = input("Para onde deseja ir? ").strip()
    origem = input("Aonde está? ").strip()
    data = input("Quando deseja ir? ").strip()
    interesse = input(
        "Anotado! \n Deseja ser notificado quando houver uma carona disponível?\n 1 - SIM / 0 - NÃO").strip()

    if origem and destino and data:
        if interesse != '0':
            hashA = SHA256.new(True_text.encode('utf - 8')).digest()
            digitalSign = keyPair.sign(hashA, '')
            id = servidor.consultaMotorista(origem, destino, data, interesse)
            print(id)

    # Registro de interesse em eventos (1,1)


def cadastro ():
    print("Novo por aqui? Cadastre-se\n")
    nome = input("Qual seu nome? ").strip().encode()
    telefone = input("Certo! \n Qual seu telefone?").strip().encode()
    encryptor = PKCS1_OAEP.new(key)
    nome = encryptor.encrypt(nome)
    telefone = encryptor.encrypt(telefone)
    if nome and telefone:
        servidor.cadastroUsuario(nome, telefone, publickey, 1) #O ultimo campo - se 1 motorista, se 0 passageiro

#TODO

#Cancelamento de um registro de interesse (0,4)
#Cada cliente tem um método para o recebimento de notificações de eventos do servidor (0,4)

escolha = ''
while escolha != '0':
    escolha = input("Olá, o que precisa hoje?\n "
                    "1 - Cadastro \n"
                    " 2 - Buscar viagem \n"
                    " 0 - Sair\n").strip()
    if escolha != '0':
        cadastro() if escolha == '1' else consulta()
print("Até a próxima!")
