from __future__ import print_function
import Pyro4
from datetime import datetime
import Crypto
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pss


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
#
class Servidor(object):
    def __init__(self):
        self.Passageiro = []
        self.Motorista = []
        self.procuraPorPassageiro = []
        self.procuraPorCarona = []

        #########################################
        def mostraALista(self):
            return self.Motorista

    #########################################
    def consulta(self, origem, destino, data, tpUser):
        if tpUser == 1:
            listaDeViagens = self.procuraPorCarona
        else:
            listaDeViagens = self.procuraPorPassageiro
        print(listaDeViagens)
        for viagens in listaDeViagens:

            if viagens[4] == data and viagens[2] == origem and viagens[3] == destino:
                return viagens
        return 0

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
        self.procuraPorCarona.append([idCorrida, idUser, origem, destino, qtdepassageiros, data])
        return idCorrida
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

    def cancelarInteresseEmPassageiro(self, idCorrida):
        for i in range(0, len(self.procuraPorPassageiro)):
            if (self.procuraPorPassageiro[i][0] == idCorrida):
                self.procuraPorPassageiro.pop(i)

    def cancelarInteresseEmCarona(self, idCorrida):
        for i in range(0, len(self.procuraPorCarona)):
            if (self.procuraPorCarona[i][0] == idCorrida):
                self.procuraPorCarona.pop(i)
def main():
    Pyro4.Daemon.serveSimple(
        {
            Servidor: "servidor.carona"
        },
        ns=True)


if __name__ == "__main__":
    main()
