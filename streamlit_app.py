import streamlit as st
import requests
import pandas as pd
from app.utils.locations import REGIONES_COMUNAS

API_URL = "http://127.0.0.1:8001/api/v1/products"

st.set_page_config(page_title="Sistema Empresarial", layout="wide")
st.title("Sistema de Gestión Empresarial")

# Inicializar session_state
if "loaded_product" not in st.session_state:
    st.session_state.loaded_product = None

# ============== FUNCIONES API ==============
def get_products():
    """Obtiene todos los productos de la API"""
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Error de conexión: {e}")
    return []

def get_product_by_id(product_id):
    """Obtiene un producto específico por ID"""
    try:
        response = requests.get(f"{API_URL}/{product_id}")
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return None
    except Exception as e:
        st.error(f"Error de conexión: {e}")
    return None

def create_product(name, description, price, customer_name, region, comuna, delivery_address, status):
    """Crea un nuevo producto"""
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
    try:
        response = requests.post(API_URL, json=product_data)
        if response.status_code in [200, 201]:
            return response.json()
    except Exception as e:
        st.error(f"Error al crear: {e}")
    return None

def update_product(product_id, name, description, price, customer_name, region, comuna, delivery_address, status):
    """Actualiza un producto existente"""
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
    try:
        response = requests.put(f"{API_URL}/{product_id}", json=product_data)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Error al actualizar: {e}")
    return None

def delete_product(product_id):
    try:
        response = requests.delete(f"{API_URL}/{product_id}")
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Error al eliminar: {e}")
    return None

import time

@st.cache_data(show_spinner=False)
def geocode_address(address, comuna, region):
    """
    Convierte una dirección de Chile en coordenadas (latitud, longitud).
    Usa Nominatim (OpenStreetMap) filtrando solo por Chile para evitar confusiones.
    """
    if not address or address == "Sin dirección":
        return None, None
        
    query = f"{address}, {comuna}, {region}, Chile"
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": query,
        "format": "json",
        "countrycodes": "cl",
        "limit": 1
    }
    headers = {
        "User-Agent": "GestorEmpresarialApp/1.0"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data:
                return float(data[0]["lat"]), float(data[0]["lon"])
        # Para evitar bloquear la API por muchas peticiones (Nominatim requiere max 1 req/sec)
        time.sleep(1)
    except Exception as e:
        pass
    return None, None

# ============== MENÚ LATERAL (SIDEBAR) ==============
st.sidebar.title("Navegación")
selected_menu = st.sidebar.radio(
    "",
    ["📝 CRUD de Pedidos", "🗺️ Mapa de Entregas", "⚙️ Configuración/Estadísticas"]
)

# ============== SECCIÓN 1: GESTIÓN INTEGRADA ==============
if selected_menu == "📝 CRUD de Pedidos":
    st.header("Gestión de Pedidos / Productos")
    
    # Obtener la lista de productos
    products_list = get_products()
    
    st.divider()
    
    # VISTA PRINCIPAL: Tabla de productos
    st.subheader("Inventario Actual")
    if products_list:
        # Mostrar datos en tabla con opciones
        df_display = pd.DataFrame(products_list)
        st.dataframe(df_display, width='stretch', hide_index=True)
    else:
        st.warning("📭 No hay pedidos registrados. ¡Crea el primero!")
    
    st.divider()
    
    # FLUJO PRINCIPAL: 3 SECCIONES EN PESTAÑAS LOCALES
    operation_tabs = st.tabs(["Crear Nuevo", "Actualizar Existente", "Eliminar"])
    
    # ========== SECCIÓN 1: CREAR ==========
    with operation_tabs[0]:
        st.subheader("Registrar Nuevo Pedido/Producto")
        with st.container(border=True):
            col_create1, col_create2 = st.columns(2)
            
            with col_create1:
                c_name = st.text_input("Nombre del Producto", placeholder="ej: Lavadora 16kg")
                c_price = st.number_input("Precio", min_value=0.0, step=0.01, format="%.2f")
                c_customer = st.text_input("Nombre del Cliente", placeholder="ej: Juan García")
            
            with col_create2:
                c_description = st.text_area(" Descripción", placeholder="ej: Lavadora automática 16kg marca XYZ", height=120)
            
            st.markdown("---")
            st.write("**Ubicación de Entrega**")
            col_loc1, col_loc2, col_loc3 = st.columns(3)
            
            with col_loc1:
                region_options = list(REGIONES_COMUNAS.keys())
                c_region = st.selectbox("Región", region_options)
            
            with col_loc2:
                c_comuna_options = REGIONES_COMUNAS[c_region]
                c_comuna = st.selectbox("Comuna", c_comuna_options)
            
            with col_loc3:
                c_status = st.selectbox("Estado Inicial", ["pendiente", "en proceso", "entregado"])
            
            c_address = st.text_input("Dirección Completa", placeholder="ej: Calle Principal 123, Apto 4")
            
            st.markdown("---")
            
            col_btn1, col_btn2 = st.columns([3, 1])
            with col_btn1:
                if st.button("Crear Pedido", type="primary", use_container_width=True):
                    if not c_name or not c_customer or c_price <= 0 or not c_address:
                        st.error("❌ Error: Faltan campos obligatorios o el precio es inválido. Por favor, revise el formulario y vuelva a intentarlo.")
                    else:
                        resultado = create_product(c_name, c_description, c_price, c_customer, c_region, c_comuna, c_address, c_status)
                        if resultado:
                            st.success(f"✅ ¡Pedido creado correctamente! (ID: {resultado.get('id')})")
                            time.sleep(1.5)
                            st.rerun()
                        else:
                            st.error("❌ Ocurrió un error al intentar guardar el pedido en la base de datos.")
    
    # ========== SECCIÓN 2: ACTUALIZAR ==========
    with operation_tabs[1]:
        st.subheader("Modificar Pedido Existente")
        st.write("**Paso 1:** Selecciona el ID del pedido que deseas actualizar")
        
        col_search1, col_search2 = st.columns([2, 1])
        with col_search1:
            u_product_id = st.number_input("ID del Pedido a Actualizar", min_value=1, key="update_id")
        
        with col_search2:
            if st.button("🔄 Cargar Datos", use_container_width=True):
                producto = get_product_by_id(u_product_id)
                if producto:
                    st.session_state.loaded_product = producto
                    st.success(f"Pedido #{u_product_id} cargado")
                else:
                    st.session_state.loaded_product = None
                    st.error(f"No se encontró pedido con ID {u_product_id}")
        
        st.divider()
        
        if st.session_state.loaded_product:
            producto = st.session_state.loaded_product
            st.write("**Paso 2:** Los campos están precargados. Modifica solo lo que necesites")
            
            with st.container(border=True):
                col_upd1, col_upd2 = st.columns(2)
                
                with col_upd1:
                    u_name = st.text_input("Nombre del Producto", value=producto.get("name", ""))
                    u_price = st.number_input("Precio", value=float(producto.get("price", 0)), min_value=0.0, step=0.01, format="%.2f")
                    u_customer = st.text_input("Nombre del Cliente", value=producto.get("customer_name", ""))
                
                with col_upd2:
                    u_description = st.text_area("Descripción", value=producto.get("description", ""), height=120)
                
                st.markdown("---")
                st.write("**Ubicación de Entrega**")
                col_upd_loc1, col_upd_loc2, col_upd_loc3 = st.columns(3)
                
                with col_upd_loc1:
                    region_options = list(REGIONES_COMUNAS.keys())
                    u_region = st.selectbox("Región", region_options, index=region_options.index(producto.get("region", region_options[0])), key="upd_region")
                
                with col_upd_loc2:
                    u_comuna_options = REGIONES_COMUNAS[u_region]
                    u_comuna_index = u_comuna_options.index(producto.get("comuna", u_comuna_options[0])) if producto.get("comuna") in u_comuna_options else 0
                    u_comuna = st.selectbox("Comuna", u_comuna_options, index=u_comuna_index, key="upd_comuna")
                
                with col_upd_loc3:
                    u_status = st.selectbox("Estado del Pedido", ["pendiente", "en proceso", "entregado"], index=["pendiente", "en proceso", "entregado"].index(producto.get("status", "pendiente")))
                
                u_address = st.text_input("Dirección Completa", value=producto.get("delivery_address", ""))
                
                st.markdown("---")
                col_upd_btn1, col_upd_btn2 = st.columns([3, 1])
                with col_upd_btn1:
                    if st.button("Guardar Cambios", type="primary", use_container_width=True):
                        if not u_name:
                            st.error("El nombre del producto es obligatorio")
                        elif not u_customer:
                            st.error("El nombre del cliente es obligatorio")
                        elif u_price <= 0:
                            st.error(" El precio debe ser mayor a 0")
                        else:
                            resultado = update_product(u_product_id, u_name, u_description, u_price, u_customer, u_region, u_comuna, u_address, u_status)
                            if resultado:
                                st.success(f"¡Pedido #{u_product_id} actualizado exitosamente!")
                                st.session_state.loaded_product = None
                                st.rerun()
                            else:
                                st.error(" Error al actualizar el pedido")
        else:
            st.info("Carga un pedido para ver sus datos precargados y poder editarlos")
    
    # ========== SECCIÓN 3: ELIMINAR ==========
    with operation_tabs[2]:
        st.subheader("Eliminar Pedido")
        st.warning("Esta acción no se puede deshacer")
        
        with st.form("delete_form"):
            del_id = st.number_input("ID del Pedido a Eliminar", min_value=1)
            
            # Mostrar confirmación
            if del_id > 0:
                prod_confirm = get_product_by_id(del_id)
                if prod_confirm:
                    st.info(f"**Datos a eliminar:**\n- Producto: {prod_confirm.get('name')}\n- Cliente: {prod_confirm.get('customer_name')}\n- ID: {del_id}")
            
            confirm_delete = st.checkbox("Confirmo que deseo eliminar este pedido")
            submitted_delete = st.form_submit_button("Eliminar Permanentemente", type="secondary")
            
            if submitted_delete:
                if not confirm_delete:
                    st.error(" Debes confirmar la eliminación")
                else:
                    resultado = delete_product(del_id)
                    if resultado:
                        st.success(f"¡Pedido #{del_id} eliminado!")
                        st.rerun()
                    else:
                        st.error(" Error al eliminar el pedido")

# ============== SECCIÓN 2: MAPA ==============
elif selected_menu == "🗺️ Mapa de Entregas":
    st.header("Mapa de Envíos y Rutas")
    
    products_to_map = get_products()
    
    if products_to_map:
        with st.spinner("Geolocalizando las direcciones en Chile..."):
            map_data = []
            
            for p in products_to_map:
                address = p.get("delivery_address")
                comuna = p.get("comuna")
                region = p.get("region")
                status = p.get("status")
                name = p.get("name")
                
                # Ignorar si está entregado o no tiene dirección
                if address and address != "Sin dirección" and status != "entregado":
                    lat, lon = geocode_address(address, comuna, region)
                    if lat and lon:
                        map_data.append({
                            "Producto": name,
                            "Cliente": p.get("customer_name"),
                            "Dirección": f"{address}, {comuna}",
                            "Estado": status,
                            "lat": lat,
                            "lon": lon
                        })
            
            if map_data:
                df_map = pd.DataFrame(map_data)
                
                st.subheader("Ubicación de Pedidos Activos (Pendientes / En proceso)")
                # Renderizar mapa usando la función nativa de Streamlit
                # Usa lat y lon del dataframe
                st.map(df_map, latitude="lat", longitude="lon", color="#ff0000", size=50)
                
                st.write("**Detalles Georreferenciados:**")
                st.dataframe(df_map.drop(columns=["lat", "lon"]), width="stretch", hide_index=True)
            else:
                st.warning("No se encontraron coordenadas válidas en Chile para las direcciones proporcionadas de pedidos activos.")
    else:
        st.info("No hay pedidos registrados para mostrar en el mapa.")

# ============== SECCIÓN 3: CONFIGURACIÓN ==============
elif selected_menu == "⚙️ Configuración/Estadísticas":
    st.header("Configuraciones del Sistema")
    
    col_config1, col_config2 = st.columns(2)
    
    with col_config1:
        st.subheader("Estadísticas del Sistema")
        all_products = get_products()
        total = len(all_products)
        pendientes = len([p for p in all_products if p.get("status") == "pendiente"])
        en_proceso = len([p for p in all_products if p.get("status") == "en proceso"])
        entregados = len([p for p in all_products if p.get("status") == "entregado"])
        
        st.metric("Total de Pedidos", total)
        st.metric("Pendientes", pendientes)
        st.metric("En Proceso", en_proceso)
        st.metric("Entregados", entregados)
    
    with col_config2:
        st.subheader("Resumen Rápido")
        if all_products:
            df_stats = pd.DataFrame(all_products)
            st.write(f"**Precio Promedio:** ${df_stats['price'].mean():.2f}")
            st.write(f"**Precio Máximo:** ${df_stats['price'].max():.2f}")
            st.write(f"**Precio Mínimo:** ${df_stats['price'].min():.2f}")
        else:
            st.write("No hay datos disponibles")
