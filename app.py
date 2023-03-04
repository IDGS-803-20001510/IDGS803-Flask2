from flask import Flask, render_template
from flask import request
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from flask import make_response
from flask import flash
import difflib
from wtforms import SelectField, RadioField

import forms
app=Flask(__name__)
app.config["SECRET_KEY"]= "Esta es la clave encriptada"
csrf = CSRFProtect()

@app.errorhandler(404)
def no_encontrado(e):
    return render_template("404.html"),404

@app.route("/cookies" , methods=["GET", "POST"])
def cookies():
    reg_user=forms.LoginForm(request.form)
    datos=''
    if request.method== 'POST' and reg_user.validate():
        user=reg_user.username.data
        passw=reg_user.password.data
        datos=user+'@'+passw
        success_message='Bienvenido {}'.format(user)
        flash(success_message)

    response=make_response(render_template("cookies.html",form=reg_user))
    if len(datos)>0:
        response.set_cookie("datos_user",datos)
    return response

@app.route("/saludo")
def saludo():
    valor_cookie=request.cookies.get("datos_user")
    nombres=valor_cookie.split('@')
    return render_template("saludo.html", nom=nombres[0])

@app.route("/formulario")
def formulario():
    return render_template("formulario.html")

@app.route("/Alumnos", methods=["GET", "POST"])
def alumnos():
    alum_form=forms.UserForm(request.form)
    if request.method == "POST" and alum_form.validate():
        print(alum_form.matricula.data)
        print(alum_form.nombre.data)
    return render_template("Alumnos.html",form=alum_form)

@app.route("/Diccionario", methods=["GET", "POST"])
def Diccionario():
    palabras_form = forms.Diccionario(request.form)
    espaniol = ""
    ingles = ""
    dicc = {}
    mensaje = ""

    if request.method=="POST":
        espaniol = palabras_form.espanol.data
        ingles = palabras_form.ingles.data
        print(espaniol)
        print(ingles)

        dicc = {espaniol:ingles}
        print(dicc)

        with open('palabras.txt', 'a') as archivo:
            for clave, valor in dicc.items():
                    archivo.write("{}:{}\n".format(clave,valor))
        mensaje = "La palabra {} ha sido agregada al diccionario".format(espaniol)
    return render_template("Actividad2-Diccionario.html",form=palabras_form, mensaje=mensaje)

@app.route("/DiccionarioV", methods=["GET", "POST"])
def DiccionarioV():
    palabras_form = forms.Diccionario(request.form)
    palabra = ""
    palabras = {}
    encontrado = False

    if request.method=="POST":
        palabra = palabras_form.palabra.data

        with open("palabras.txt", "r") as archivo:
            palabra = palabra.lower()
            for linea in archivo:
                clave, valor = linea.strip().split(":")
                palabras[clave] = valor   
           

            if request.form.get("idioma") == "espanol":
                # buscar las palabras más cercanas en el diccionario
                matches = difflib.get_close_matches(palabra, palabras.values())
                if matches:
                    # usar la primera palabra coincidente como clave
                    clave = next(key for key, value in palabras.items() if value == matches[0])
                    return render_template("Actividad2-Diccionario.html", form=palabras_form, palabra=clave)
                else:
                    return render_template("Actividad2-Diccionario.html", form=palabras_form, palabra="No se encontro la palabra")
                
        if request.form.get("idioma") == "ingles":
            # buscar las palabras más cercanas en el diccionario
            matches = difflib.get_close_matches(palabra, palabras.keys())
            if matches:
                # usar la primera palabra coincidente como valor
                valor = palabras[matches[0]]
                return render_template("Actividad2-Diccionario.html", form=palabras_form, palabra=valor)
            else:
                return render_template("Actividad2-Diccionario.html", form=palabras_form, palabra="No se encontro la palabra")


class Seleccion(FlaskForm):
    banda1 = SelectField("Selecciona un color",  choices=[("black", "Negro"), ("chocolate", "Café"), 
             ("red", "Rojo"), ("orangered", "Naranja"), ("yellow", "Amarillo"), ("green", "Verde"),
             ("blue", "Azul"), ("purple", "Violeta"), ("gray", "Gris"), ("white", "Blanco")],
             render_kw={"class": "color-select"})
    banda2 = SelectField("Selecciona un color",  choices=[("black", "Negro"), ("chocolate", "Café"), 
             ("red", "Rojo"), ("orangered", "Naranja"), ("yellow", "Amarillo"), ("green", "Verde"),
             ("blue", "Azul"), ("purple", "Violeta"), ("gray", "Gris"), ("white", "Blanco")],
             render_kw={"class": "color-select"})
    banda3 = SelectField("Selecciona un color", choices=[("black", "Negro"), ("chocolate", "Café"), 
             ("red", "Rojo"), ("orangered", "Naranja"), ("yellow", "Amarillo"), ("green", "Verde"),
             ("blue", "Azul"), ("purple", "Violeta"), ("gray", "Gris"), ("white", "Blanco")],
             render_kw={"class": "color-select"})
    tolerancia = RadioField("Selecciona la tolerancia", choices=[("goldenrod", "Oro"), ("silver", "Plata")])

tolerancia_porcentaje = {'chocolate': 1, 'red': 2, 'Verde': 0.5, 'blue': 0.25, 'purple': 0.1, 'gray': 0.05, 'goldenrod': 5, 'silver': 10}

def calcular_resistencia(banda1, banda2, banda3, tolerancia):
    colores = {'black': 0, 'chocolate': 1, 'red': 2, 'orangered': 3, 'yellow': 4, 'green': 5, 'blue': 6, 'purple': 7, 'gray': 8, 'white': 9}
    valor = (colores[banda1]*10 + colores[banda2]) * 10**colores[banda3]
    tolerancia_valor = valor * (tolerancia_porcentaje[tolerancia]) / 100
    return valor, tolerancia_valor

@app.route("/Resistencia", methods=["GET", "POST"])
def Resistencia():
        opcion_banda1 = ""
        opcion_banda2 = ""
        opcion_banda3 = ""
        opcion_tolerancia = ""
        valor = ""
        tolerancia_valor = ""
        valor_minimo = ""
        valor_maximo = ""
        tolerancia = ""
        nuevoColorB1 = ""
        nuevoColorB2 = ""
        nuevoColorB3 = ""
        nuevoColorT = ""
            
        form = Seleccion()
        if form.validate_on_submit():
            opcion_banda1 = form.banda1.data
            if opcion_banda1 == 'orangered':
                nuevoColorB1 = 'Naranja'
            elif opcion_banda1 == 'black' :
                nuevoColorB1 = 'Negro'
            elif opcion_banda1 == 'chocolate' :
                nuevoColorB1 = 'Café'
            elif opcion_banda1 == 'red' :
                nuevoColorB1 = 'Rojo'
            elif opcion_banda1 == 'yellow' :
                nuevoColorB1 = 'Amarillo'
            elif opcion_banda1 == 'green' :
                nuevoColorB1 = 'Verde'
            elif opcion_banda1 == 'blue' :
                nuevoColorB1 = 'Azul'
            elif opcion_banda1 == 'purple' :
                nuevoColorB1 = 'Violeta'
            elif opcion_banda1 == 'gray' :
                nuevoColorB1 = 'Gris'
            elif opcion_banda1 == 'white' :
                nuevoColorB1 = 'Blanco'

            opcion_banda2 = form.banda2.data
            if opcion_banda2 == 'orangered':
                nuevoColorB2 = 'Naranja'
            elif opcion_banda2 == 'black' :
                nuevoColorB2 = 'Negro'
            elif opcion_banda2 == 'chocolate' :
                nuevoColorB2 = 'Café'
            elif opcion_banda2 == 'red' :
                nuevoColorB2 = 'Rojo'
            elif opcion_banda2 == 'yellow' :
                nuevoColorB2 = 'Amarillo'
            elif opcion_banda2 == 'green' :
                nuevoColorB2 = 'Verde'
            elif opcion_banda2 == 'blue' :
                nuevoColorB2 = 'Azul'
            elif opcion_banda2 == 'purple' :
                nuevoColorB2 = 'Violeta'
            elif opcion_banda2 == 'gray' :
                nuevoColorB2 = 'Gris'
            elif opcion_banda2 == 'white' :
                nuevoColorB2 = 'Blanco'

            opcion_banda3 = form.banda3.data
            if opcion_banda3 == 'orangered':
                nuevoColorB3 = 'Naranja'
            elif opcion_banda3 == 'black' :
                nuevoColorB3 = 'Negro'
            elif opcion_banda3 == 'chocolate' :
                nuevoColorB3 = 'Café'
            elif opcion_banda3 == 'red' :
                nuevoColorB3 = 'Rojo'
            elif opcion_banda3 == 'yellow' :
                nuevoColorB3 = 'Amarillo'
            elif opcion_banda3 == 'green' :
                nuevoColorB3 = 'Verde'
            elif opcion_banda3 == 'blue' :
                nuevoColorB3 = 'Azul'
            elif opcion_banda3 == 'purple' :
                nuevoColorB3 = 'Violeta'
            elif opcion_banda3 == 'gray' :
                nuevoColorB3 = 'Gris'
            elif opcion_banda3 == 'white' :
                nuevoColorB3 = 'Blanco'
            
            opcion_tolerancia = form.tolerancia.data
            if opcion_tolerancia == 'goldenrod':
                nuevoColorT = 'Oro'
            elif opcion_tolerancia == 'silver' :
                nuevoColorT = 'Plata'
            valor, tolerancia_valor = calcular_resistencia(opcion_banda1, opcion_banda2, opcion_banda3, opcion_tolerancia)         
            valor_minimo = valor * (1 - tolerancia_porcentaje[opcion_tolerancia]/100)
            valor_maximo = valor * (1 + tolerancia_porcentaje[opcion_tolerancia]/100)

        return render_template("Resistencias.html",form=form, banda1 = opcion_banda1, banda2 = opcion_banda2, banda3 = opcion_banda3, tolerancia = opcion_tolerancia , valor=valor, tolerancias=tolerancia_valor, minimo = valor_minimo, maximo = valor_maximo, nuevoColorB1= nuevoColorB1, nuevoColorB2 = nuevoColorB2, nuevoColorB3 = nuevoColorB3, nuevoColorT= nuevoColorT)         


if __name__=="__main__":
    csrf.init_app(app)
    app.run(debug= True)