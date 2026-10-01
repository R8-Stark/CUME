import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="SAPCyE | Dashboard Directivo BSC",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------------------------------------------------------
# Datos oficiales del proyecto integrador SAPCyE
# -----------------------------------------------------------------------------
M1_INGRESOS = 6100
M2_INGRESOS = 7500
M3_INGRESOS = 9500
PUNTO_EQUILIBRIO = 5379
MARGEN_CONTRIBUCION = 48.95
COBERTURA_D0 = 0.38
COBERTURA_D90 = 1.68
RESERVA_D0 = 0
RESERVA_D90 = 2633

CRISIS = {
    "ingresos": 3600,
    "costos_directos": 2200,
    "gastos": 2870,
    "resultado": -1470,
    "resistencia": 3.0,
}

MEZCLA_M3 = pd.DataFrame(
    {
        "Servicio": ["Individual", "Pareja", "Talleres", "Familiar"],
        "Participación": [50.5, 21.1, 15.8, 12.6],
    }
)

PLAN_CHOQUE = pd.DataFrame(
    [
        ["Control semanal de efectivo", "Ingresos frente a egresos y efectivo libre.", "Resp. adm.-financiero", "Cumplido"],
        ["Conciliación mensual", "Cierre de ingresos, egresos y anticipos.", "Resp. adm.-financiero", "Cumplido"],
        ["Políticas de anticipos y cobro", "Condiciones escritas por servicio.", "Dirección General", "Cumplido"],
        ["Costeo por servicio", "Separar costos directos e indirectos y calcular margen y equilibrio.", "Dirección General / Resp. adm.", "Cumplido"],
        ["Registro financiero único", "Crear un registro por línea de servicio y conciliar todos los movimientos.", "Resp. adm.-financiero", "Cumplido"],
        ["Modalidad híbrida y cobro digital", "Agenda y pago en línea; sesiones remotas ante lluvias.", "Coord. de servicios", "Cumplido"],
        ["Documentación de procesos y responsables", "Manuales breves, suplencias y facultades de decisión.", "Dirección General", "Cumplido"],
        ["Piloto de orientación vocacional", "Validar precio, margen y demanda con una institución.", "Coord. de servicios", "Cumplido"],
        ["Reserva de contingencia", "Aportaciones mensuales hasta completar $2,633.", "Resp. adm.-financiero", "Cumplido"],
    ],
    columns=["Acción estratégica", "Descripción", "Responsable", "Estatus"],
)

# -----------------------------------------------------------------------------
# CSS - SaaS oscuro
# -----------------------------------------------------------------------------
CSS = """
<style>
:root {
    --bg: #070b12;
    --panel: #0d131d;
    --panel-2: #111925;
    --border: #202b3a;
    --text: #f2f5f8;
    --muted: #8e9aaa;
    --green: #36d399;
    --yellow: #f6c453;
    --red: #ff647c;
    --blue: #61a8ff;
}
.stApp {
    background: radial-gradient(circle at 85% -10%, #15243a 0%, var(--bg) 34%, #060910 100%);
    color: var(--text);
}
.block-container { max-width: 1500px; padding-top: 1.1rem; padding-bottom: 3rem; }
header[data-testid="stHeader"] { background: transparent; }
[data-testid="stToolbar"] { display: none; }

.hero {
    display:flex; align-items:flex-end; justify-content:space-between; gap:1rem;
    padding: 0.4rem 0 1rem 0;
}
.brand { font-size: 1.7rem; font-weight: 800; letter-spacing:-0.03em; }
.subtitle { color:var(--muted); font-size:0.88rem; margin-top:0.25rem; }
.badge {
    display:inline-flex; align-items:center; gap:0.45rem; padding:0.42rem 0.7rem;
    border:1px solid #243247; border-radius:999px; background:#0b111a; color:#b9c4d2;
    font-size:0.76rem; font-weight:700;
}
.dot { width:8px; height:8px; border-radius:50%; display:inline-block; }
.green { background:var(--green); box-shadow:0 0 12px rgba(54,211,153,.45); }
.yellow { background:var(--yellow); box-shadow:0 0 12px rgba(246,196,83,.4); }
.red { background:var(--red); box-shadow:0 0 12px rgba(255,100,124,.4); }
.blue { background:var(--blue); }

.kpi {
    background: linear-gradient(180deg, rgba(18,27,40,.96), rgba(12,18,28,.96));
    border:1px solid var(--border); border-radius:18px; padding:1rem 1.05rem;
    min-height:138px; box-shadow:0 14px 40px rgba(0,0,0,.16);
}
.kpi-top { display:flex; justify-content:space-between; align-items:center; color:var(--muted); font-size:.78rem; font-weight:700; }
.kpi-value { font-size:1.8rem; font-weight:800; letter-spacing:-.035em; margin:.65rem 0 .2rem; }
.kpi-trend { font-size:.75rem; font-weight:700; }
.kpi-trend.green-t { color:var(--green); }
.kpi-trend.yellow-t { color:var(--yellow); }
.kpi-trend.red-t { color:var(--red); }

.section-title { font-size:1.12rem; font-weight:800; margin:1.25rem 0 .65rem; }
.section-caption { color:var(--muted); font-size:.8rem; margin-top:-.35rem; margin-bottom:.8rem; }
.card {
    background:rgba(13,19,29,.88); border:1px solid var(--border); border-radius:18px;
    padding:1rem; box-shadow:0 12px 34px rgba(0,0,0,.13);
}
.strategy {
    border:1px solid var(--border); border-radius:15px; padding:1rem; background:#0d141f;
    min-height:150px; position:relative;
}
.strategy:after { content:"→"; position:absolute; right:-15px; top:50%; transform:translateY(-50%); color:#3a4a5f; font-size:1.35rem; z-index:2; }
.strategy:last-child:after { display:none; }
.strategy .tag { font-size:.7rem; text-transform:uppercase; letter-spacing:.08em; font-weight:800; color:var(--blue); }
.strategy h4 { margin:.45rem 0 .35rem; font-size:.95rem; }
.strategy p { margin:0; color:#aeb8c6; font-size:.78rem; line-height:1.45; }
.strategy .target { margin-top:.7rem; font-size:.75rem; color:#dfe5ec; }

.alert-row { display:flex; gap:.7rem; padding:.65rem 0; border-bottom:1px solid #1b2533; }
.alert-row:last-child { border-bottom:0; }
.alert-text { font-size:.82rem; color:#d4dbe4; line-height:1.4; }

.stTabs [data-baseweb="tab-list"] { gap:.2rem; background:#0a1018; border:1px solid var(--border); padding:.3rem; border-radius:14px; }
.stTabs [data-baseweb="tab"] { border-radius:10px; padding:.55rem 1rem; color:#9ba7b6; font-weight:700; }
.stTabs [aria-selected="true"] { background:#172334 !important; color:#f5f7fa !important; }
.stTabs [data-baseweb="tab-highlight"] { display:none; }

div[data-testid="stMetric"] { background:#0d141f; border:1px solid var(--border); border-radius:14px; padding:.8rem; }
div[data-testid="stMetricLabel"] { color:#8e9aaa; }
div[data-testid="stMetricValue"] { color:#f4f7fa; }

.stSelectbox label { color:#aeb8c6 !important; font-size:.78rem !important; font-weight:700 !important; }
[data-baseweb="select"] > div { background:#0d141f; border-color:#263347; border-radius:12px; }

div[data-testid="stDataFrame"] { border:1px solid var(--border); border-radius:14px; overflow:hidden; }
.small-note { color:#718095; font-size:.72rem; margin-top:.8rem; }
.footer { color:#657387; font-size:.72rem; text-align:right; margin-top:1.5rem; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


def money(value: float) -> str:
    return f"${value:,.0f} MXN"


def kpi_card(title: str, value: str, trend: str, tone: str = "green") -> None:
    st.markdown(
        f"""
        <div class="kpi">
            <div class="kpi-top"><span>{title}</span><span class="dot {tone}"></span></div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-trend {tone}-t">{trend}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def strategy_card(tag: str, title: str, body: str, target: str) -> None:
    st.markdown(
        f"""
        <div class="strategy">
            <div class="tag">{tag}</div>
            <h4>{title}</h4>
            <p>{body}</p>
            <div class="target">{target}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def alert_item(tone: str, text_value: str) -> None:
    st.markdown(
        f'<div class="alert-row"><span class="dot {tone}"></span><div class="alert-text">{text_value}</div></div>',
        unsafe_allow_html=True,
    )


def money_chart_base() -> go.Figure:
    months = ["M1", "M2", "M3"]
    ingresos = [M1_INGRESOS, M2_INGRESOS, M3_INGRESOS]
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Ingresos", x=months, y=ingresos, marker_color="#61a8ff", hovertemplate="%{x}: $%{y:,.0f}<extra></extra>"))
    fig.add_trace(go.Scatter(name="Punto de equilibrio", x=months, y=[PUNTO_EQUILIBRIO] * 3, mode="lines+markers", line=dict(color="#ff647c", width=3), hovertemplate="PE: $%{y:,.0f}<extra></extra>"))
    fig.update_layout(
        template="plotly_dark", height=390, margin=dict(l=10, r=10, t=25, b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=1.01, x=0),
        yaxis=dict(tickprefix="$", separatethousands=True, gridcolor="#1d2837", zeroline=False),
        xaxis=dict(gridcolor="rgba(0,0,0,0)"),
        hoverlabel=dict(bgcolor="#101925"),
    )
    return fig


def money_chart_crisis() -> go.Figure:
    categories = ["Ingresos", "Costos directos", "Gastos básicos", "Resultado"]
    values = [CRISIS["ingresos"], CRISIS["costos_directos"], CRISIS["gastos"], CRISIS["resultado"]]
    fig = go.Figure(go.Bar(
        x=categories, y=values,
        marker_color=["#61a8ff", "#f6c453", "#a78bfa", "#ff647c"],
        hovertemplate="%{x}: $%{y:,.0f}<extra></extra>",
    ))
    fig.add_hline(y=0, line_width=1, line_color="#4b596c")
    fig.update_layout(
        template="plotly_dark", height=390, margin=dict(l=10, r=10, t=25, b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(tickprefix="$", separatethousands=True, gridcolor="#1d2837", zeroline=False),
        xaxis=dict(gridcolor="rgba(0,0,0,0)"),
    )
    return fig


def mix_chart() -> go.Figure:
    fig = px.pie(MEZCLA_M3, names="Servicio", values="Participación", hole=.62)
    fig.update_traces(texttemplate="%{label}<br>%{value:.1f}%", textposition="outside", hovertemplate="%{label}: %{value:.1f}%<extra></extra>")
    fig.update_layout(
        template="plotly_dark", height=420, margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
    )
    return fig


# -----------------------------------------------------------------------------
# Encabezado
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <div>
            <div class="brand">SAPCyE <span style="color:#52647b">/</span> Dashboard Directivo BSC</div>
            <div class="subtitle">War Room Empresarial · Diagnóstico Estratégico y Plan de Rescate Financiero · Día 90</div>
        </div>
        <div class="badge"><span class="dot green"></span>Modelo académico · Corte Día 90</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# Navegación superior
# -----------------------------------------------------------------------------
t1, t2, t3, t4 = st.tabs(["Resumen C-Level", "Financiero", "Cliente", "Operación y Talento"])

with t1:
    st.markdown('<div class="section-title">Indicadores ejecutivos</div>', unsafe_allow_html=True)
    cols = st.columns(4, gap="medium")
    with cols[0]: kpi_card("Ingresos Mensuales M3", money(M3_INGRESOS), "↑ meta cumplida · Día 90", "green")
    with cols[1]: kpi_card("Margen de Contribución", "48.95%", "↑ meta ≥ 45% · Día 90", "green")
    with cols[2]: kpi_card("Cobertura de Gasto Básico", "1.68 meses", "↑ 0.38 → 1.68 meses", "green")
    with cols[3]: kpi_card("Reserva de Contingencia", money(RESERVA_D90), "↑ $0 → $2,633", "green")

    st.markdown('<div class="section-title">Mapa estratégico · causa y efecto</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-caption">Cadena BSC: Aprendizaje → Procesos → Cliente → Financiera.</div>', unsafe_allow_html=True)
    c = st.columns(4, gap="small")
    with c[0]:
        strategy_card("Aprendizaje y crecimiento", "Reducir dependencia de fundadora", "Documentar procesos críticos y delegar capacidades de decisión.", "5 de 5 procesos documentados")
    with c[1]:
        strategy_card("Procesos internos", "Información confiable", "Registrar, conciliar y costear la operación para sostener decisiones trazables.", "100% movimientos · 4 servicios costeados")
    with c[2]:
        strategy_card("Cliente", "Construir demanda recurrente", "Fortalecer continuidad de usuarios y ocupación de talleres.", "Continuidad ≥ 50% · Ocupación ≥ 80%")
    with c[3]:
        strategy_card("Financiera", "Lograr rentabilidad y liquidez sostenibles", "Convertir la mejora operativa en flujo y reserva.", "Ingresos $9,500 · Margen ≥ 45%")

    st.markdown('<div class="section-title">Alertas recientes</div>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    alert_item("green", "Cobertura de efectivo subió de 0.38 a 1.68 meses tras el plan de 90 días.")
    alert_item("green", "Se completó la meta de reserva de contingencia acumulando $2,633 MXN.")
    alert_item("yellow", "Alerta de riesgo: alta concentración de ingresos en psicología (84.2% del total).")
    alert_item("green", "Mitigación del Talón de Aquiles: 5 de 5 procesos críticos documentados formalmente.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="small-note">Nota: las cifras del proyecto corresponden a un modelo académico con supuestos explícitos y no a estados financieros históricos.</div>', unsafe_allow_html=True)

with t2:
    st.markdown('<div class="section-title">Stress Test financiero</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-caption">Alterna el modelo base y el escenario pesimista combinado del mes 3.</div>', unsafe_allow_html=True)
    escenario = st.selectbox("Escenario", ["Escenario Base", "Escenario de Crisis (Stress Test)"], index=0, key="escenario")

    if escenario == "Escenario Base":
        a, b = st.columns([1, 2.25], gap="large")
        with a:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.metric("M3 ingresos", money(M3_INGRESOS))
            st.metric("Punto de equilibrio", money(PUNTO_EQUILIBRIO))
            st.metric("Resultado M3", money(2017))
            st.markdown('<div class="small-note">Margen de seguridad M3 básico: 43.4%.</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with b:
            st.plotly_chart(money_chart_base(), use_container_width=True, config={"displayModeBar": False})
    else:
        st.error("Stress Test activo: el escenario pesimista combinado genera un resultado mensual de -$1,470 MXN.")
        a, b = st.columns([1, 2.25], gap="large")
        with a:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.metric("Ingresos M3 crisis", money(CRISIS["ingresos"]))
            st.metric("Gastos básicos", money(CRISIS["gastos"]))
            st.metric("Resultado mensual", money(CRISIS["resultado"]))
            st.markdown('<div class="small-note">La caja libre de $4,411 resistiría aproximadamente 3.0 meses bajo este esquema, si el choque ocurre después del día 90.</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with b:
            st.plotly_chart(money_chart_crisis(), use_container_width=True, config={"displayModeBar": False})

    st.markdown('<div class="section-title">Lectura ejecutiva</div>', unsafe_allow_html=True)
    st.markdown('<div class="card">El escenario base alcanza $9,500 de ingresos en M3 frente a un punto de equilibrio básico de $5,379. El stress test combina caída de demanda, reducción de tarifa y aumento de costos; el pesimista combinado lleva los ingresos a $3,600 y el resultado mensual a -$1,470.</div>', unsafe_allow_html=True)

with t3:
    st.markdown('<div class="section-title">Cliente · mezcla de ingresos M3</div>', unsafe_allow_html=True)
    left, right = st.columns([1.1, 1.5], gap="large")
    with left:
        st.plotly_chart(mix_chart(), use_container_width=True, config={"displayModeBar": False}, key="mix_cliente")
    with right:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("**Composición del ingreso mensual M3**")
        df_mix = MEZCLA_M3.copy()
        df_mix["Participación"] = df_mix["Participación"].map(lambda x: f"{x:.1f}%")
        st.dataframe(df_mix, hide_index=True, use_container_width=True)
        st.markdown('<div class="small-note">La mezcla reproduce los $9,500 del M3: individual $4,800; pareja $2,000; familiar $1,200; talleres $1,500.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Seguimiento del plan de choque</div>', unsafe_allow_html=True)
    st.dataframe(PLAN_CHOQUE, hide_index=True, use_container_width=True, column_config={"Estatus": st.column_config.TextColumn("Estatus")})

with t4:
    st.markdown('<div class="section-title">Operación y talento · capacidad de ejecución</div>', unsafe_allow_html=True)
    a, b, c = st.columns(3, gap="medium")
    with a: kpi_card("Procesos críticos documentados", "5 de 5", "Meta cumplida · Día 90", "green")
    with b: kpi_card("Servicios costeados", "4 de 4", "Meta del día 45 cumplida", "green")
    with c: kpi_card("Movimientos conciliados", "100%", "Meta cumplida · Día 90", "green")

    left, right = st.columns([1.1, 1.5], gap="large")
    with left:
        st.markdown('<div class="section-title">Mezcla de ingresos M3</div>', unsafe_allow_html=True)
        st.plotly_chart(mix_chart(), use_container_width=True, config={"displayModeBar": False}, key="mix_operacion")
    with right:
        st.markdown('<div class="section-title">Plan de choque · estatus</div>', unsafe_allow_html=True)
        st.dataframe(PLAN_CHOQUE, hide_index=True, use_container_width=True)

    st.markdown('<div class="card"><b>Talón de Aquiles mitigado:</b> la documentación, designación de responsables y registro único buscan reducir la concentración de la operación y el conocimiento en la persona fundadora.</div>', unsafe_allow_html=True)

st.markdown('<div class="footer">SAPCyE · Dashboard Directivo BSC · Modelo académico · Día 90</div>', unsafe_allow_html=True)
