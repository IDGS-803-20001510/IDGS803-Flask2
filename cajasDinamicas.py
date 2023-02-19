from flask import Flask, render_template
from flask import request

import forms
app=Flask(__name__)

@app.route("/cajasD")
def cajasD():
    return render_template("cajasD.html")


if __name__=="__main__":
    app.run(debug= True)