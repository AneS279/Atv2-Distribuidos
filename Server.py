from __future__ import print_function
import Pyro4



@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
#
class Servidor(object):
    def __init__(self):
        self.Passageiro = []
        self.Motorista = []
        self.procuraPassageiro = []
        self.procuraCarona = []
#########################################
    def amostraALista(self):
        return self.Motorista
#########################################

    # Clientes devem informar a origem, destino e a data da viagem desejada. (0,3)
    def consultaCaronas(self, origem, destino, data):
        id = procuraCarona
        self.procuraCarona.append(origem, destino, data)

    def consultaPassegeiro(self, origem, destino, data):
        self.procuraPassageiro.append(origem, destino, data)

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
