from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify
from datetime import datetime
app = Flask(__name__)
api = Api(app)

CORS(app)
@app.route("/")
def hello():
    return jsonify({'text':'Hello World!'})

class Servidor(Resource):
    clientes = {}
    Passageiro = []
    Motorista = []
    procuraPorPassageiro = []
    procuraPorCarona = []
    def get(self):
        return {'employees': [{'id':1, 'name':'Balram'},{'id':2, 'name':'Tom'}]}

    # def consultaUsuario(self, idUser, tpUser):
    #     if tpUser == 1:
    #         listaDeUsuario = self.Passageiro
    #     else:
    #         listaDeUsuario = self.Motorista
    #     print(listaDeUsuario)
    #     for usuario in listaDeUsuario:
    #         if usuario[0] == idUser:
    #             return usuario

class CadastroUsuario(Servidor):
    def post(self, nome, telefone, tpUser):
        if (tpUser == '1'):
            idUser = (len(Servidor.Motorista) + 1)
            Servidor.Motorista.append([idUser, nome, telefone])
            return idUser
        else:
            idUser = (len(Servidor.Passageiro) + 1)
            Servidor.Passageiro.append([idUser, nome, telefone])
            return idUser
class ConsultaViagens(Servidor):
       def consultaUsuario(self, idUser, tpUser):
        if tpUser == 0: #VOLTA PRA 1 DEPOIS
            listaDeUsuario = Servidor.Passageiro
        else:
            listaDeUsuario = Servidor.Motorista
        print(listaDeUsuario)
        for usuario in listaDeUsuario:
            if str(usuario[0]) == idUser:
                return usuario

       def get(self, origem, destino, data, tpUser):
            listaCompativeis =[]
            if tpUser == 0:#VOLTA PRA 1 DEPOIS
                listaDeViagens = Servidor.procuraPorCarona
            else:
                listaDeViagens = Servidor.procuraPorPassageiro
            print(tpUser," - ", listaDeViagens)
            for viagens in listaDeViagens:
                if viagens[4] == data and viagens[2] == origem and viagens[3] == destino:
                    usuarioCompativel = self.consultaUsuario(viagens[1], tpUser)
                    listaCompativeis.append(usuarioCompativel)
                    print(listaCompativeis)
            return listaCompativeis

class RemoveInteresseEmPassageiro(Servidor):
    def delete(self, idCorrida):
        for i in range(0, len(Servidor.procuraPorPassageiro)):
            if (Servidor.procuraPorPassageiro[i][0] == idCorrida):
                Servidor.procuraPorPassageiro.pop(i)
                return Servidor.procuraPorPassageiro

class InteresseEmPassageiro(Servidor):
    def post(self, idUser, origem, destino, data):
        id = datetime.now()
        id = str(id).replace(":", "")
        id = str(id).replace("-", "")
        id = str(id).replace(".", "")
        idCorrida = str(id).replace(" ", "")
        Servidor.procuraPorPassageiro.append([idCorrida, idUser, origem, destino, data])
        return idCorrida


api.add_resource(CadastroUsuario, '/servidor/cadastro/<nome>/<telefone>/<tpUser>')
api.add_resource(ConsultaViagens, '/servidor/consulta/<origem>/<destino>/<data>/<tpUser>')
api.add_resource(InteresseEmPassageiro, '/servidor/interesseEmPassageiro/<idUser>/<origem>/<destino>/<data>')
api.add_resource(RemoveInteresseEmPassageiro, '/servidor/removeInteresseEmPassageiro/<idCorrida>')



if __name__ == '__main__':
    app.run(port=5002)