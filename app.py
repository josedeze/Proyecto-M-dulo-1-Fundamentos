import streamlit as st

# ----------------------------
# Helpers de "estado" (memoria en la app)
# ----------------------------
def init_state():
    if "actividades" not in st.session_state:
        st.session_state.actividades = []  # lista de diccionarios

init_state()

# ----------------------------
# Home
# ----------------------------
def render_home():
    st.title("Proyecto Aplicado en Streamlit – Fundamentos de Programación")
    st.write("**Estudiante:** Jose Luis De Zela Quispe")
    st.write("**Curso:** Python Fundamentals (Módulo 1)")
    st.write("**Año:** 2026")
    st.write(
        "Objetivo: construir una app en Streamlit que demuestre variables, estructuras de datos, "
        "control de flujo, funciones, programación funcional y POO."
    )
    st.write("**Tecnologías:** Python, Streamlit")

# ----------------------------
# Ejercicio 1 – Variables y Condicionales
# ----------------------------
def render_ejercicio_1():
    st.subheader("Ejercicio 1 – Verificador de Presupuesto")

    presupuesto = st.number_input("Presupuesto", min_value=0.0, value=1000.0,step=1.0)
    gasto = st.number_input("Gasto", min_value=0.0, value=300.0,step=1.0)

    if st.button("Evaluar presupuesto"):
        diferencia = presupuesto - gasto
        if gasto <= presupuesto:
            st.success("El gasto está dentro del presupuesto.")
        else:
            st.warning("El gasto excede el presupuesto.")

        st.write(f"Diferencia (presupuesto - gasto): **{diferencia:.2f}**")

# ----------------------------
# Ejercicio 2 – Listas y Diccionarios
# ----------------------------
def render_ejercicio_2():
    st.subheader("Ejercicio 2 – Registro de Actividades (Lista de Diccionarios)")

    nombre = st.text_input("Nombre de la actividad", placeholder="Ej: Marketing Febrero")
    tipo = st.selectbox("Tipo", ["Ingreso", "Gasto", "Inversión", "Otro"])
    presupuesto = st.number_input("Presupuesto", min_value=0.0, value=0.0, step=50.0)
    gasto_real = st.number_input("Gasto real", min_value=0.0, value=0.0, step=50.0)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Agregar actividad"):
            # Validación simple
            if not nombre.strip():
                st.warning("Escribe un nombre para la actividad.")
                return

            actividad = {
                "nombre": nombre.strip(),
                "tipo": tipo,
                "presupuesto": float(presupuesto),
                "gasto_real": float(gasto_real),
            }
            st.session_state.actividades.append(actividad)
            st.success("Actividad agregada.")

    with col2:
        if st.button("Limpiar lista"):
            st.session_state.actividades = []
            st.info("Lista de actividades reiniciada.")

    st.write("### Actividades registradas")
    if st.session_state.actividades:
        st.dataframe(st.session_state.actividades, use_container_width=True)

        st.write("### Estado por actividad")
        for a in st.session_state.actividades:
            if a["gasto_real"] <= a["presupuesto"]:
                st.success(f"{a['nombre']}: Dentro del presupuesto")
            else:
                st.warning(f"{a['nombre']}: Excede presupuesto")
    else:
        st.info("Aún no has registrado actividades.")

# ----------------------------
# Ejercicio 3 – Funciones y Programación Funcional
# ----------------------------
def calcular_retorno(actividad: dict, tasa: float, meses: int) -> float:
    # Retorno = presupuesto × tasa × meses
    return actividad["presupuesto"] * tasa * meses

def render_ejercicio_3():
    st.subheader("Ejercicio 3 – Retorno Esperado (función + map/lambda)")

    if not st.session_state.actividades:
        st.info("Primero registra actividades en el Ejercicio 2.")
        return

    tasa = st.slider("Tasa (ej: 0.02 = 2%)", min_value=0.0, max_value=0.5, value=0.02, step=0.01)
    meses = st.number_input("Meses", min_value=1, value=6, step=1)

    if st.button("Calcular retorno"):
        # Programación funcional: map + lambda
        retornos = list(map(lambda act: calcular_retorno(act, tasa, int(meses)), st.session_state.actividades))

        st.write("### Resultados")
        for act, ret in zip(st.session_state.actividades, retornos):
            st.write(f"- **{act['nombre']}** → Retorno esperado: **{ret:.2f}**")

# ----------------------------
# Ejercicio 4 – POO
# ----------------------------
class Actividad:
    def __init__(self, nombre: str, tipo: str, presupuesto: float, gasto_real: float):
        self.nombre = nombre
        self.tipo = tipo
        self.presupuesto = presupuesto
        self.gasto_real = gasto_real

    def esta_en_presupuesto(self) -> bool:
        return self.gasto_real <= self.presupuesto

    def mostrar_info(self) -> str:
        return (
            f"Actividad: {self.nombre} | Tipo: {self.tipo} | "
            f"Presupuesto: {self.presupuesto:.2f} | Gasto real: {self.gasto_real:.2f}"
        )

def render_ejercicio_4():
    st.subheader("Ejercicio 4 – POO (Clase Actividad)")

    if not st.session_state.actividades:
        st.info("Primero registra actividades en el Ejercicio 2.")
        return

    # Convertimos diccionarios a objetos
    objetos = [
        Actividad(a["nombre"], a["tipo"], a["presupuesto"], a["gasto_real"])
        for a in st.session_state.actividades
    ]

    st.write("### Actividades como objetos")
    for obj in objetos:
        st.write(obj.mostrar_info())
        if obj.esta_en_presupuesto():
            st.success("Cumple presupuesto")
        else:
            st.warning("No cumple presupuesto")

# ----------------------------
# Navegación principal
# ----------------------------
def main():
    st.sidebar.title("Menú")
    opcion = st.sidebar.selectbox(
        "Ir a:",
        ["Home", "Ejercicio 1", "Ejercicio 2", "Ejercicio 3", "Ejercicio 4"]
    )

    if opcion == "Home":
        render_home()
    elif opcion == "Ejercicio 1":
        render_ejercicio_1()
    elif opcion == "Ejercicio 2":
        render_ejercicio_2()
    elif opcion == "Ejercicio 3":
        render_ejercicio_3()
    elif opcion == "Ejercicio 4":
        render_ejercicio_4()

if __name__ == "__main__":
    main()