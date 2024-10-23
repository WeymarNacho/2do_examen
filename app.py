from flask import Flask, request,render_template,redirect,url_for,session
from datetime import datetime

app=Flask(__name__)
app.secret_key = 'unaclavesecreta'

@app.route("/")
def index():
    if 'carrito' not in session:
        session['carrito'] = []
    
    carrito =  session.get('carrito',[])
    return render_template('index.html',carrito=carrito)

def generar_id():
    if 'carrito' in session and len(session['carrito'])>0:
        return max(item['id'] for item in session ['carrito'])+1
    else:
        return 1



@app.route("/agregar",methods=['GET','POST'])
def agregar():
    if request.method == 'POST':
        nombre =request.form['nombre']
        cantidad=request.form['cantidad']
        precio=request.form['precio']
        fecha_vencimiento=request.form['fecha_vencimiento']
        categoria =request.form['categoria']

        nuevo_producto={
            'id':generar_id(),
            'nombre':nombre,
            'cantidad':cantidad,
            'precio':precio,
            'fecha_vencimiento':fecha_vencimiento,
            'categoria':categoria
        }

        if 'carrito' not in session:
            session['carrito']=[]

        session['carrito'].append(nuevo_producto)
        session.modified=True
        return redirect(url_for('index'))


    return render_template('agregar.html')

@app.route('/editar/<int:id>',methods=['GET','POST'])
def editar(id):
    lista_carrito = session.get('carrito',[])
    carrito=next(( c for c in lista_carrito if c['id']==id),None)
    if not carrito:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        carrito['nombre']=request.form['nombre']
        carrito['cantidad']=int(request.form['cantidad'])
        carrito['precio'] =float(request.form['precio'])
        carrito['fecha_vencimiento'] =request.form['fecha_vencimiento']
        carrito['categoria'] =request.form['categoria']
        session.modified =True
        return redirect(url_for('index'))

    return render_template('editar.html',carrito=carrito)


@app.route("/eliminar/<int:id>",methods =["POST"])
def eliminar(id):
    lista_carrito =session.get('carrito',[])
    carrito =next((c for c in lista_carrito if c['id']==id),None)
    if carrito:
        session['carrito'].remove(carrito)
        session.modified =True
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)