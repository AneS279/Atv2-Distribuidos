from flask import Flask, Response, render_template, stream_with_context, request
from flask import Flask, render_template
from flask_sse import sse
from apscheduler.schedulers.background import BackgroundScheduler
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify
from datetime import datetime
import json
import time
import logging
import os

app = Flask(__name__)
api = Api(app)
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix='/stream')


CORS(app)
@app.route('/')
def index():
    return jsonify(get_data())

class Servidor(Resource):
    clientes = {}
    Passageiro = []
    Motorista = []
    procuraPorPassageiro = []
    procuraPorCarona = []
    tamanhoFilaPassageiro = 0
    def get(self):
        return {'employees': [{'id':1, 'name':'Balram'},{'id':2, 'name':'Tom'}]}

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

class ConsultaViagensDoUsuario(Servidor):
    def get(self, idUser, tpUser):
        viagens = []
        if tpUser == '1':
            listaDeUsuario = Servidor.procuraPorPassageiro
        else:
            listaDeUsuario = Servidor.procuraPorCarona
        print(listaDeUsuario)
        for usuario in listaDeUsuario:
            if str(usuario[1]) == idUser:
                viagens.append(usuario)
        return viagens

class ConsultaViagens(Servidor):
    def consultaUsuario(self, idUser, tpUser):
        if tpUser == '1':
            listaDeUsuario = Servidor.Passageiro
        else:
            listaDeUsuario = Servidor.Motorista
        print(listaDeUsuario)
        for usuario in listaDeUsuario:
            if str(usuario[0]) == idUser:
                # server_side_event(usuario, idUser)
                return usuario

    def get(self, origem, destino, data, tpUser):
        listaCompativeis =[]
        if tpUser == '1':#VOLTA PRA 1 DEPOIS
            listaDeViagens = Servidor.procuraPorCarona
        else:
            listaDeViagens = Servidor.procuraPorPassageiro
        for viagens in listaDeViagens:
            if viagens[4] == data and viagens[2] == origem and viagens[3] == destino:
                usuarioCompativel = self.consultaUsuario(viagens[1], tpUser)
                listaCompativeis.append([usuarioCompativel, viagens])
                print(listaCompativeis)
            return listaCompativeis

class RemoveInteresseEmPassageiro(Servidor):
    def delete(self, idCorrida):
        for i in range(0, len(Servidor.procuraPorPassageiro)):
            if (Servidor.procuraPorPassageiro[i][0] == idCorrida):
                Servidor.procuraPorPassageiro.pop(i)
                return Servidor.procuraPorPassageiro

class RemoveInteresseEmCarona(Servidor):
    def delete(self, idCorrida):
        for i in range(0, len(Servidor.procuraPorCarona)):
            if (Servidor.procuraPorCarona[i][0] == idCorrida):
                Servidor.procuraPorCarona.pop(i)
                return Servidor.procuraPorCarona

class InteresseEmPassageiro(Servidor):
    def post(self, idUser, origem, destino, data):
        id = datetime.now()
        id = str(id).replace(":", "")
        id = str(id).replace("-", "")
        id = str(id).replace(".", "")
        idCorrida = str(id).replace(" ", "")
        Servidor.procuraPorPassageiro.append([idCorrida, idUser, origem, destino, data])
        # escutaMotorista(origem, destino, data)
        # server_side_event(Servidor.procuraPorPassageiro)
        return idCorrida

class InteresseEmCarona(Servidor):
    def post(self, idUser, origem, destino, data, qtdePassageiros):
        id = datetime.now()
        id = str(id).replace(":", "")
        id = str(id).replace("-", "")
        id = str(id).replace(".", "")
        idCorrida = str(id).replace(" ", "")
        Servidor.procuraPorCarona.append([idCorrida, idUser, origem, destino, data, qtdePassageiros])
        print(Servidor.procuraPorCarona)
        # escutaMotorista(origem, destino, data)
        return idCorrida

class TamanhoLista(Servidor):
    def get(self, tpUser):
        if tpUser == '0':
            listaDeViagens = Servidor.procuraPorCarona
        else:
            listaDeViagens = Servidor.procuraPorPassageiro
        return len(listaDeViagens) + 1

CORS(app)

# def escutaMotorista(origem, destino, data):
#     def respond_to_client():
#         yield f"id: 1\ndata: {data}\nevent: online\n\n"
#         if(len(Servidor.procuraPorPassageiro) != Servidor.tamanhoFilaPassageiro):
#             Servidor.tamanhoFilaPassageir = len(Servidor.procuraPorPassageiro)
#             disponiveis = ConsultaViagens.get(ConsultaViagens,origem,destino,data,1)
#             return disponiveis
#     return Response(respond_to_client(), mimetype='text/event-stream')
# @app.route("/listen/<origem>/<destino>/<data>")

def server_side_eventMotorista(lista, id):
    """ Function to publish server side event """
    with app.app_context():
        sse.publish(lista, type='publish', channel=str(id))
        print(sse.redis)
        print("FUNCIONA POR FAVOOOOOOOOOR")




api.add_resource(CadastroUsuario, '/servidor/cadastro/<nome>/<telefone>/<tpUser>')
api.add_resource(ConsultaViagens, '/servidor/consulta/<origem>/<destino>/<data>/<tpUser>')
api.add_resource(InteresseEmPassageiro, '/servidor/interesseEmPassageiro/<idUser>/<origem>/<destino>/<data>')
api.add_resource(InteresseEmCarona, '/servidor/interesseEmCarona/<idUser>/<origem>/<destino>/<data>/<qtdePassageiros>')
api.add_resource(RemoveInteresseEmPassageiro, '/servidor/removeInteresseEmPassageiro/<idCorrida>')
api.add_resource(RemoveInteresseEmCarona, '/servidor/RemoveInteresseEmCarona/<idCorrida>')
api.add_resource(TamanhoLista, '/servidor/TamanhoLista/<tpUser>')
api.add_resource(ConsultaViagensDoUsuario, '/servidor/consultaViagensDoUsuario/<idUser>/<tpUser>')



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)