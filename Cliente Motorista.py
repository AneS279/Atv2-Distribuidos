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
from Crypto.Signature import pss
import binascii
import asyncio
sys.excepthook = Pyro4.util.excepthook

nameserver = Pyro4.locateNS()
uri = nameserver.lookup("servidor.carona")
servidor = Pyro4.Proxy(uri)

key = RSA.generate(2048)
privatekey = key.export_key()
file_out = open("privateMotorista.pem", "wb")
file_out.write(privatekey)
file_out.close()

publickey = key.publickey().export_key()
file_out = open("publicMotorista.pem", "wb")
file_out.write(publickey)
file_out.close()

def consulta(idUser):
    if(not(idUser)):
        print("Antes de agendar a viagem, precisamos de um cadastro!\n")
        idUser = cadastro()
    destino = input("Para onde deseja ir? ").strip()
    origem = input("Aonde está? ").strip()
    data = input("Quando deseja ir? ").strip()
    if origem and destino and data:
        respConsulta = servidor.consultaViagens(origem, destino, data, 1)
        idCorrida = interesse(data, origem, idUser, destino)
        if (len(respConsulta) == 0):
            adicionarALista = input(
                "Não encontrei nada deseja adicionar a sua lista de interesse? 1 - SIM/ 0 - NÃO\n").strip()
            if adicionarALista == '0':
                print('Tudo bem! Nos vemos na próxima\n')
                servidor.cancelarInteresseEmPassageiro(idCorrida)
            else:
                print("Ok! Esse é seu ID: ", idCorrida)
                #servidor.notificaMotorista(origem, destino, data)
            #    asyncio.run(notificaMotorista(idUser, data, origem, destino))
        else:
            servidor.cancelarInteresseEmPassageiro(idCorrida)
            print("Encontrei ", len(respConsulta), "\n")
            for i in respConsulta:
                print("Nome: ", i[1], "\n",
                      "Telefone: ", i[2],
                      "\n __________________________ \n")
    # Registro de interesse em eventos (1,1)
def interesse(data, origem, idUser, destino):
    print(data)
    encoded = str(idUser)
    idUserEncoded = SHA256.new(encoded.encode('utf-8'))
    private = RSA.import_key(open('privateMotorista.pem').read())
    signature = pss.new(private).sign(idUserEncoded)
    id = servidor.interesseEmPassageiro(idUser, origem, destino, data, signature)
    return id
def cadastro ():
    print("Novo por aqui? Cadastre-se\n")
    nome = input("Qual seu nome? ").strip()
    telefone = input("Certo! \n Qual seu telefone?").strip()
    if nome and telefone:
        idUser = servidor.cadastroUsuario(nome, telefone, publickey, 1) #O ultimo campo - se 1 motorista, se 0 passageiro
    return idUser
def removeInteresse(idUser):
    remover = input("Digite o número da viagem que deseja remover").strip()
    servidor.cancelarInteresseEmPassageiro(remover)
    print("Feito! Nos vemos na próxima!\n")

@Pyro4.expose
def notificaMotorista(idUser, data, origem, destino):
    servidor._pyroAsync()
    asyncresult = servidor.consulta(origem, destino, data, 1)
    while True:
        viagens = servidor.consulta(origem, destino, data, 1)
        print(viagens)
        if viagens != 0:
            return "AAEEEEEE"
        await asyncio.sleep(1)

def main():

    escolha = ''
    idUser = ''
    while escolha != '0':
        escolha = input("Olá, o que precisa hoje?\n "
                        "1 - Cadastro \n"
                        "2 - Buscar viagem \n"
                        "0 - Sair\n").strip()
        if escolha != '0':
            if escolha == '1' and idUser == '':
                idUser = cadastro()
            elif escolha == '2':
                consulta(idUser)
            elif escolha == '3':
                removeInteresse(idUser)
    print("Até a próxima!")


if __name__ == "__main__":
    main()