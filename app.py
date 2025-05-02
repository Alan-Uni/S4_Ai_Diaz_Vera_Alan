import streamlit as st
import pandas as pd
from datetime import datetime

st.title("Sistema Contable Componentes TUX")

st.markdown(
    """
    <style>,m,
    .stDataFrame {
        background-color: #001F3F;
        color: #FFD700;
    }
    .stDataFrame th {
        background-color: #001F3F;
        color: #FFD700;
    }
    .stDataFrame td {
        background-color: #001F3F;
        color: #FFD700;
    }
    .stNumberInput label {
        color: #FFD700 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

if 'transacciones' not in st.session_state:
    st.session_state.transacciones = []
    
if 'balances' not in st.session_state:
    st.session_state.balances = {
        "Activo": {
            "Caja": 22102.00, 
            "Bancos": 0.00,
            "Compras": 0.00,
            "Descuentos Compras": 0.00,
            "Devoluciones Compras": 0.00,
            "Rebajas Compras": 0.00,
            "IVA acreditable": 0.00
        },
        "Pasivo": {
            "Ventas": 0.00,
            "Descuentos Ventas": 0.00,
            "Devoluciones Ventas": 0.00,
            "Rebajas Ventas": 0.00,
            "IVA trasladado": 0.00
        }
    }

def actualizar_balances(transaccion):
    for cuenta, monto in transaccion["cargos"].items():
        if cuenta in st.session_state.balances["Activo"]:
            st.session_state.balances["Activo"][cuenta] += monto
        elif cuenta in st.session_state.balances["Pasivo"]:
            st.session_state.balances["Pasivo"][cuenta] += monto

    for cuenta, monto in transaccion["abonos"].items():
        if cuenta in st.session_state.balances["Activo"]:
            st.session_state.balances["Activo"][cuenta] -= monto
        elif cuenta in st.session_state.balances["Pasivo"]:
            st.session_state.balances["Pasivo"][cuenta] -= monto
            
def generar_transaccion(tipo, cargos, abonos):
    return {
        "fecha": datetime.now().strftime("%d/%m/%Y"),
        "tipo": tipo,
        "cargos": cargos,
        "abonos": abonos
    }
def mostrar_firmas():
    col1, col2 = st.columns(2)
    
    with col1:
        
        st.markdown("**Propietario**")
        st.image("./firmas/firma_propietario.png", width=150)  
        st.markdown("Alan Díaz Vera")
        st.markdown("""<div style="border-bottom: 2px solid black; width: 80%;"></div>""", 
                   unsafe_allow_html=True)
    
    with col2:
        st.markdown("**Revisó**")
        st.image("./firmas/firma_revisor.png", width=150)  
        st.markdown("Nuria González Zúñiga")
        st.markdown("""<div style="border-bottom: 2px solid black; width: 80%;"></div>""", 
                   unsafe_allow_html=True)
        
def mostrar_firmas2():
    col1, col2, col3 = st.columns(3)
    
    with col1:
        
        st.markdown("**Propietario**")
        st.image("./firmas/firma_propietario.png", width=150)  
        st.markdown("Alan Díaz Vera")
        st.markdown("""<div style="border-bottom: 2px solid black; width: 80%;"></div>""", 
                   unsafe_allow_html=True)
    with col2:
        
        st.markdown("**Cajero**")
        st.image("./firmas/firma_cajero.png", width=150)  
        st.markdown("Alberto Rasgado Ramirez")
        st.markdown("""<div style="border-bottom: 2px solid black; width: 80%;"></div>""", 
                   unsafe_allow_html=True)
    with col3:
        st.markdown("**Revisó**")
        st.image("./firmas/firma_revisor.png", width=150)  
        st.markdown("Nuria González Zúñiga")
        st.markdown("""<div style="border-bottom: 2px solid black; width: 80%;"></div>""", 
                   unsafe_allow_html=True)
        
with st.sidebar:
    st.header("Transacciones")
    opcion = st.selectbox(
        "Seleccione transacción:",
        ["Traspaso a bancos", "Compra con IVA", "Descuento compra",
         "Venta con IVA", "Descuento venta", "Devolución compra",
         "Devolución venta", "Rebaja compra", "Rebaja venta"]
    )

if opcion == "Traspaso a bancos":
    with st.form("Traspaso"):
        monto = st.number_input("Monto a transferir", value=22102.00)
        if st.form_submit_button("Registrar"):
            transaccion = generar_transaccion(
                "Traspaso bancos",
                {"Bancos": monto},
                {"Caja": monto}
            )
            st.session_state.transacciones.append(transaccion)
            actualizar_balances(transaccion)

elif opcion == "Compra con IVA":
    with st.form("Compra IVA"):
        compra = st.number_input("Monto de compra", value=2000.00)
        iva = compra * 0.16
        total = compra + iva
        if st.form_submit_button("Registrar"):
            transaccion = generar_transaccion(
                "Compra con IVA",
                {"Compras": compra, "IVA acreditable": iva},
                {"Bancos": total}
            )
            st.session_state.transacciones.append(transaccion)
            actualizar_balances(transaccion)

elif opcion == "Descuento compra":
    with st.form("Descuento Compra"):
        descuento = st.number_input("Monto de descuento", value=200.00)
        iva_desc = descuento * 0.16
        if st.form_submit_button("Registrar"):
            transaccion = generar_transaccion(
                "Descuento compra",
                {"Bancos": descuento + iva_desc},
                {"Descuentos Compras": descuento, "IVA acreditable": iva_desc}
            )
            st.session_state.transacciones.append(transaccion)
            actualizar_balances(transaccion)

elif opcion == "Venta con IVA":
    with st.form("Venta IVA"):
        venta = st.number_input("Monto de venta", value=6000.00)
        iva = venta * 0.16
        total = venta + iva
        if st.form_submit_button("Registrar"):
            transaccion = generar_transaccion(
                "Venta con IVA",
                {"Bancos": total},
                {"Ventas": venta, "IVA trasladado": iva}
            )
            st.session_state.transacciones.append(transaccion)
            actualizar_balances(transaccion)

elif opcion == "Descuento venta":
    with st.form("Descuento Venta"):
        descuento = st.number_input("Monto de descuento", value=480.00)
        iva_desc = descuento * 0.16
        if st.form_submit_button("Registrar"):
            transaccion = generar_transaccion(
                "Descuento venta",
                {"Descuentos Ventas": descuento, "IVA trasladado": iva_desc},
                {"Bancos": descuento + iva_desc}
            )
            st.session_state.transacciones.append(transaccion)
            actualizar_balances(transaccion)

elif opcion == "Devolución compra":
    with st.form("Devolución Compra"):
        monto = st.number_input("Monto devolución", value=600.00)
        iva_dev = monto * 0.16
        if st.form_submit_button("Registrar"):
            transaccion = generar_transaccion(
                "Devolución compra",
                {"Bancos": monto + iva_dev},
                {"Devoluciones Compras": monto, "IVA acreditable": iva_dev}
            )
            st.session_state.transacciones.append(transaccion)
            actualizar_balances(transaccion)

elif opcion == "Devolución venta":
    with st.form("Devolución Venta"):
        monto = st.number_input("Monto devolución", value=3000.00)
        iva_dev = monto * 0.16
        if st.form_submit_button("Registrar"):
            transaccion = generar_transaccion(
                "Devolución venta",
                {"Devoluciones Ventas": monto, "IVA trasladado": iva_dev},
                {"Bancos": monto + iva_dev}
            )
            st.session_state.transacciones.append(transaccion)
            actualizar_balances(transaccion)

elif opcion == "Rebaja compra":
    with st.form("Rebaja Compra"):
        monto = st.number_input("Monto rebaja", value=1000.00)
        iva_reb = monto * 0.16
        if st.form_submit_button("Registrar"):
            transaccion = generar_transaccion(
                "Rebaja compra",
                {"Bancos": monto + iva_reb},
                {"Rebajas Compras": monto, "IVA acreditable": iva_reb}
            )
            st.session_state.transacciones.append(transaccion)
            actualizar_balances(transaccion)

elif opcion == "Rebaja venta":
    with st.form("Rebaja Venta"):
        monto = st.number_input("Monto rebaja", value=1000.00)
        iva_reb = monto * 0.16
        if st.form_submit_button("Registrar"):
            transaccion = generar_transaccion(
                "Rebaja venta",
                {"Rebajas Ventas": monto, "IVA trasladado": iva_reb},
                {"Bancos": monto + iva_reb}
            )
            st.session_state.transacciones.append(transaccion)
            actualizar_balances(transaccion)






st.header("Reportes Contables Sucursal")
st.subheader("Arqueo de Caja ")

monedas_base = {
    "Denominación": [0.5, 1, 2, 5, 10, 20],
    "Cantidad": [10, 17, 20, 28, 20, 10]
}

billetes_base = {
    "Denominación": [20, 50, 100, 500, 1000],
    "Cantidad": [25, 40, 30, 20, 6]
}

col1, col2 = st.columns(2)
with col1:
    st.write("**Monedas**")
    monedas_edit = st.data_editor(
        pd.DataFrame(monedas_base),
        column_config={
            "Denominación": st.column_config.NumberColumn(
                format="$%.2f",
                help="Denominación de la moneda"
            ),
            "Cantidad": st.column_config.NumberColumn(
                format="%d unidades",
                help="Cantidad física de monedas"
            )
        },
        num_rows="fixed"  
    )
    monedas_edit["Total"] = monedas_edit["Denominación"] * monedas_edit["Cantidad"]

with col2:
    st.write("**Billetes**")
    billetes_edit = st.data_editor(
        pd.DataFrame(billetes_base),
        column_config={
            "Denominación": st.column_config.NumberColumn(
                format="$%.2f",
                help="Denominación del billete"
            ),
            "Cantidad": st.column_config.NumberColumn(
                format="%d unidades",
                help="Cantidad física de billetes"
            )
        },
        num_rows="fixed"  
    )
    billetes_edit["Total"] = billetes_edit["Denominación"] * billetes_edit["Cantidad"]

total_caja = monedas_edit["Total"].sum() + billetes_edit["Total"].sum()
st.write(f"**Total en Caja:** ${total_caja:,.2f}")
mostrar_firmas2()




st.subheader("Libro Diario")
libro_diario_rows = []
for idx, t in enumerate(st.session_state.transacciones, start=1):
    fecha = t["fecha"]
    
    for cuenta, monto in t["cargos"].items():
        libro_diario_rows.append({
            "FECHA": fecha,
            "CUENTAS": cuenta,
            "Num de transacción": idx,  
            "DEBE": monto,
            "HABER": 0.00
        })
    
    for cuenta, monto in t["abonos"].items():
        libro_diario_rows.append({
            "FECHA": fecha,
            "CUENTAS": cuenta,
            "Num de transacción": idx,  
            "DEBE": 0.00,
            "HABER": monto
        })

libro_diario = pd.DataFrame(libro_diario_rows)
libro_diario = libro_diario.rename(columns={
    "Num de transacción": "Num de transacción"  # Forzar nombre consistente
})[["FECHA", "CUENTAS", "Num de transacción", "DEBE", "HABER"]]

totales = pd.DataFrame({
    "FECHA": ["Total"],
    "CUENTAS": [""],
    "Num de transacción": [""],
    "DEBE": [libro_diario["DEBE"].sum()],
    "HABER": [libro_diario["HABER"].sum()]
})

libro_diario = pd.concat([libro_diario, totales], ignore_index=True)
st.dataframe(libro_diario)





st.subheader("Libro Mayor ")
cuentas_mayor = {
    "Caja": {"Debe": [], "Haber": []},
    "Bancos": {"Debe": [], "Haber": []},
    "Compras": {"Debe": [], "Haber": []},
    "Descuentos Compras": {"Debe": [], "Haber": []},
    "Devoluciones Compras": {"Debe": [], "Haber": []},
    "Rebajas Compras": {"Debe": [], "Haber": []},
    "IVA acreditable": {"Debe": [], "Haber": []},  
    "Ventas": {"Debe": [], "Haber": []},
    "Descuentos Ventas": {"Debe": [], "Haber": []},
    "Devoluciones Ventas": {"Debe": [], "Haber": []},
    "Rebajas Ventas": {"Debe": [], "Haber": []},
    "IVA trasladado": {"Debe": [], "Haber": []},  
}


for t in st.session_state.transacciones:
    for cuenta, monto in t["cargos"].items():
        if cuenta not in cuentas_mayor:  
            cuentas_mayor[cuenta] = {"Debe": [], "Haber": []}
        cuentas_mayor[cuenta]["Debe"].append(abs(monto))
        cuentas_mayor[cuenta]["Haber"].append(0.00)
    
    for cuenta, monto in t["abonos"].items():
        if cuenta not in cuentas_mayor:  
            cuentas_mayor[cuenta] = {"Debe": [], "Haber": []}
        cuentas_mayor[cuenta]["Haber"].append(abs(monto))
        cuentas_mayor[cuenta]["Debe"].append(0.00)

for cuenta, movimientos in cuentas_mayor.items():
    st.markdown(f"**{cuenta}**")
    
   
    max_len = max(len(movimientos["Debe"]), len(movimientos["Haber"]))
    
    movimientos["Debe"] += [0.00] * (max_len - len(movimientos["Debe"]))
    movimientos["Haber"] += [0.00] * (max_len - len(movimientos["Haber"]))
    
    df = pd.DataFrame({
        "Debe": movimientos["Debe"],
        "Haber": movimientos["Haber"]
    })
    
    st.dataframe(df)
    st.write(f"**Saldo:** ${sum(df['Debe']) - sum(df['Haber']):,.2f}")
    st.markdown("---")



st.subheader("Balanza de Comprobación ")

balanza_data = []
for cuenta in cuentas_mayor:
    mov_debe = sum(cuentas_mayor[cuenta]["Debe"])
    mov_haber = sum(cuentas_mayor[cuenta]["Haber"])
    
    saldo_debe = max(mov_debe - mov_haber, 0)  
    saldo_haber = max(mov_haber - mov_debe, 0)  
    
    balanza_data.append({
        "Cuenta": cuenta,
        "Mov_Debe": mov_debe,
        "Mov_Haber": mov_haber,
        "Saldo_Debe": saldo_debe if saldo_debe > 0 else "",
        "Saldo_Haber": saldo_haber if saldo_haber > 0 else ""
    })

df_balanza = pd.DataFrame(balanza_data)

total_mov_debe = df_balanza["Mov_Debe"].sum()
total_mov_haber = df_balanza["Mov_Haber"].sum()
total_saldo_debe = df_balanza["Saldo_Debe"].replace("", 0).astype(float).sum()
total_saldo_haber = df_balanza["Saldo_Haber"].replace("", 0).astype(float).sum()

totales = pd.DataFrame([{
    "Cuenta": "Total",
    "Mov_Debe": total_mov_debe,
    "Mov_Haber": total_mov_haber,
    "Saldo_Debe": total_saldo_debe,
    "Saldo_Haber": total_saldo_haber
}])

df_final = pd.concat([df_balanza, totales], ignore_index=True)

st.dataframe(
    df_final,
    column_config={
        "Cuenta": "Cuenta",
        "Mov_Debe": st.column_config.NumberColumn("Movimientos Debe", format="$%.2f"),
        "Mov_Haber": st.column_config.NumberColumn("Movimientos Haber", format="$%.2f"),
        "Saldo_Debe": st.column_config.NumberColumn("Saldos Debe", format="$%.2f"),
        "Saldo_Haber": st.column_config.NumberColumn("Saldos Haber", format="$%.2f")
    },
    hide_index=True
)


st.subheader("Estado de Resultados ")

ventas_totales = abs(st.session_state.balances["Pasivo"]["Ventas"])
descuentos_ventas = abs(st.session_state.balances["Pasivo"]["Descuentos Ventas"])
devoluciones_ventas = abs(st.session_state.balances["Pasivo"]["Devoluciones Ventas"])
rebajas_ventas = abs(st.session_state.balances["Pasivo"]["Rebajas Ventas"])
ventas_netas = ventas_totales - descuentos_ventas - devoluciones_ventas - rebajas_ventas

compras = abs(st.session_state.balances["Activo"]["Compras"])
gastos_compras = 0.00  
compras_totales = compras + gastos_compras

devoluciones_compra = abs(st.session_state.balances["Activo"]["Devoluciones Compras"])
descuentos_compra = abs(st.session_state.balances["Activo"]["Descuentos Compras"])
rebajas_compra = abs(st.session_state.balances["Activo"]["Rebajas Compras"])
compras_netas = compras_totales - devoluciones_compra - descuentos_compra - rebajas_compra

mercancia_disponible = compras_netas  
inventario_final = compras_netas*0.03
costo_ventas = mercancia_disponible - inventario_final

utilidad_bruta = ventas_netas - costo_ventas

gastos_operacion_venta = 0.00
gastos_operacion_admin = 0.00
utilidad_operacion = utilidad_bruta - (gastos_operacion_venta + gastos_operacion_admin)

estado_data = [
    {"Concepto": "Ventas totales", "1": "", "2": "", "3": ventas_totales, "4": ""},
    {"Concepto": "Descuentos sobre Ventas", "1": "", "2": descuentos_ventas, "3": "", "4": ""},
    {"Concepto": "Devoluciones y Rebajas sobre Ventas", "1": "", "2": devoluciones_ventas + rebajas_ventas, "3": devoluciones_ventas + rebajas_ventas+ descuentos_ventas, "4": ""},
    {"Concepto": "Ventas Netas", "1": "", "2": "", "3": "", "4": ventas_netas},
    {"Concepto": "Inventario inicial", "1": "", "2": "", "3": 0.00, "4": ""},
    {"Concepto": "Compras", "1": compras, "2": "", "3": "", "4": ""},
    {"Concepto": "Gastos de compras", "1": gastos_compras, "2": "", "3": "", "4": ""},
    {"Concepto": "Compras Totales", "1": "", "2": compras_totales, "3": "", "4": ""},
    {"Concepto": "Devoluciones sobre Compra", "1": devoluciones_compra, "2": "", "3": "", "4": ""},
    {"Concepto": "Descuentos sobre Compra", "1": descuentos_compra, "2": "", "3": "", "4": ""},
    {"Concepto": "Rebajas sobre Compra", "1": rebajas_compra, "2": rebajas_compra+descuentos_compra+devoluciones_compra, "3": "", "4": ""},
    {"Concepto": "Compras netas", "1": "", "2": "", "3": compras_netas, "4": ""},
    {"Concepto": "Mercancías Disponibles", "1": "", "2": "", "3": mercancia_disponible, "4": ""},
    {"Concepto": "Inventario final", "1": "", "2": "", "3": inventario_final, "4": ""},
    {"Concepto": "Costo de ventas", "1": "", "2": "", "3":"", "4":  costo_ventas},
    {"Concepto": "Utilidad bruta", "1": "", "2": "", "3": "", "4": utilidad_bruta},
    {"Concepto": "Gastos de operación", "1": "", "2": "", "3": "", "4": ""},
    {"Concepto": "Gastos de Venta", "1": "", "2": "", "3": gastos_operacion_venta, "4": ""},
    {"Concepto": "Gastos de administración", "1": "", "2": "", "3": gastos_operacion_admin, "4": gastos_operacion_admin+gastos_operacion_venta},
    {"Concepto": "Utilidad por Operación", "1": "", "2": "", "3": "", "4": utilidad_operacion},
    {"Concepto": "Otros ingresos y Gastos", "1": "", "2": "", "3": "", "4": ""},
    {"Concepto": "Donaciones", "1": "", "2": "", "3": 0.00, "4": ""},
    {"Concepto": "Pérdida en Venta de Inmuebles", "1": "", "2": "", "3": 0.00, "4": 0.00},
    {"Concepto": "", "1": "", "2": "", "3": "", "4": utilidad_operacion},
]

estado_resultados = pd.DataFrame(estado_data).set_index("Concepto")

def formatear_moneda(valor):
    return f"$ {valor:,.2f}" if isinstance(valor, (int, float)) else ""

estado_formateado = estado_resultados.copy()
for col in ["1", "2", "3", "4"]:
    estado_formateado[col] = estado_formateado[col].apply(formatear_moneda)

st.markdown("""
<style>
.dataframe td {
    text-align: right;
    border: 1px solid #FFD700;
}
.dataframe th {
    display: none;
}
</style>
""", unsafe_allow_html=True)

st.dataframe(estado_formateado, use_container_width=True)
mostrar_firmas()