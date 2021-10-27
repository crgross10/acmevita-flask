'''
* Cada departamento deve possuir um *nome do departamento*.
* A API deve responder com uma listagem de departamentos no formato JSON informando o *nome do departamento* de cada departamento.

#### Como um Usuário da API eu gostaria de consultar todos os colaboradores de um departamento para visualizar a organização da ACMEVita.

* Cada colaborador deve possuir um *nome completo*.
* Cada colaborador deve pertencer a *um* departamento.
* Cada colaborador pode possuir *nenhum, um ou mais* dependententes.
* A API deve responder com uma listagem de colaboradores do departamento no formato JSON informando o *nome completo* de cada colaborador e
a respectiva flag booleana `have_dependents` caso o colaborador possua *um ou mais dependentes*.
''']

from flask import Flask, request
from flask_restful import Resource, Api
from models import Departamentos, Colaboradores, Dependentes

app = Flask(__name__)
api = Api(app)


class Departamento(Resource):
    def get(self):
        departamentos = Departamentos.query.all()
        response = [{'id':i.id, 'departamento':i.departamento}  for i in departamentos]
        return response

class ListaColaboradoresDepartamento(Resource):
    def get(self,id_departamento):
        colaboradores_dic = {}
        departamento = Departamentos.query.filter_by(id=id_departamento)
        for i in departamento:
             departamento_id = i.id
             departamento_nome = i.departamento

        dependentes = Dependentes.query.all()
        colaboradores = Colaboradores.query.filter_by(departamento_id=departamento_id)
        count = 0
        for c in colaboradores:
            count=count+1
            id_colaborador = c.id
            colaborador = c.nome_completo
            if  len(list(Dependentes.query.filter_by(colaborador_id = id_colaborador))) > 0:
                have_dependents = True
            else:
                have_dependents = False

            colaboradores_dic.update({ count: {'id':id_colaborador, 'colaborador':colaborador, 'have_dependents':have_dependents}})


        response = [{departamento_nome:colaboradores_dic}]
        return response


api.add_resource(Departamento, '/departamentos/')
api.add_resource(ListaColaboradoresDepartamento, '/colaboradores_departamento/<int:id_departamento>/')

if __name__ == '__main__':
    app.run(debug=True)
