```python
import streamlit as st
from datetime import datetime

# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================
st.set_page_config(
    page_title="Transfelog App",
    page_icon="T",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CSS - DESIGN MODERNO, CLEAN, GRADIENTES
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    .stApp {
        background: linear-gradient(160deg, #f0f4f7 0%, #e8eef3 50%, #f5f8fa 100%);
        font-family: 'Inter', sans-serif;
    }

    /* Header */
    .app-header {
        background: linear-gradient(135deg, #1a2332 0%, #243447 40%, #4A9BA8 100%);
        padding: 1.8rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 12px 40px rgba(74, 155, 168, 0.2);
        display: flex;
        align-items: center;
        gap: 1.2rem;
    }
    .logo-mark {
        width: 48px;
        height: 48px;
        position: relative;
    }
    .logo-t {
        width: 24px;
        height: 28px;
        background: linear-gradient(135deg, #b8c4cc 0%, #8a9baa 100%);
        transform: skewX(-12deg);
        position: absolute;
        top: 4px;
        left: 4px;
        border-radius: 3px;
    }
    .logo-f {
        width: 24px;
        height: 28px;
        background: linear-gradient(135deg, #4A9BA8 0%, #3a7f8a 100%);
        transform: skewX(-12deg);
        position: absolute;
        bottom: 4px;
        right: 4px;
        border-radius: 3px;
    }
    .header-info {
        flex: 1;
    }
    .header-info h1 {
        color: #ffffff;
        font-size: 1.6rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.3px;
    }
    .header-info p {
        color: rgba(255,255,255,0.6);
        font-size: 0.8rem;
        margin: 0.2rem 0 0 0;
        font-weight: 400;
    }

    /* Seções */
    .section-label {
        color: #1a2332;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin: 2rem 0 0.8rem 0;
        padding-left: 0.5rem;
        border-left: 3px solid #4A9BA8;
    }

    /* Card de resultado */
    .result-card {
        background: linear-gradient(135deg, #ffffff 0%, #f4fafb 100%);
        border-radius: 20px;
        padding: 2.5rem;
        box-shadow: 0 8px 32px rgba(74, 155, 168, 0.1);
        border: 1px solid rgba(74, 155, 168, 0.15);
        margin: 1.5rem 0;
        text-align: center;
    }
    .result-label {
        color: #6b7280;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 500;
    }
    .result-total {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #4A9BA8 0%, #2d7a85 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0.5rem 0;
    }

    /* Tier badge */
    .tier-badge-premium {
        background: linear-gradient(135deg, #f59e0b, #d97706);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 6px;
        font-size: 0.72rem;
        font-weight: 600;
        display: inline-block;
        letter-spacing: 0.5px;
    }
    .tier-badge-plus {
        background: linear-gradient(135deg, #4A9BA8, #3a7f8a);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 6px;
        font-size: 0.72rem;
        font-weight: 600;
        display: inline-block;
        letter-spacing: 0.5px;
    }
    .tier-badge-base {
        background: linear-gradient(135deg, #6b7280, #4b5563);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 6px;
        font-size: 0.72rem;
        font-weight: 600;
        display: inline-block;
        letter-spacing: 0.5px;
    }

    /* KPI cards */
    .kpi-row {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin: 1.5rem 0;
    }
    .kpi-item {
        background: #ffffff;
        border-radius: 14px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.04);
        border: 1px solid #f0f0f0;
    }
    .kpi-item-label {
        color: #9ca3af;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 500;
    }
    .kpi-item-value {
        color: #1a2332;
        font-size: 1.4rem;
        font-weight: 700;
        margin-top: 0.3rem;
    }

    /* Detalhamento */
    .breakdown-card {
        background: #ffffff;
        border-radius: 14px;
        padding: 1.5rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.04);
        margin: 1rem 0;
    }
    .breakdown-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.7rem 0;
        border-bottom: 1px solid #f5f5f5;
    }
    .breakdown-row:last-child {
        border-bottom: none;
    }
    .breakdown-name {
        color: #4b5563;
        font-size: 0.85rem;
        font-weight: 400;
    }
    .breakdown-value {
        color: #1a2332;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .breakdown-total {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 0 0 0;
        margin-top: 0.5rem;
        border-top: 2px solid #4A9BA8;
    }
    .breakdown-total-label {
        color: #1a2332;
        font-size: 0.9rem;
        font-weight: 700;
    }
    .breakdown-total-value {
        color: #4A9BA8;
        font-size: 1.2rem;
        font-weight: 800;
    }

    /* Locked badge */
    .locked-badge {
        background: linear-gradient(135deg, #f3f4f6, #e5e7eb);
        color: #9ca3af;
        padding: 0.6rem 1rem;
        border-radius: 10px;
        font-size: 0.78rem;
        font-weight: 500;
        display: inline-block;
        margin-top: 0.5rem;
    }

    /* Botão principal */
    .stButton > button {
        background: linear-gradient(135deg, #4A9BA8 0%, #3a7f8a 100%);
        color: white;
        border: none;
        border-radius: 14px;
        padding: 0.9rem 2.5rem;
        font-weight: 600;
        font-size: 1rem;
        letter-spacing: 0.3px;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(74, 155, 168, 0.3);
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #3d8a96 0%, #2d7580 100%);
        box-shadow: 0 8px 28px rgba(74, 155, 168, 0.4);
        transform: translateY(-2px);
    }

    /* Footer */
    .app-footer {
        text-align: center;
        color: #b0b8c4;
        font-size: 0.72rem;
        margin-top: 3rem;
        padding: 1.5rem;
        border-top: 1px solid #e8eef3;
        font-weight: 400;
    }

    /* Esconder defaults do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Inputs */
    .stSelectbox > div > div {
        border-radius: 12px;
    }
    .stTextInput > div > div > input {
        border-radius: 12px;
    }
    .stNumberInput > div > div > input {
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# DADOS DE CONFIGURAÇÃO
# ============================================================

CODIGOS_TIER = {
    "15081996": "PREMIUM",
    "13092020": "PLUS",
    "06121990": "BASE",
}

PRECOS = {
    "BASE": {
        "Moto": {"taxa_base": 28, "valor_km": 4.50, "ponto_f1": 8, "ponto_f2": 12, "ponto_f3": 18},
        "Carro": {"taxa_base": 50, "valor_km": 5.50, "ponto_f1": 10, "ponto_f2": 15, "ponto_f3": 22},
        "Fiorino": {"taxa_base": 80, "valor_km": 7.00, "ponto_f1": 12, "ponto_f2": 18, "ponto_f3": 25},
        "Van": {"taxa_base": 130, "valor_km": 8.50, "ponto_f1": 15, "ponto_f2": 22, "ponto_f3": 30},
        "VUC": {"taxa_base": 180, "valor_km": 10.00, "ponto_f1": 18, "ponto_f2": 26, "ponto_f3": 35},
        "3/4": {"taxa_base": 250, "valor_km": 11.50, "ponto_f1": 22, "ponto_f2": 30, "ponto_f3": 40},
        "Truck": {"taxa_base": 350, "valor_km": 13.00, "ponto_f1": 25, "ponto_f2": 35, "ponto_f3": 48},
        "Carreta": {"taxa_base": 550, "valor_km": 16.00, "ponto_f1": 30, "ponto_f2": 42, "ponto_f3": 58},
    },
    "PLUS": {
        "Moto": {"taxa_base": 22, "valor_km": 3.60, "ponto_f1": 6.50, "ponto_f2": 10, "ponto_f3": 14},
        "Carro": {"taxa_base": 40, "valor_km": 4.40, "ponto_f1": 8, "ponto_f2": 12, "ponto_f3": 17},
        "Fiorino": {"taxa_base": 64, "valor_km": 5.60, "ponto_f1": 10, "ponto_f2": 14, "ponto_f3": 20},
        "Van": {"taxa_base": 104, "valor_km": 6.80, "ponto_f1": 12, "ponto_f2": 17, "ponto_f3": 24},
        "VUC": {"taxa_base": 144, "valor_km": 8.00, "ponto_f1": 14, "ponto_f2": 21, "ponto_f3": 28},
        "3/4": {"taxa_base": 200, "valor_km": 9.20, "ponto_f1": 17, "ponto_f2": 24, "ponto_f3": 32},
        "Truck": {"taxa_base": 280, "valor_km": 10.40, "ponto_f1": 20, "ponto_f2": 28, "ponto_f3": 38},
        "Carreta": {"taxa_base": 440, "valor_km": 12.80, "ponto_f1": 24, "ponto_f2": 34, "ponto_f3": 46},
    },
    "PREMIUM": {
        "Moto": {"taxa_base": 18, "valor_km": 2.90, "ponto_f1": 5, "ponto_f2": 8, "ponto_f3": 11},
        "Carro": {"taxa_base": 32, "valor_km": 3.60, "ponto_f1": 6.50, "ponto_f2": 10, "ponto_f3": 14},
        "Fiorino": {"taxa_base": 52, "valor_km": 4.50, "ponto_f1": 8, "ponto_f2": 11, "ponto_f3": 16},
        "Van": {"taxa_base": 84, "valor_km": 5.50, "ponto_f1": 10, "ponto_f2": 14, "ponto_f3": 19},
        "VUC": {"taxa_base": 117, "valor_km": 6.50, "ponto_f1": 12, "ponto_f2": 17, "ponto_f3": 22},
        "3/4": {"taxa_base": 162, "valor_km": 7.50, "ponto_f1": 14, "ponto_f2": 19, "ponto_f3": 26},
        "Truck": {"taxa_base": 228, "valor_km": 8.50, "ponto_f1": 16, "ponto_f2": 22, "ponto_f3": 30},
        "Carreta": {"taxa_base": 358, "valor_km": 10.40, "ponto_f1": 19, "ponto_f2": 27, "ponto_f3": 37},
    }
}

VEICULOS_INFO = {
    "Moto": {"capacidade": "20 kg", "volume": "0,1 m\u00b3", "desc": "Documentos e pequenos volumes"},
    "Carro": {"capacidade": "300 kg", "volume": "1,5 m\u00b3", "desc": "Caixas e encomendas leves"},
    "Fiorino": {"capacidade": "600 kg", "volume": "3,5 m\u00b3", "desc": "Entregas comerciais"},
    "Van": {"capacidade": "1.500 kg", "volume": "12 m\u00b3", "desc": "Cargas m\u00e9dias e pallets"},
    "VUC": {"capacidade": "3.000 kg", "volume": "18 m\u00b3", "desc": "Distribui\u00e7\u00e3o urbana"},
    "3/4": {"capacidade": "4.000 kg", "volume": "25 m\u00b3", "desc": "Cargas industriais"},
    "Truck": {"capacidade": "12.000 kg", "volume": "45 m\u00b3", "desc": "Grandes volumes"},
    "Carreta": {"capacidade": "25.000 kg", "volume": "90 m\u00b3", "desc": "Carga completa pesada"},
}

PROTECAO = {
    "taxa_cliente_base": 0.0023,
    "taxa_cliente_plus": 0.0021,
    "taxa_cliente_premium": 0.0018,
    "custo_seguradora": 0.0008,
    "valor_minimo": 5.00,
    "teto_cobertura": 500000,
}

ADICIONAIS = {
    "Hor\u00e1rio comercial": 0,
    "Hor\u00e1rio de pico": 0.15,
    "Per\u00edodo noturno": 0.25,
    "S\u00e1bado": 0.20,
    "Domingo ou feriado": 0.30,
    "Zona de restri\u00e7\u00e3o (ZMRC)": 0.10,
}

# ============================================================
# FUNÇÕES DE CÁLCULO
# ============================================================

def identificar_tier(codigo):
    codigo_limpo = codigo.strip()
    if codigo_limpo in CODIGOS_TIER:
        return CODIGOS_TIER[codigo_limpo]
    return None


def calcular_taxa_pontos(n_pontos, preco_veiculo):
    total = 0
    for i in range(n_pontos):
        if i < 3:
            total += preco_veiculo["ponto_f1"]
        elif i < 8:
            total += preco_veiculo["ponto_f2"]
        else:
            total += preco_veiculo["ponto_f3"]
    return total


def calcular_protecao(valor_mercadoria, tier):
    if tier == "PLUS":
        taxa = PROTECAO["taxa_cliente_plus"]
    elif tier == "PREMIUM":
        taxa = PROTECAO["taxa_cliente_premium"]
    else:
        taxa = PROTECAO["taxa_cliente_base"]
    valor = valor_mercadoria * taxa
    return max(valor, PROTECAO["valor_minimo"])


def calcular_cotacao(veiculo, tier, km_total, n_pontos, tipo_carga,
                     percentual_complemento, protecao_ativa, valor_mercadoria,
                     adicional_selecionado):
    preco = PRECOS[tier][veiculo]
    taxa_base = preco["taxa_base"]
    valor_km = km_total * preco["valor_km"]
    taxa_pontos = calcular_taxa_pontos(n_pontos, preco)
    subtotal = taxa_base + valor_km + taxa_pontos

    if tipo_carga == "Complemento":
        subtotal = subtotal * (percentual_complemento / 100)

    valor_adicional = 0
    if adicional_selecionado in ADICIONAIS:
        valor_adicional = subtotal * ADICIONAIS[adicional_selecionado]

    valor_protecao = 0
    if protecao_ativa and valor_mercadoria > 0:
        valor_protecao = calcular_protecao(valor_mercadoria, tier)

    total = subtotal + valor_adicional + valor_protecao

    return {
        "taxa_base": taxa_base,
        "valor_km": valor_km,
        "km_total": km_total,
        "taxa_pontos": taxa_pontos,
        "n_pontos": n_pontos,
        "subtotal": subtotal,
        "adicional": valor_adicional,
        "adicional_nome": adicional_selecionado,
        "protecao": valor_protecao,
        "total": round(total, 2),
        "tipo_carga": tipo_carga,
    }


# ============================================================
# HEADER COM LOGO
# ============================================================

st.markdown("""
<div class="app-header">
    <div class="logo-mark">
        <div class="logo-t"></div>
        <div class="logo-f"></div>
    </div>
    <div class="header-info">
        <h1>TRANSFELOG</h1>
        <p>Grupo Transfelog do Brasil</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# CÓDIGO DO CLIENTE (TIER)
# ============================================================
st.markdown('<div class="section-label">Acesso</div>', unsafe_allow_html=True)

codigo_cliente = st.text_input(
    "C\u00f3digo do cliente",
    type="password",
    placeholder="Insira seu c\u00f3digo de acesso",
    label_visibility="collapsed"
)

tier_ativo = identificar_tier(codigo_cliente)

if codigo_cliente and tier_ativo is None:
    st.error("C\u00f3digo inv\u00e1lido. Verifique com seu consultor.")
elif tier_ativo:
    if tier_ativo == "PREMIUM":
        st.markdown('<span class="tier-badge-premium">PREMIUM</span>', unsafe_allow_html=True)
    elif tier_ativo == "PLUS":
        st.markdown('<span class="tier-badge-plus">PLUS</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="tier-badge-base">BASE</span>', unsafe_allow_html=True)

# Só mostra o restante se o código for válido
if tier_ativo:

    # ============================================================
    # SELEÇÃO DE VEÍCULO (DROPDOWN CLEAN)
    # ============================================================
    st.markdown('<div class="section-label">Ve\u00edculo</div>', unsafe_allow_html=True)

    opcoes_veiculo = list(VEICULOS_INFO.keys())
    veiculo_selecionado = st.selectbox(
        "Selecione o ve\u00edculo",
        opcoes_veiculo,
        format_func=lambda v: f"{v}  \u2014  {VEICULOS_INFO[v]['capacidade']}  |  {VEICULOS_INFO[v]['volume']}",
        label_visibility="collapsed"
    )
    st.caption(VEICULOS_INFO[veiculo_selecionado]["desc"])

    # ============================================================
    # TIPO DE CARGA
    # ============================================================
    st.markdown('<div class="section-label">Tipo de carga</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        tipo_carga = st.selectbox(
            "Tipo",
            ["Carga Completa", "Complemento"],
            label_visibility="collapsed"
        )
    with col2:
        percentual_complemento = 100
        if tipo_carga == "Complemento":
            percentual_complemento = st.slider("Espa\u00e7o utilizado (%)", 40, 100, 60)
        else:
            st.caption("Ve\u00edculo exclusivo")

    # ============================================================
    # DISTÂNCIA E PARADAS
    # ============================================================
    st.markdown('<div class="section-label">Percurso</div>', unsafe_allow_html=True)

    col_km, col_paradas = st.columns(2)
    with col_km:
        km_total = st.number_input(
            "Dist\u00e2ncia total (km)",
            min_value=1.0,
            max_value=500.0,
            value=25.0,
            step=1.0
        )
    with col_paradas:
        n_paradas = st.number_input(
            "Pontos de entrega",
            min_value=1,
            max_value=20,
            value=3,
            step=1
        )

    st.markdown('<span class="locked-badge">Roteirizador autom\u00e1tico \u2014 dispon\u00edvel em breve</span>', unsafe_allow_html=True)

    # ============================================================
    # PERÍODO
    # ============================================================
    st.markdown('<div class="section-label">Per\u00edodo</div>', unsafe_allow_html=True)

    adicional = st.selectbox(
        "Per\u00edodo da entrega",
        list(ADICIONAIS.keys()),
        label_visibility="collapsed"
    )

    # ============================================================
    # PROTEÇÃO DE CARGA
    # ============================================================
    st.markdown('<div class="section-label">Prote\u00e7\u00e3o de carga</div>', unsafe_allow_html=True)

    col_p1, col_p2 = st.columns([1, 2])
    with col_p1:
        protecao_ativa = st.toggle("Ativar prote\u00e7\u00e3o", value=True)
    with col_p2:
        valor_mercadoria = 0.0
        if protecao_ativa:
            valor_mercadoria = st.number_input(
                "Valor da mercadoria (R$)",
                min_value=0.0,
                value=10000.0,
                step=1000.0,
                format="%.2f"
            )

    if protecao_ativa and valor_mercadoria > 0:
        vp = calcular_protecao(valor_mercadoria, tier_ativo)
        st.caption(f"Prote\u00e7\u00e3o adicional: R$ {vp:.2f}")

    # ============================================================
    # BOTÃO CALCULAR
    # ============================================================
    st.markdown("")
    st.markdown("")
    calcular = st.button("CALCULAR COTA\u00c7\u00c3O", use_container_width=True)

    # ============================================================
    # RESULTADO
    # ============================================================
    if calcular:
        resultado = calcular_cotacao(
            veiculo=veiculo_selecionado,
            tier=tier_ativo,
            km_total=km_total,
            n_pontos=n_paradas,
            tipo_carga=tipo_carga,
            percentual_complemento=percentual_complemento,
            protecao_ativa=protecao_ativa,
            valor_mercadoria=valor_mercadoria,
            adicional_selecionado=adicional
        )

        st.markdown(f"""
        <div class="result-card">
            <div class="result-label">VALOR DA COTA\u00c7\u00c3O</div>
            <div class="result-total">R$ {resultado['total']:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)

        # KPIs
        st.markdown(f"""
        <div class="kpi-row">
            <div class="kpi-item">
                <div class="kpi-item-label">Dist\u00e2ncia</div>
                <div class="kpi-item-value">{km_total} km</div>
            </div>
            <div class="kpi-item">
                <div class="kpi-item-label">Paradas</div>
                <div class="kpi-item-value">{n_paradas}</div>
            </div>
            <div class="kpi-item">
                <div class="kpi-item-label">Ve\u00edculo</div>
                <div class="kpi-item-value">{veiculo_selecionado}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Detalhamento
        detalhes_html = f"""
        <div class="breakdown-card">
            <div class="breakdown-row">
                <span class="breakdown-name">Taxa base ({veiculo_selecionado})</span>
                <span class="breakdown-value">R$ {resultado['taxa_base']:.2f}</span>
            </div>
            <div class="breakdown-row">
                <span class="breakdown-name">Quilometragem ({km_total} km \u00d7 R$ {PRECOS[tier_ativo][veiculo_selecionado]['valor_km']:.2f})</span>
                <span class="breakdown-value">R$ {resultado['valor_km']:.2f}</span>
            </div>
            <div class="breakdown-row">
                <span class="breakdown-name">Pontos de entrega ({n_paradas})</span>
                <span class="breakdown-value">R$ {resultado['taxa_pontos']:.2f}</span>
            </div>
        """

        if resultado['adicional'] > 0:
            detalhes_html += f"""
            <div class="breakdown-row">
                <span class="breakdown-name">{adicional}</span>
                <span class="breakdown-value">R$ {resultado['adicional']:.2f}</span>
            </div>
            """

        if resultado['protecao'] > 0:
            detalhes_html += f"""
            <div class="breakdown-row">
                <span class="breakdown-name">Prote\u00e7\u00e3o de carga</span>
                <span class="breakdown-value">R$ {resultado['protecao']:.2f}</span>
            </div>
            """

        detalhes_html += f"""
            <div class="breakdown-total">
                <span class="breakdown-total-label">Total</span>
                <span class="breakdown-total-value">R$ {resultado['total']:,.2f}</span>
            </div>
        </div>
        """

        st.markdown(detalhes_html, unsafe_allow_html=True)

        # Texto para copiar
        st.markdown("")
        msg = f"""*TRANSFELOG | Cota\u00e7\u00e3o de Frete*

Ve\u00edculo: {veiculo_selecionado}
Dist\u00e2ncia: {km_total} km
Pontos de entrega: {n_paradas}
Per\u00edodo: {adicional}
{'Prote\u00e7\u00e3o de carga: Inclusa' if protecao_ativa else ''}

*TOTAL: R$ {resultado['total']:,.2f}*

Grupo Transfelog do Brasil
transfelog.streamlit.app"""

        st.text_area("Copiar cota\u00e7\u00e3o", msg, height=200, label_visibility="collapsed")

else:
    if not codigo_cliente:
        st.markdown("")
        st.caption("Insira seu c\u00f3digo de acesso para calcular sua cota\u00e7\u00e3o.")

# ============================================================
# FOOTER
# ============================================================
st.markdown("""
<div class="app-footer">
    Transfelog App \u00b7 Grupo Transfelog do Brasil \u00b7 S\u00e3o Paulo e ABC Paulista
</div>
""", unsafe_allow_html=True)
