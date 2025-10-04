import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

# ----------------------------
# Cargar Tablas
# ----------------------------
DimCustomer = pd.read_csv('../data/DimCustomer.csv')
DimProduct = pd.read_csv('../data/DimProduct.csv')
DimChannel = pd.read_csv('../data/DimChannel.csv')
DimStore = pd.read_csv('../data/DimStore.csv')
DimDate = pd.read_csv('../data/DimDate.csv')
DimGeography = pd.read_csv('../data/DimGeography.csv')
FactSales = pd.read_csv('../data/FactSales.csv')

## 2. Conexión a la base de datos

# USER = "root"
# PASSWORD = ""
# HOST = "localhost"
# DB = "contoso"

# engine = create_engine(f"mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}/{DB}")

# ----------------------------
# Guardar en MySQL
# ----------------------------
#DimCustomer.to_sql('DimCustomer', engine, index=False, if_exists='replace')
#DimProduct.to_sql('DimProduct', engine, index=False, if_exists='replace')
#DimChannel.to_sql('DimChannel', engine, index=False, if_exists='replace')
#DimStore.to_sql('DimStore', engine, index=False, if_exists='replace')
#DimDate.to_sql('DimDate', engine, index=False, if_exists='replace')
#DimGeography.to_sql('DimGeography', engine, index=False, if_exists='replace')
#FactSales.to_sql('FactSales', engine, index=False, if_exists='replace')


# FactSales = pd.read_sql("SELECT * FROM FactSales", engine)
# DimProduct = pd.read_sql("SELECT * FROM DimProduct", engine)
# DimChannel = pd.read_sql("SELECT * FROM DimChannel", engine)
# DimStore = pd.read_sql("SELECT * FROM DimStore", engine)
# DimDate = pd.read_sql("SELECT * FROM DimDate", engine)

# ----------------------------
# Procesamiento DimDate
# ----------------------------
DimDate['DateKey'] = pd.to_datetime(DimDate['DateKey'], format='%Y-%m-%d')
DimDate['year'] = DimDate['DateKey'].dt.year
DimDate['month'] = DimDate['DateKey'].dt.month
DimDate['day'] = DimDate['DateKey'].dt.day
DimDate = DimDate[['DateKey', 'year', 'month', 'day']]

# ----------------------------
# Procesamiento FactSales
# ----------------------------
FactSales['DateKey'] = pd.to_datetime(FactSales['DateKey'], format='%Y-%m-%d')
FactSales = FactSales.rename(columns={'channelKey': 'ChannelKey'})
FactSales['year_month'] = FactSales['DateKey'].dt.to_period('M').astype(str)
FactSales['year'] = FactSales['DateKey'].dt.year
FactSales['month'] = FactSales['DateKey'].dt.month

# ---------------------------- # Guardar en MYSQL # ---------------------------- 
# Conexión a MySQL
engine = create_engine("mysql+mysqlconnector://root:@localhost/contoso")

# Guardar tablas en MySQL
DimCustomer.to_sql('DimCustomer', engine, index=False, if_exists='replace')
DimProduct.to_sql('DimProduct', engine, index=False, if_exists='replace')
DimChannel.to_sql('DimChannel', engine, index=False, if_exists='replace')
DimStore.to_sql('DimStore', engine, index=False, if_exists='replace')
DimDate.to_sql('DimDate', engine, index=False, if_exists='replace')
FactSales.to_sql('FactSales', engine, index=False, if_exists='replace')


# ----------------------------
# Funciones de Visualización
# ----------------------------

def grafico_ventas_mensuales(df):
    ventas_mensuales = df.groupby('year_month')['SalesAmount'].sum().reset_index()
    fig = px.line(ventas_mensuales, x='year_month', y='SalesAmount',
                  title='Evolución Mensual de Ventas')
    fig.show()


def grafico_top_productos(df, dim_product, top_n=10):
    ventas_productos = df.groupby('ProductKey')['SalesAmount'].sum().reset_index()
    ventas_productos = ventas_productos.merge(dim_product[['ProductKey', 'ProductName']], on='ProductKey', how='left')
    top_productos = ventas_productos.sort_values(by='SalesAmount', ascending=False).head(top_n)

    fig = px.bar(top_productos, x='ProductName', y='SalesAmount',
                 title=f'Top {top_n} Productos más Vendidos',
                 labels={'ProductName': 'Producto', 'SalesAmount': 'Monto de Ventas'})
    fig.show()


def grafico_ventas_canal(df, dim_channel):
    ventas_canal = df.groupby('ChannelKey')['SalesAmount'].sum().reset_index()
    ventas_canal = ventas_canal.merge(dim_channel[['ChannelKey', 'ChannelName']], on='ChannelKey', how='left')

    fig = px.pie(ventas_canal, names='ChannelName', values='SalesAmount',
                 title='Distribución de Ventas por Canal')
    fig.show()

def grafico_heatmap(df):
    heatmap = df.groupby(['year', 'month'])['SalesAmount'].sum().reset_index()

    fig = px.density_heatmap(heatmap, x='month', y='year', z='SalesAmount',
                             title='Mapa de Calor de Ventas (Año vs Mes)',
                             labels={'month': 'Mes', 'year': 'Año', 'SalesAmount': 'Monto Ventas'},
                             color_continuous_scale='plotly3')
    fig.show()


# ----------------------------
# Dashboard: Ejecutar todo
# ----------------------------

def ejecutar_dashboard():
    grafico_ventas_mensuales(FactSales)
    grafico_top_productos(FactSales, DimProduct)
    grafico_ventas_canal(FactSales, DimChannel)
    grafico_heatmap(FactSales)


# ----------------------------
# Llamada principal
# ----------------------------
if __name__ == "__main__":
    ejecutar_dashboard()
