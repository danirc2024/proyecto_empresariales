import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Sistema de Seguimiento de Pedidos", layout="wide")
st.title("📦 Sistema de Seguimiento de Pedidos")

# Ruta del archivo de datos
DATA_FILE = "pedidos.json"

# Cargar datos existentes
def cargar_pedidos():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Guardar datos
def guardar_pedidos(pedidos):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(pedidos, f, ensure_ascii=False, indent=2)

# Inicializar datos en sesión
if "pedidos" not in st.session_state:
    st.session_state.pedidos = cargar_pedidos()

# Interfaz con tabs
tab1, tab2, tab3 = st.tabs(["📝 Registrar Pedido", "📊 Consultar Pedidos", "🔄 Cambiar Estado"])

# TAB 1: REGISTRAR PEDIDO
with tab1:
    st.subheader("Registrar un Nuevo Pedido")
    
    col1, col2 = st.columns(2)
    
    with col1:
        cliente = st.text_input("Nombre del Cliente", placeholder="Ej: Juan García")
        producto = st.text_input("Producto/Descripción", placeholder="Ej: Laptop Dell")
    
    with col2:
        cantidad = st.number_input("Cantidad", min_value=1, step=1)
        precio = st.number_input("Precio unitario ($)", min_value=0.0, step=0.01)
    
    if st.button("✅ Registrar Pedido", type="primary"):
        if cliente and producto:
            nuevo_pedido = {
                "id": len(st.session_state.pedidos) + 1,
                "cliente": cliente,
                "producto": producto,
                "cantidad": int(cantidad),
                "precio_total": round(cantidad * precio, 2),
                "estado": "pendiente",
                "fecha": datetime.now().strftime("%d/%m/%Y %H:%M")
            }
            st.session_state.pedidos.append(nuevo_pedido)
            guardar_pedidos(st.session_state.pedidos)
            st.success(f"✅ Pedido #{nuevo_pedido['id']} registrado exitosamente")
        else:
            st.error("❌ Por favor completa todos los campos")

# TAB 2: CONSULTAR PEDIDOS
with tab2:
    st.subheader("Consultar Estado de Pedidos")
    
    if st.session_state.pedidos:
        # Crear tabla
        df = pd.DataFrame(st.session_state.pedidos)
        
        # Selector de estado para filtrar
        estado_filtro = st.selectbox("Filtrar por estado:", ["Todos", "pendiente", "en proceso", "entregado"])
        
        if estado_filtro != "Todos":
            df = df[df["estado"] == estado_filtro]
        
        # Mostrar tabla
        st.dataframe(
            df[["id", "cliente", "producto", "cantidad", "precio_total", "estado", "fecha"]],
            use_container_width=True,
            hide_index=True
        )
        
        st.write(f"**Total de pedidos:** {len(st.session_state.pedidos)}")
    else:
        st.info("📭 No hay pedidos registrados aún")

# TAB 3: CAMBIAR ESTADO
with tab3:
    st.subheader("Actualizar Estado de Pedido")
    
    if st.session_state.pedidos:
        # Buscar pedido por ID
        pedido_id = st.selectbox(
            "Seleccionar Pedido",
            options=[p["id"] for p in st.session_state.pedidos],
            format_func=lambda x: f"Pedido #{x} - {next(p['cliente'] for p in st.session_state.pedidos if p['id'] == x)}"
        )
        
        # Encontrar el pedido
        pedido_actual = next(p for p in st.session_state.pedidos if p["id"] == pedido_id)
        
        # Mostrar información actual
        st.write(f"**Cliente:** {pedido_actual['cliente']}")
        st.write(f"**Producto:** {pedido_actual['producto']}")
        st.write(f"**Estado actual:** {pedido_actual['estado']}")
        
        # Selector de nuevo estado
        nuevo_estado = st.selectbox(
            "Cambiar estado a:",
            ["pendiente", "en proceso", "entregado"]
        )
        
        if st.button("🔄 Actualizar Estado", type="primary"):
            # Actualizar estado
            for p in st.session_state.pedidos:
                if p["id"] == pedido_id:
                    p["estado"] = nuevo_estado
                    break
            guardar_pedidos(st.session_state.pedidos)
            st.success(f"✅ Pedido #{pedido_id} actualizado a: **{nuevo_estado}**")
    else:
        st.info("📭 No hay pedidos registrados para actualizar")
