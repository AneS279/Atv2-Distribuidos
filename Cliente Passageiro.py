from __future__ import print_function
import sys

if sys.version_info < (3, 0):
    input = raw_input


def visit(self, warehouse):
    print("This is {0}.".format(self.name))
    self.deposit(warehouse)
    self.retrieve(warehouse)
    print("Thank you, come again!")


def deposit(self, warehouse):
    print("The warehouse contains:", warehouse.list_contents())
    item = input("Type a thing you want to store (or empty): ").strip()
    if item:
        warehouse.store(self.name, item)

def consultaCarona(self, servidor):
    destino = input("Para onde deseja ir? ").strip()
    origem = input("Aonde está? ").strip()
    data = input("Quando deseja ir? ").strip()
    if origem and destino and data:
            servidor.consultaCarona(self, origem, destino, data)


def cadastroUsuario(self, servidor):
    print("Novo por aqui? Cadastre-se")
    nome = input("Qual seu nome? ").strip()
    telefone = input("Certo! \n Qual seu telefone? ").strip()
    if nome and telefone:
        servidor.cadastroCliente(self, nome, telefone, 9, 0)
