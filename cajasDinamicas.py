from flask import Flask, render_template
from flask import request
from collections import Counter

import forms
app=Flask(__name__)

@app.route("/cajasD", methods=['GET', 'POST'])
def cajasD():
    if request.method == 'POST':
        cajas=request.form.get("txtCantCajas")
        return render_template("cajasD.html", cant = int(cajas))
    else:
         return render_template("cajasD.html", cant = 0)
    

@app.route("/cajasDDib" , methods = ['POST'])
def cajasDDib():
    cantNum = request.form.get('txtNum')
    lista = []

    for i in range(1, int(cantNum)+1):
        value = request.form.get('caja'+str(i))
        lista.append(int(value))

    numMayor = max(lista)
    numMenor = min(lista)
    promedio = sum(lista)/int(cantNum)

    contador = Counter(lista)
    
    return render_template('cajasDDib.html', numMayor = str(numMayor), numMenor = str(numMenor), promedio = str(promedio), contador = contador, lenCont = len(contador))

if __name__=="__main__":
    app.run(debug= True)