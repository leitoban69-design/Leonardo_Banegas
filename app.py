import psycopg2
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- Conexión a PostgreSQL ---
conn = psycopg2.connect(
    host="pdpg-d6ge08sr85hc738srkkg-a.virginia-postgres.render.com",
    database="sistema_xkqk",
    user="sistema",
    password="w1mEeP3fmiSkV0tc96WjB77oRdN2YetH",
    port="5432",
    sslmode="require"
)
cur = conn.cursor()

# --- Funciones CRUD ---
def crear_estudiante(nombre, apellido, cedula, carrera, semestre):
    cur.execute("INSERT INTO estudiantes (nombre, apellido, cedula, carrera, semestre) VALUES (%s, %s, %s, %s, %s)", 
                (nombre, apellido, cedula, carrera, semestre))
    conn.commit()

def leer_estudiantes():
    cur.execute("SELECT * FROM estudiantes")
    return cur.fetchall()

def actualizar_estudiante(id, nombre, apellido, cedula, carrera, semestre):
    cur.execute("UPDATE estudiantes SET nombre=%s, apellido=%s, cedula=%s, carrera=%s, semestre=%s WHERE id=%s", 
                (nombre, apellido, cedula, carrera, semestre, id))
    conn.commit()

def eliminar_estudiante(id):
    cur.execute("DELETE FROM estudiantes WHERE id=%s", (id,))
    conn.commit()

# --- Interfaz Streamlit ---
st.title("Sistema de Gestión de Estudiantes")
st.header("Leonardo Plutarco Banegas López")
st.subheader("Carrera: Big Data e Inteligencia de Negocios")

# --- Mostrar estudiantes primero ---
estudiantes = leer_estudiantes()
df = pd.DataFrame(estudiantes, columns=["ID", "Nombre", "Apellido", "Cédula", "Carrera", "Semestre"])
st.write("### Lista de estudiantes registrados")
st.dataframe(df)

st.write("---")

# --- Formulario de Ingreso ---
st.write("### Ingresar nuevo estudiante")
with st.form("form_ingreso", clear_on_submit=True):
    nombre = st.text_input("Nombre")
    apellido = st.text_input("Apellido")
    cedula = st.text_input("Cédula")
    carrera = st.text_input("Carrera")
    semestre = st.number_input("Semestre", min_value=1)
    if st.form_submit_button("Guardar estudiante"):
        crear_estudiante(nombre, apellido, cedula, carrera, semestre)
        st.success(f"Estudiante {nombre} guardado correctamente")
        st.rerun()

st.write("---")

# --- Formulario de Actualizar ---
st.write("### Actualizar estudiante")
with st.form("form_actualizar", clear_on_submit=True):
    id_upd = st.number_input("ID a actualizar", min_value=1)
    n_nom = st.text_input("Nuevo Nombre")
    n_ape = st.text_input("Nuevo Apellido")
    n_ced = st.text_input("Nueva Cédula")
    n_car = st.text_input("Nueva Carrera")
    n_sem = st.number_input("Nuevo Semestre", min_value=1)
    if st.form_submit_button("Actualizar"):
        actualizar_estudiante(id_upd, n_nom, n_ape, n_ced, n_car, n_sem)
        st.success(f"ID {id_upd} actualizado")
        st.rerun()

st.write("---")

# --- Formulario de Eliminar ---
st.write("### Eliminar estudiante")
with st.form("form_eliminar", clear_on_submit=True):
    id_del = st.number_input("ID a eliminar", min_value=1)
    if st.form_submit_button("Eliminar"):
        eliminar_estudiante(id_del)
        st.warning(f"ID {id_del} eliminado")
        st.rerun()

# --- Gráfico al Final ---
st.write("---")
st.write("### Análisis Visual: Distribución por Semestre")
if not df.empty:
    fig, ax = plt.subplots()
    df["Semestre"].value_counts().sort_index().plot(kind="bar", color="skyblue", ax=ax)
    st.pyplot(fig)
