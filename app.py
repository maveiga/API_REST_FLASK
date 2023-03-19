#import pip install Flask Flask-SQLAlchemy mysqlclient

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost:3306/youtube' #conexão
db = SQLAlchemy(app)


class Clientes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    email=db.Column(db.String(150),nullable=False)

#busca todos os clientes
@app.route('/clientes', methods=['GET'])
def busca_clientes():
    clientes =Clientes.query.all()
    lista=[]
    for cliente in clientes:
        dados={'id':cliente.id,'nome':cliente.nome,'email':cliente.email}
        lista.append(dados)
    return jsonify({'clientes':lista})

#busca de um cliente por id
@app.route('/clientes/<cliente_id>', methods=['GET'])
def busca_id(cliente_id):
    cliente=Clientes.query.get_or_404(cliente_id)
    return jsonify({'id':cliente.id,'nome':cliente.nome,'email':cliente.email})
    
#inserindo cliente        
@app.route('/clientes', methods=['POST'])
def inserir_clientes():
    nome=request.json['nome']
    email=request.json['email']
    #faz a validação se existe o email na base
    if Clientes.query.filter_by(email=email).first() is not None:
        return jsonify({'error': 'O email já existe no banco de dados!'}), 409  # 409 é o código de erro para "Conflito"
    cliente=Clientes(nome=nome, email=email)
    db.session.add(cliente)        
    db.session.commit()
    #tratamento de erro
    try: 
        return jsonify({'message':'cliente criado com sucesso'})
    except:
        return jsonify({'message':'erro interno no servidor'})
   
 #atualizando cliente   
@app.route('/clientes/<cliente_id>', methods=['PUT'])
def atualizar_clientes(cliente_id):
    cliente =Clientes.query.get_or_404(cliente_id)
    nome=request.json['nome']
    email=request.json['email']
    if Clientes.query.filter_by(email=email).first() is not None:
        return jsonify({'error': 'O email já existe no banco de dados!'}), 409
    cliente.nome=nome
    cliente.email=email
    db.session.commit()
    try:
        return jsonify({'message':'Atualizado com sucesso'})
    except:
        return jsonify({'message':'erro interno no servidor'})

@app.route('/clientes/<cliente_id>', methods=['DELETE'])
def excluir(cliente_id):
    cliente=Clientes.query.get_or_404(cliente_id)
    db.session.delete(cliente)
    db.session.commit()
    return jsonify({'message':'deletado com sucesso'})       
    
   
        
if __name__=='__main__':
    app.run(debug=True)