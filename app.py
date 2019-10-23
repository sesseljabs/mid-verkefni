from flask import Flask, flash, redirect, render_template, request, json
from datetime import datetime
import urllib.request as url

app = Flask(__name__)

with url.urlopen("http://apis.is/petrol") as f:
    data = json.loads(f.read().decode())

li = data["results"]
def inttomon(i):
    dicta = {
        "01": "janúar",
        "02": "febrúar",
        "03": "mars",
        "04": "apríl",
        "05": "maí",
        "06": "júní",
        "07": "júlí",
        "08": "ágúst",
        "09": "september",
        "10": "október",
        "11": "nóvember",
        "12": "desember"
    }
    return dicta[i]
date = data["timestampPriceCheck"]

def getdate(values, date=date):
    obj = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f")
    #print(obj)
    values = values
    return obj.strftime(f"%d {inttomon(obj.strftime('%m'))} %Y %H:%M")

'''def lowest(company, li=li):
    listi = []
    for i in li:
        if i["company"] == company:
            pass'''



# gera lista af fyrirtækjum
fyrirtaeki = []
for i in li:
    if i["company"] not in fyrirtaeki:
        fyrirtaeki.append(i["company"])
print(fyrirtaeki)

laegstabensin = {}
for i in fyrirtaeki:
    temp = []
    for x in li:
        if x["company"] == i:
            temp.append(x["bensin95"])
    laegstabensin[i] = min(temp)

laegstadiesel = {}
for i in fyrirtaeki:
    temp = []
    for x in li:
        if x["company"] == i:
            temp.append(x["diesel"])
    laegstadiesel[i] = min(temp)

verd = {}
verd["bensin"] = min(laegstabensin, key=laegstabensin.get)
verd["diesel"] = min(laegstadiesel, key=laegstadiesel.get)
print(verd)

app.jinja_env.filters['getdate'] = getdate

@app.route("/")
def home():
    return render_template("index.html", li=sorted(fyrirtaeki), bensinverd=laegstabensin, dieselverd=laegstadiesel, verd=verd)

@app.route("/stod/<string:stod>")
def stod(stod):
    listi = []
    for i in li:
        if i["company"] == stod:
            listi.append(i)
    return render_template("stod.html", listi=listi)

@app.errorhandler(404)
def pagenotfound(error):
    return render_template("error.html")

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
    #app.run()