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
sys.excepthook = Pyro4.util.excepthook

servidor = Pyro4.Proxy("PYRONAME:servidor.carona")

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
    destino = input("Para onde deseja ir? ").strip().encode()
    origem = input("Aonde está? ").strip().encode()
    data = input("Quando deseja ir? ").strip().encode()
    if origem and destino and data:
        respConsulta = servidor.consulta(origem, destino, data, 1)
        if(not(respConsulta)):
            adicionarALista = input(
                "Não encontrei nada dese|ja adicionar a sua lista de interesse? 1 - SIM/ 0 - NÃO\n").strip()
            interesse(data, origem, idUser, destino) if adicionarALista == '1' else print('Tudo bem! Nos vemos na próxima\n')

    # Registro de interesse em eventos (1,1)
def interesse(data, origem, idUser, destino):
    encoded = str(idUser)
    idUserEncoded = SHA256.new(encoded.encode('utf-8'))
    print(idUserEncoded)
    private = RSA.import_key(open('privateMotorista.pem').read())
    signature = pss.new(private).sign(idUserEncoded)
    sig_results = open("signature.txt", "wb")
    sig_results.write(signature)
    sig_results.close()
    print(binascii.hexlify(signature))
    id = servidor.interesseEmCarona(idUser, origem, destino, data, signature)
def cadastro ():
    print("Novo por aqui? Cadastre-se\n")
    nome = input("Qual seu nome? ").strip().encode()
    telefone = input("Certo! \n Qual seu telefone?").strip().encode()
    encryptor = PKCS1_OAEP.new(key)
    nome = encryptor.encrypt(nome)
    telefone = encryptor.encrypt(telefone)
    if nome and telefone:
        idUser = servidor.cadastroUsuario(nome, telefone, publickey, 1) #O ultimo campo - se 1 motorista, se 0 passageiro
        print(idUser)
    return idUser
def removeInteresse(idUser):
    print(idUser)
    viagensMarcadas = servidor.viagensRelacionadasAoMotorista(idUser)
    if(not(viagensMarcadas)):
        print("Não encontrei nenhuma viagem agendada para você.")
    else:
        print("Encontrei essas viagens para você, digite o número correspondente a que deseja cancelar")
        for i in range (0, viagensMarcadas):
            print(i, " - ", viagensMarcadas[i])
        remover = input("Digite o número da viagem que deseja remover").strip()
        servidor.cancelarInteresseEmViagem(idUser, viagensMarcadas[remover][0])
#TODO

#Cancelamento de um registro de interesse (0,4)
#Cada cliente tem um método para o recebimento de notificações de eventos do servidor (0,4)


def main():

    escolha = ''
    idUser = ''
    while escolha != '0':
        escolha = input("Olá, o que precisa hoje?\n "
                        "1 - Cadastro \n"
                        "2 - Buscar viagem \n"
                        "0 - Sair\n").strip()
        if escolha != '0':
            if escolha == '1':
                idUser = cadastro()
            elif escolha == '2':
                consulta(idUser)
            else:
                removeInteresse(idUser)
    print("Até a próxima!")


if __name__ == "__main__":
    main()