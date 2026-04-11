import streamlit as st
import requests
import pandas as pd
from app.utils.locations import REGIONES_COMUNAS

API_URL = "http://127.0.0.1:8001/api/v1/products"

st.set_page_config(page_title="Sistema Empresarial", layout="wide")
st.title("Sistema de Gestión Empresarial")

# Definir las 3 pestañas
tab1, tab2, tab3 = st.tabs(["CRUD Pedidos", "Mapa (Próximamente)", "Configuración"])

def get_products():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return []

def create_product(name, description, price, customer_name, region, comuna, delivery_address, status):
    product_data = {
        "name": name, 
        "description": description, 
        "price": price,
        "customer_name": customer_name,
        "region": region,
        "comuna": comuna,
        "delivery_address": delivery_address,
        "status": status
    }
    response = requests.post(API_URL, json=product_data)
    return response.json()

def update_product(product_id, name, description, price, customer_name, region, comuna, delivery_address, status):
    product_data = {
        "name": name, 
        "description": description, 
        "price": price,
        "customer_name": customer_name,
        "region": region,
        "comuna": comuna,
        "delivery_address": delivery_address,
        "status": status
    }
    response = requests.put(f"{API_URL}/{product_id}", json=product_data)
    return response.json()

def delete_product(product_id):
    response = requests.delete(f"{API_URL}/{product_id}")
    return response.json()

with tab1:
    st.header("Gestión de Pedidos / Productos")
    
    # Mostrar productos
    st.subheader("Lista Actual")
    products = get_products()
    if products:
        df = pd.DataFrame(products)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No hay datos disponibles o la API no está corriendo.")

    col1, col2, col3 = st.columns(3)
    
    # Crear producto
    with col1:
        st.subheader("Crear")
        with st.container(border=True):
            name = st.text_input("Nombre Producto", key="c_name")
            description = st.text_area("Descripción", key="c_desc")
            price = st.number_input("Precio", min_value=0.0, key="c_price")
            st.markdown("---")
            customer_name = st.text_input("Nombre Cliente", key="c_cname")
            
            # Selección dinámica de región y comuna para creación
            region_options = list(REGIONES_COMUNAS.keys())
            region = st.selectbox("Región", region_options, key="c_region")
            comuna_options = REGIONES_COMUNAS[region]
            comuna = st.selectbox("Comuna", comuna_options, key="c_comuna")
            
            delivery_address = st.text_input("Dirección de Entrega", key="c_addr")
            status = st.selectbox("Estado del Pedido", ["pendiente", "en proceso", "entregado"], key="c_status")

            submitted_create = st.button("Crear Nuevo", type="primary", use_container_width=True)
            if submitted_create:
                if name:
                    create_product(name, description, price, customer_name, region, comuna, delivery_address, status)
                    st.success("¡Registro creado!")
                    st.rerun()
                else:
                    st.error("El nombre del producto es obligatorio.")

    # Actualizar producto
    with col2:
        st.subheader("Actualizar")
        with st.container(border=True):
            product_id = st.number_input("ID a actualizar", min_value=1, key="u_pid")
            new_name = st.text_input("Nuevo Nombre Producto", key="u_name")
            new_desc = st.text_area("Nueva Descripción", key="u_desc")
            new_price = st.number_input("Nuevo Precio", min_value=0.0, key="u_price")
            st.markdown("---")
            new_customer = st.text_input("Nuevo Nombre Cliente", key="u_cname")
            
            # Selección dinámica para actualización
            new_region = st.selectbox("Nueva Región", region_options, key="u_region")
            new_comuna_options = REGIONES_COMUNAS[new_region]
            new_comuna = st.selectbox("Nueva Comuna", new_comuna_options, key="u_comuna")
            
            new_address = st.text_input("Nueva Dirección de Entrega", key="u_addr")
            new_status = st.selectbox("Nuevo Estado", ["pendiente", "en proceso", "entregado"], key="u_status")

            submitted_update = st.button("Actualizar", type="primary", use_container_width=True)
            if submitted_update:
                if new_name:
                    update_product(product_id, new_name, new_desc, new_price, new_customer, new_region, new_comuna, new_address, new_status)
                    st.success("¡Registro actualizado!")
                    st.rerun()
                else:
                    st.error("El nombre del producto es obligatorio.")

    # Eliminar producto
    with col3:
        st.subheader("Eliminar")
        with st.form("delete_form"):
            del_product_id = st.number_input("ID a eliminar", min_value=1)
            submitted_delete = st.form_submit_button("Eliminar")
            if submitted_delete:
                delete_product(del_product_id)
                st.success("¡Registro eliminado!")
                st.rerun()

with tab2:
    st.header("Mapa de Envíos / Rutas")
    st.info("Este espacio está reservado para la funcionalidad de Mapas (Próximamente).")

with tab3:
    st.header("Configuraciones del Sistema")
    st.write("Aquí puedes agregar otras opciones, ajustes y reportes a futuro.")
