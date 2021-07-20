from __future__ import print_function
import Pyro4
from datetime import datetime
import Crypto
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
#
class Servidor(object):
    def __init__(self):
        self.Passageiro = []
        self.Motorista = []
        self.procuraPassageiro = []
        self.procuraMotorista = []
#########################################
        def amostraALista(self):
            return self.Motorista
#########################################
    def interesseMotorista(self, idUser, origem, destino, data, signature):
        id = datetime.now()
        id = str(id).replace(":", "")
        id = str(id).replace("-", "")
        id = str(id).replace(".", "")
        idCorrida = str(id).replace(" ", "")

        for motorista in self.Motorista:
            if motorista[0] == idUser:
                encoded = str(idUser)
                h = SHA256.new(encoded.encode())
                publicKey = motorista[3]
                try:
                    pkcs1_15.new(publicKey).verify(h, signature)
                    self.procuraPassageiro.append(idCorrida,idUser, origem, destino, data, signature)
                    return idCorrida
                except (ValueError, TypeError):
                    print("A assinatura é inválida :(")

    # Clientes devem informar a origem, destino e a data da viagem desejada. (0,3)
    def consultaMotorista(self, origem, destino, data):
        for viagens in self.procuraPassageiro:
            if viagens[data] == data and viagens[origem] == origem and viagens[destino] == destino:
                return "Encontrei a viagem " + viagens
        return 0
    def consultaPassageiro(self, origem, destino, data):
        self.procuraPassageiro.append(origem, destino, data)
        for viagens in self.procuraMotorista:
            if viagens[data] == data:
                print("Hey, aqui estou")

    # Clientes devem informar seu nome, telefone e chave pública. (0,2)
    def cadastroUsuario(self, nome, telefone, publicKey, tpUser):
        if (tpUser == 1):
            idUser = (len(self.Motorista) + 1)
            self.Motorista.append([idUser,nome, telefone, publicKey])
            return idUser
        else:
            self.Passageiro.append([nome, telefone, publicKey])

def main():
    Pyro4.Daemon.serveSimple(
        {
            Servidor: "servidor.carona"
        },
        ns=True)


if __name__ == "__main__":
    main()
