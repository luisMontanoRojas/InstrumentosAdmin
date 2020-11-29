from flask import Flask, render_template, request, redirect, url_for
from bson import ObjectId
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client.musicalInstrumentsShop
products = db.products

@app.route('/')
def listaTodos():
    products_l = products.find()
    return render_template('home.html', products=products_l)

@app.route('/addProducto', methods=["POST"])
def addProducto():
    nombre = request.form['nombre']
    precio = request.form['precio']
    descripcion = request.form['descripcion']
    cantidad = request.form['cantidad']
    imageurl1 = request.form['imageurl1']
    imageurl2 = request.form['imageurl2']
    categoria = request.form['categoria']
    vistas=0
    cantidad_vendidas=0

    productToAdd={
        "nombre" : nombre, 
        "precio" : precio, 
        "descripcion" : descripcion, 
        "cantidad" : cantidad, 
        "imageurl1" : imageurl1, 
        "imageurl2" : imageurl2, 
        "categoria" : categoria, 
        "vistas" : vistas, 
        "cantidad_vendidas" : cantidad_vendidas
    }

    products.insert_one(productToAdd)
    return listaTodos()

@app.route('/eliminarProducto')
def eliminarProducto():
    id_prd = request.values.get("_id")
    products.delete_one({"_id": ObjectId(id_prd)})
    return listaTodos()

@app.route('/pianos')
def listaPianos():
    products_l = products.find({"categoria":"Piano Digital"})
    return render_template('home.html', products=products_l)

@app.route('/guitarras')
def listaGuitarras():
    # //esto se cambiara y se pondra sin acentp
    products_l = products.find({"categoria":"Guitarra Eléctrica"})
    return render_template('home.html', products=products_l)

@app.route('/baterias')
def listaBaterias():
    # //esto se cambiara y se pondra sin acentp
    products_l = products.find({"categoria":"Batería Completa"})
    return render_template('home.html', products=products_l)

@app.route('/flautas')
def listaFlautas():
    products_l = products.find({"categoria":"Flauta Travesera"})
    return render_template('home.html', products=products_l)

@app.route('/violines')
def listaViolines():
    products_l = products.find({"categoria":"Violin"})
    return render_template('home.html', products=products_l)

@app.route('/mas_vistos')
def listaMasVistos():
    products_l = products.find()
    products_lO = sorted(products_l, key=lambda product: product['vistas'], reverse=True)
    return render_template('home.html', products=products_lO)

@app.route('/mas_vendidos')
def listaMasVendidos():
    products_l = products.find()
    products_lO = sorted(products_l, key=lambda product: product['cantidad_vendidas'], reverse=True)
    return render_template('home.html', products=products_lO)

@app.route("/search", methods=["GET"])
def search():
    key=request.values.get("key")
    products_l=products.find({"nombre":(key)})
    return render_template('home.html',products=products_l)

@app.route('/contact')
def about():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)