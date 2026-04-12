# Sistema de Gestión Empresarial

## Descripción
Aplicación web para gestionar pedidos y productos de una empresa con distribución geográfica. Combina un frontend en Streamlit con una API REST en FastAPI, permitiendo crear, actualizar, consultar y eliminar pedidos con información de cliente, ubicación de entrega y estado.

## Funcionalidades Actuales
- ✅ **CRUD Completo**: Crear, leer, actualizar y eliminar productos/pedidos
- ✅ **Gestión de Cliente**: Captura nombre del cliente para cada pedido
- ✅ **Gestión Geográfica**: Registro de región y comuna de entrega
- ✅ **Dirección de Entrega**: Almacenamiento de dirección completa
- ✅ **Control de Estados**: Estados para seguimiento del pedido
- ✅ **API REST**: Backend en FastAPI con endpoints documentados
- ✅ **Base de Datos**: Persistencia con base de datos relacional (SQLAlchemy)

## Tecnología
- **Frontend**: Streamlit (interfaz web interactiva)
- **Backend**: FastAPI (API REST)
- **Base de Datos**: SQLAlchemy ORM
- **Python 3.7+**

## Estructura del Proyecto
```
proyecto_empresariales/
├── streamlit_app.py          # Interfaz principal
├── app/
│   ├── main.py              # Punto de entrada FastAPI
│   ├── api/
│   │   ├── api.py           # Router principal
│   │   └── endpoints/
│   │       └── products.py   # Endpoints CRUD de productos
│   ├── models/
│   │   └── product.py        # Modelo de base de datos
│   ├── schemas/
│   │   └── product.py        # Esquemas de validación
│   ├── services/
│   │   └── product_service.py # Lógica de negocio
│   ├── repositories/
│   │   └── product_repository.py # Acceso a datos
│   ├── db/
│   │   └── session.py        # Configuración de BD
│   ├── core/
│   │   └── config.py         # Configuración
│   └── utils/
│       └── locations.py      # Datos de regiones y comunas
```

## Instalación

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Ejecutar la aplicación (se inicia ambas partes):
```bash
bash run.sh
```
O manualmente:
```bash
# Terminal 1 - Backend (FastAPI)
uvicorn app.main:app --reload --port 8001

# Terminal 2 - Frontend (Streamlit)
streamlit run streamlit_app.py
```

3. Acceder a:
   - **Frontend**: `http://localhost:8501`
   - **API**: `http://localhost:8001`
   - **Docs API**: `http://localhost:8001/docs`

## Uso

### Pestaña: CRUD Pedidos
- **Crear Pedido**: Ingresa datos del cliente, producto, precio, región, comuna y dirección
- **Ver Pedidos**: Tabla con todos los pedidos registrados
- **Actualizar Pedido**: Edita información de un pedido existente
- **Eliminar Pedido**: Elimina pedidos del sistema
- **Seguimiento**: Consulta el estado actual de cada pedido

### Pestaña: Mapa (Próximamente)
Visualización geográfica de entregas

### Pestaña: Configuración
Opciones del sistema

## Campos de un Producto/Pedido
- **ID**: Identificador único
- **Nombre**: Nombre del producto
- **Descripción**: Detalles adicionales
- **Precio**: Precio unitario
- **Cliente**: Nombre del cliente
- **Región**: Región de entrega
- **Comuna**: Comuna específica
- **Dirección de Entrega**: Domicilio completo
- **Estado**: Estado del pedido (Pendiente, En Proceso, Entregado)

## Endpoints de API
```
POST   /api/v1/products              - Crear producto
GET    /api/v1/products              - Listar productos
GET    /api/v1/products/{id}         - Obtener producto
PUT    /api/v1/products/{id}         - Actualizar producto
DELETE /api/v1/products/{id}         - Eliminar producto
```

---
**Aplicación empresarial para gestión integral de pedidos y distribución**
