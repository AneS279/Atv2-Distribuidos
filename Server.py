from __future__ import print_function
import Pyro4
from datetime import datetime


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

    # Clientes devem informar a origem, destino e a data da viagem desejada. (0,3)
    def consultaMotorista(self, origem, destino, data, interesse):
        if interesse != '0':
            id = datetime.now()
            id = str(id).replace(":", "")
            id = str(id).replace("-", "")
            id = str(id).replace(".", "")
            id = str(id).replace(" ", "")
        else:
            id = 0
        self.procuraMotorista.append([id, origem, destino, data])
        for viagens in self.procuraPassageiro:
            if viagens[data] == data:
                print("Hey, aqui estou")
        return id

    def consultaPassegeiro(self, origem, destino, data):
        self.procuraPassageiro.append(origem, destino, data)
        for viagens in self.procuraMotorista:
            if viagens[data] == data:
                print("Hey, aqui estou")

    # Clientes devem informar seu nome, telefone e chave pública. (0,2)
    def cadastroUsuario(self, nome, telefone, publicKey, idUser):
        if (idUser == 1):
            self.Motorista.append([nome, telefone, publicKey])
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
