# Sistema de Seguimiento de Pedidos

## Descripción
Aplicación simple para gestionar pedidos de una empresa de comercio electrónico. Permite registrar pedidos, asignar estados y consultar el estado.

## Funcionalidades
- ✅ **Registrar pedidos**: Se captura información del cliente, producto, cantidad y precio
- ✅ **Asignar estados**: Los pedidos pueden tener tres estados (pendiente → en proceso → entregado)
- ✅ **Consultar estado**: Se pueden ver todos los pedidos con su estado actual
- ✅ **Filtrar por estado**: Consulta pedidos por su estado específico

## Requisitos
- Python 3.7+
- Streamlit
- Pandas

## Instalación

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```
##o le mandas el pip install streamlit nmas

2. Ejecutar la aplicación:
```bash
streamlit run app.py
```

3. Abrir navegador en: `http://localhost:8501`

## Uso

### Pestaña 1: Registrar Pedido
- Completar datos del cliente, producto, cantidad y precio
- Hacer clic en "Registrar Pedido"
- El pedido se crea con estado "pendiente" por defecto

### Pestaña 2: Consultar Pedidos
- Ver tabla con todos los pedidos
- Filtrar por estado si es necesario
- Se muestra: ID, Cliente, Producto, Cantidad, Precio, Estado y Fecha

### Pestaña 3: Cambiar Estado
- Seleccionar un pedido
- Elegir nuevo estado
- Confirmar cambio

## Almacenamiento
Los datos se guardan en archivo JSON (`pedidos.json`) de forma persistente.

## Estructura de un Pedido
```json
{
  "id": 1,
  "cliente": "Juan García",
  "producto": "Laptop Dell",
  "cantidad": 2,
  "precio_total": 4000.00,
  "estado": "pendiente",
  "fecha": "10/04/2026 14:30"
}
```

## Estados Disponibles
- **pendiente**: Pedido registrado, no iniciado
- **en proceso**: Pedido en preparación/envío
- **entregado**: Pedido completado

---
**Proyecto simple y funcional para seguimiento de pedidos empresariales**
