from __future__ import print_function
import Pyro4
from datetime import datetime
import Crypto
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pss


@Pyro4.behavior(instance_mode="single")
#
class Servidor(object):
    def __init__(self):
        self.clientes = {}
        self.Passageiro = []
        self.Motorista = []
        self.procuraPorPassageiro = []
        self.procuraPorCarona = []

    def clientesAtivos(self):
        return list(self.clientes.keys())
        #########################################
    def consultaUsuario(self, idUser, tpUser):
        if tpUser == 1:
            listaDeUsuario = self.Passageiro
        else:
            listaDeUsuario = self.Motorista
        print(listaDeUsuario)
        for usuario in listaDeUsuario:
            if usuario[0] == idUser:
                return usuario

    @Pyro4.expose
    #########################################
    def consultaViagens(self, origem, destino, data, tpUser):
        listaCompativeis =[]
        if tpUser == 1:
            listaDeViagens = self.procuraPorCarona
        else:
            listaDeViagens = self.procuraPorPassageiro
        print(tpUser," - ", listaDeViagens)
        for viagens in listaDeViagens:
            if viagens[4] == data and viagens[2] == origem and viagens[3] == destino:
                usuarioCompativel = self.consultaUsuario(viagens[1], tpUser)
                listaCompativeis.append(usuarioCompativel)
        return listaCompativeis

    @Pyro4.expose
    # Clientes devem informar a origem, destino e a data da viagem desejada. (0,3)
    def cadastroUsuario(self, nome, telefone, publicKey, tpUser):
        if (tpUser == 1):
            idUser = (len(self.Motorista) + 1)
            self.Motorista.append([idUser, nome, telefone, publicKey])
            return idUser
        else:
            idUser = (len(self.Passageiro) + 1)
            self.Passageiro.append([idUser, nome, telefone, publicKey])
            return idUser


    def notificaMotorista (self, origem, destino, data):
        for viagens in self.procuraPorPassageiro:
            if viagens[4] == data and viagens[2] == origem and viagens[3] == destino:
                notifica

    @Pyro4.expose
    #Clientes devem informar seu nome, telefone e chave pública. (0,2)
    def interesseEmCarona(self, idUser, origem, destino, data, qtdepassageiros, signature):
        id = datetime.now()
        id = str(id).replace(":", "")
        id = str(id).replace("-", "")
        id = str(id).replace(".", "")
        idCorrida = str(id).replace(" ", "")
        encoded = str(idUser)
        idUserEncoded = SHA256.new(encoded.encode('utf-8'))
        public_key = RSA.import_key(open('publicPassageiro.pem').read())
        #pss.new(public_key).verify(idUserEncoded, signature)
        self.procuraPorCarona.append([idCorrida, idUser, origem, destino, data, qtdepassageiros])
        self.notificaMotorista(origem, destino, data)
        return idCorrida

    @Pyro4.expose
    def interesseEmPassageiro(self, idUser, origem, destino, data, signature):
        id = datetime.now()
        id = str(id).replace(":", "")
        id = str(id).replace("-", "")
        id = str(id).replace(".", "")
        idCorrida = str(id).replace(" ", "")
        encoded = str(idUser)
        idUserEncoded = SHA256.new(encoded.encode('utf-8'))
        public_key = RSA.import_key(open('publicMotorista.pem').read())
        #pss.new(public_key).verify(idUserEncoded, signature)
        self.procuraPorPassageiro.append([idCorrida, idUser, origem, destino, data])
        return idCorrida

    @Pyro4.expose
    def cancelarInteresseEmPassageiro(self, idCorrida):
        for i in range(0, len(self.procuraPorPassageiro)):
            if (self.procuraPorPassageiro[i][0] == idCorrida):
                self.procuraPorPassageiro.pop(i)

    @Pyro4.expose
    def cancelarInteresseEmCarona(self, idCorrida):
        for i in range(0, len(self.procuraPorCarona)):
            if (self.procuraPorCarona[i][0] == idCorrida):
                self.procuraPorCarona.pop(i)
def main():
    daemon = Pyro4.Daemon()
    uri = daemon.register(Servidor)
    print(uri)
    ns = Pyro4.locateNS()
    ns.register("servidor.carona", uri)
    daemon.requestLoop()
#####
#daemon = Pyro4.Daemon()
#uri = daemon.register(MyPyroThing)
#print(uri)
#daemon.requestLoop()
#uri = daemon.register(some_object)
#ns = Pyro4.locateNS()
#ns.register("example.objectname", uri)
#https://pyro4.readthedocs.io/en/stable/servercode.html
#https://pyro4.readthedocs.io/en/stable/clientcode.html
#
#
#
#
if __name__ == "__main__":
    main()
