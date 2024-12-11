from flask import Flask, jsonify
from backend import mintr,Ruaf,Simit




app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route("/")
def root():
    return "Api de consumo para la consulta de antecedentes y comparendos"


@app.route("/mintr/<placa>", methods = ['GET'])
def response(placa):
    try:
        return jsonify( mintr.consultarMintri(placa))
    except: 
        return "no se pudo realizar la peticion"
    

@app.route("/simit/<placa>", methods = ['GET'])
def response2(placa):
    try:
        return jsonify( Simit.ConsultaSimit(placa))
    except: 
        return "no se pudo realizar la peticion"
    

@app.route("/ruaf/<tipoDocumento>/<noDocumento>/<fechaExpedicion>", methods = ['GET'])
def response3(tipoDocumento, noDocumento, fechaExpedicion):
    try:
        return jsonify(Ruaf.consultarRuaf(tipoDocumento, noDocumento, fechaExpedicion))
    except: 
        return "no se pudo realizar la peticion"
    






if __name__ == "__main__":
    app.run(debug=True)




