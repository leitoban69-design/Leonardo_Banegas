import psycopg2
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# --- Clases POO ---
class Persona:
    def __init__(self, nombre, apellido, cedula):
        self.nombre = nombre
        self.apellido = apellido
        self.cedula = cedula


    def mostrar_info(self):
        return f"{self.nombre} {self.apellido} - Cédula: {self.cedula}"


class Estudiante(Persona):
    def __init__(self, nombre, apellido, cedula, carrera, semestre):
        super().__init__(nombre, apellido, cedula)
        self.carrera = carrera
        self.semestre = semestre


    def mostrar_info(self):
        return f"{super().mostrar_info()} - Carrera: {self.carrera}, Semestre: {self.semestre}"


class Profesor(Persona):
    def __init__(self, nombre, apellido, cedula, materia, titulo):
        super().__init__(nombre, apellido, cedula)
        self.materia = materia
        self.titulo = titulo


    def mostrar_info(self):
        return f"{super().mostrar_info()} - Materia: {self.materia}, Título: {self.titulo}"


# --- Conexión a PostgreSQL en Render ---
conn = psycopg2.connect(
    host="pdpg-d6ge08sr85hc738srkkg-a.virginia-postgres.render.com",
    database="sistema_xkqk",
    user="sistema",
    password="w1mEeP3fmiSkV0tc96WjB77oRdN2YetH",
    port="5432",
    sslmode="require"
)
cur = conn.cursor()
conn.rollback()
cur = conn.cursor()


# Crear tabla si no existe
cur.execute("""
CREATE TABLE IF NOT EXISTS estudiantes (
    id SERIAL PRIMARY KEY,
    nombre TEXT,
    apellido TEXT,
    cedula TEXT,
    carrera TEXT,
    semestre INT
)
""")
conn.commit()


# --- Funciones CRUD ---
def crear_estudiante(nombre, apellido, cedula, carrera, semestre):
    cur.execute("""
        INSERT INTO estudiantes (nombre, apellido, cedula, carrera, semestre)
        VALUES (%s, %s, %s, %s, %s)
    """, (nombre, apellido, cedula, carrera, semestre))
    conn.commit()


def leer_estudiantes():
    cur.execute("SELECT * FROM estudiantes")
    return cur.fetchall()


def actualizar_estudiante(id, nombre, apellido, cedula, carrera, semestre):
    cur.execute("""
        UPDATE estudiantes
        SET nombre=%s, apellido=%s, cedula=%s, carrera=%s, semestre=%s
        WHERE id=%s
    """, (nombre, apellido, cedula, carrera, semestre, id))
    conn.commit()


def eliminar_estudiante(id):
    cur.execute("DELETE FROM estudiantes WHERE id=%s", (id,))
    conn.commit()


# --- Interfaz Streamlit ---
st.title("Sistema de Gestión de Estudiantes")
st.header("Leonardo Plutarco Banegas López")
st.subheader("Carrera: Big Data e Inteligencia de Negocios")


# --- Dentro de la Interfaz Streamlit ---

# --- Crear estudiante ---
st.write("### Ingresar nuevo estudiante")
# Agregamos 'key' para poder resetearlos después
nombre = st.text_input("Nombre", key="n_nombre")
apellido = st.text_input("Apellido", key="n_apellido")
cedula = st.text_input("Cédula", key="n_cedula")
carrera = st.text_input("Carrera", key="n_carrera")
semestre = st.number_input("Semestre", min_value=1, key="n_semestre")

if st.button("Guardar estudiante"):
    # Llamada a la función CRUD
    crear_estudiante(nombre, apellido, cedula, carrera, semestre)
    st.success(f"Estudiante {nombre} {apellido} guardado correctamente")
    
    # Lógica de limpieza: ponemos los campos en blanco en el estado de la sesión
    st.session_state.n_nombre = ""
    st.session_state.n_apellido = ""
    st.session_state.n_cedula = ""
    st.session_state.n_carrera = ""
    st.session_state.n_semestre = 1
    
    # Refrescamos la página para que se vean los cambios y los campos limpios
    st.rerun()

# --- Mostrar estudiantes ---
st.write("### Lista de estudiantes registrados")
estudiantes = leer_estudiantes()
st.table(estudiantes)


# --- Mostrar con pandas ---
df = pd.DataFrame(estudiantes, columns=["ID", "Nombre", "Apellido", "Cédula", "Carrera", "Semestre"])
st.write("### Tabla de estudiantes con pandas")
st.dataframe(df)

if st.button("Actualizar estudiante"):
    actualizar_estudiante(id_update, nuevo_nombre, nuevo_apellido, nueva_cedula, nueva_carrera, nuevo_semestre)
    st.success(f"Estudiante con ID {id_update} actualizado correctamente")
    
    # Limpiamos los campos de actualización
    for k in ["nuevo_nombre", "nuevo_apellido", "nueva_cedula", "nueva_carrera"]:
        st.session_state[k] = ""
    
    st.rerun()


# --- Eliminar estudiante ---
st.write("### Eliminar estudiante")
# Agregamos una 'key' para poder limpiar el campo después
id_delete = st.number_input("ID del estudiante a eliminar", min_value=1, key="input_eliminar")

if st.button("Eliminar estudiante"):
    # Ejecuta la función CRUD (4 espacios)
    eliminar_estudiante(id_delete)
    
    # Mensaje de confirmación (4 espacios)
    st.warning(f"Estudiante con ID {id_delete} eliminado correctamente")
    
    # Limpiamos el campo (4 espacios)
    st.session_state.input_eliminar = 1
    
    # Forzamos el refresco (4 espacios)
    st.rerun()

 # --- Gráfico con matplotlib ---
 st.write("### Distribución por semestre")
 fig, ax = plt.subplots()
 df["Semestre"].value_counts().sort_index().plot(kind="bar", ax=ax)
 st.pyplot(fig)
