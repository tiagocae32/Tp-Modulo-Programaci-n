# Dashboard de Ventas - Contoso

Este proyecto construye un **dashboard interactivo** basado en datos de ventas de la empresa ficticia Contoso.

## 📊 Dataset seleccionado
Datos públicos de Microsoft:  
[Contoso Data Warehouse Sample](https://github.com/Microsoft/sql-server-samples/tree/master/samples/databases/contoso-data-warehouse)

Tablas utilizadas:
- DimCustomer
- DimProduct
- DimChannel
- DimStore
- DimDate
- DimGeography
- FactSales

## 🛠️ Motor de Base de Datos
Se utilizó **MySQL** como base de datos relacional.

### Creación de la base de datos
```sql
CREATE DATABASE contoso;
