from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import json
import os
from Paciente import Paciente
from Medicamento import Medicamento
from Cita import Cita

app = Flask(__name__)
CORS(app)

#Almacenamiento
administrador = {
    "nombre":"ingrid",
    "apellido":"perez",
    "nombre_usuario":"admin",
    "contrasena":"1234"
}

pacientes = []
medicamentos = []
citas = []
doctores = []

pacientes.append(Paciente("Ingrid","Pérez","","","ingrid","1234","24452452"))

@app.route('/', methods=['GET'])
def principal():
    return "Api Taller 1"

@app.route('/registro_paciente', methods=['POST'])
def registro_paciente():
    cuerpo = request.get_json()
    nombre = cuerpo['nombre'] #nombre = ingrid
    apellido = cuerpo['apellido']
    fecha_nacimiento = cuerpo['fecha_nacimiento']
    sexo = cuerpo['sexo']
    nombre_usuario = cuerpo['nombre_usuario']
    if(existe_usuario(nombre_usuario)):
        return jsonify({'agregado':0,'mensaje':'Ya existe un usuario con este nombre'})
    contrasena = cuerpo['contraseña']
    telefono = cuerpo['telefono']
    nuevo_paciente = Paciente(nombre,apellido,fecha_nacimiento,sexo,nombre_usuario,contrasena,telefono)
    global pacientes
    pacientes.append(nuevo_paciente)
    return jsonify({'agregado':1,'mensaje':'Registro exitoso'})

@app.route('/obtener_pacientes', methods=['GET'])
def obtener_pacientes():
    json_pacientes = []
    global pacientes
    for paciente in pacientes:
        json_pacientes.append(paciente.get_json())
    return jsonify(json_pacientes)

@app.route('/login', methods=['GET'])
def login():
    nombre_usuario = request.args.get("nombre_usuario")
    contrasena = request.args.get("contrasena")
    if not existe_usuario(nombre_usuario):
        return jsonify({'estado': 0, 'mensaje':'No existe este usuario'})
    usuario = verificar_contrasena(nombre_usuario,contrasena)
    if usuario == 1 or usuario == 2:
        return jsonify({'estado': usuario, 'mensaje':'Login exitoso', 'indice': get_indice_usuario(nombre_usuario)})
    return jsonify({'estado': 0, 'mensaje':'La contraseña es incorrecta'})
    

def verificar_contrasena(nombre_usuario, contrasena):
    if nombre_usuario == administrador['nombre_usuario'] and contrasena == administrador['contrasena']:
        return 1
    global pacientes
    for paciente in pacientes:
        if paciente.nombre_usuario == nombre_usuario and paciente.contrasena == contrasena:
            return 2
    return 0

def get_indice_usuario(nombre_usuario):
    for i in range(len(pacientes)):
        if pacientes[i].nombre_usuario == nombre_usuario:
            return i
    return -1

def existe_usuario(nombre_usuario):
    if nombre_usuario == administrador['nombre_usuario']:
        return True
    global pacientes
    for paciente in pacientes:
        if paciente.nombre_usuario == nombre_usuario:
            return True
    return False

#INICIO CRUD MEDICAMENTOS
@app.route('/cargar_medicamentos', methods=['POST'])
def cargar_medicamentos():
    cuerpo = request.get_json()
    contenido = cuerpo['contenido']
    filas = contenido.split("\r\n")
    global medicamentos
    for fila in filas:
        print(fila)
        columnas = fila.split(",")
        medicamento = Medicamento(columnas[0],columnas[1],columnas[2],columnas[3])
        medicamentos.append(medicamento)
    return jsonify({"mensaje":"Carga masiva exitosa"})

@app.route('/obtener_medicamentos', methods=['GET'])
def obtener_medicamentos():
    json_medicamentos = []
    global medicamentos
    for medicamento in medicamentos:
        json_medicamentos.append(medicamento.get_json())
    return jsonify(json_medicamentos)

@app.route('/eliminar_medicamento', methods=['POST'])
def eliminar_medicamento():
    cuerpo = request.get_json()
    indice = cuerpo['indice']
    i = int(indice)
    global medicamentos
    medicamentos.pop(i)
    return jsonify({"mensaje":"Eliminado exitosamente"})

@app.route('/editar_medicamento', methods=['POST'])
def editar_medicamento():
    cuerpo = request.get_json()
    indice = cuerpo['indice']
    nombre = cuerpo['nombre']
    precio = cuerpo['precio']
    descripcion = cuerpo['descripcion']
    cantidad = cuerpo['cantidad']
    i = int(indice)
    global medicamentos
    medicamentos[i].editar(nombre,precio,descripcion,cantidad)
    return jsonify(medicamentos[i].get_json())

#FIN CRUD MEDICAMENTOS  

#INICIO CITAS
@app.route('/obtener_citas', methods=['GET'])
def obtener_citas():
    json_citas = []
    global citas
    for cita in citas:
        json_citas.append(cita.get_json())
    return jsonify(json_citas)

@app.route('/obtener_citas_enfermera', methods=['GET'])
def obtener_citas_enfermera():
    json_citas = []
    global citas
    for cita in citas:
        if cita.estado == "Pendiente":
            json_citas.append(cita.get_json())
    return jsonify(json_citas)

@app.route('/citas_doctor', methods=['GET'])
def citas_doctor():
    indice = request.args.get("id_doctor")
    i = int(indice)
    json_citas = []
    global citas
    for cita in citas:
        if cita.doctor == i and cita.estado=="Aceptada":
            json_citas.append(cita.get_json())
    return jsonify(json_citas)    

@app.route('/solicitar_cita', methods=['POST'])
def solicitar_cita():
    cuerpo = request.get_json()
    indice = cuerpo['id']
    fecha = cuerpo['fecha']
    hora = cuerpo['hora']
    motivo = cuerpo['motivo']
    i = int(indice)
    global citas
    citas.append(Cita(fecha,hora,motivo,i))
    return jsonify({"mensaje":"Cita creada exitosamente"})
#FIN CITAS

#INICIO PACIENTE
@app.route('/tiene_cita', methods=['GET'])
def tiene_cita():
    indice = request.args.get("id")
    global citas
    for cita in citas:
        if cita.paciente == int(indice):
            if cita.estado == "Pendiente" or cita.estado == "Aceptada":
                return jsonify({'estado':1, 'mensaje':'Tiene una cita pendiente o aceptada.', 'fecha':cita.fecha, 'hora':cita.hora,'estado':cita.estado,'doctor':cita.doctor})
    return jsonify({'estado':0, 'mensaje':'No tiene citas pendientes.'})
#FIN PACIENTE

if __name__ == '__main__':
    puerto = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0',port=puerto)
