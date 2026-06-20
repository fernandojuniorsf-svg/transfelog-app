```python
import streamlit as st
import requests
from datetime import datetime

# ============================================================
# CONFIGURACAO DA PAGINA
# ============================================================
st.set_page_config(
    page_title="Transfelog App",
    page_icon="T",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CSS CUSTOMIZADO - DESIGN MODERNO
# ============================================================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #f8fafb 0%, #eef2f5 100%);
    }
    .header-container {
        background: linear-gradient(135deg, #2d3436 0%, #1a1e21 50%, #4A9BA8 100%);
        padding: 2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(74, 155, 168, 0.15);
    }
    .header-title {
        color: #ffffff;
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .header-subtitle {
        color: rgba(255,255,255,0.7);
        font-size: 0.9rem;
        margin-top: 0.3rem;
        font-weight: 400;
    }
    .kpi-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border-left: 4px solid #4A9BA8;
        transition: transform 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(74, 155, 168, 0.15);
    }
    .kpi-label {
        color: #6b7280;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.3rem;
    }
    .kpi-value {
        color: #1a1e21;
        font-size: 1.8rem;
        font-weight: 700;
    }
    .kpi-value-highlight {
        color: #4A9BA8;
        font-size: 1.8rem;
        font-weight: 700;
    }
    .result-card {
        background: linear-gradient(135deg, #ffffff 0%, #f0fafb 100%);
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 4px 24px rgba(74, 155, 168, 0.12);
        border: 1px solid rgba(74, 155, 168, 0.2);
        margin: 1.5rem 0;
    }
    .result-total {
        font-size: 2.5rem;
        font-weight: 800;
        color: #4A9BA8;
        margin: 0.5rem 0;
    }
    .result-label {
        color: #6b7280;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .section-title {
        color: #1a1e21;
        font-size: 1.1rem;
        font-weight: 600;
        margin: 1.5rem 0 0.8rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #4A9BA8;
        display: inline-block;
    }
    .detail-row {
        display: flex;
        justify-content: space-between;
        padding: 0.6rem 0;
        border-bottom: 1px solid #f3f4f6;
    }
    .detail-label {
        color: #6b7280;
        font-size: 0.9rem;
    }
    .detail-value {
        color: #1a1e21;
        font-weight: 600;
        font-size: 0.9rem;
    }
    .route-step {
        background: #ffffff;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        margin: 0.5rem 0;
        border-left: 3px solid #4A9BA8;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    }
    .route-number {
        color: #4A9BA8;
        font-weight: 700;
        font-size: 0.85rem;
    }
    .route-address {
        color: #1a1e21;
        font-size: 0.9rem;
        margin-top: 0.2rem;
    }
    .route-km {
        color: #6b7280;
        font-size: 0.8rem;
    }
    .stButton > button {
        background: linear-gradient(135deg, #4A9BA8 0%, #3d8a96 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.7rem 2rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.2s ease;
        box-shadow: 0 4px 12px rgba(74, 155, 168, 0.3);
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #3d8a96 0%, #2d7580 100%);
        box-shadow: 0 6px 20px rgba(74, 155, 168, 0.4);
        transform: translateY(-1px);
    }
    .savings-badge {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
        margin-top: 0.5rem;
    }
    .footer {
        text-align: center;
        color: #9ca3af;
        font-size: 0.75rem;
        margin-top: 3rem;
        padding: 1.5rem;
        border-top: 1px solid #e5e7eb;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stSelectbox > div > div {
        border-radius: 10px;
    }
    .stTextInput > div > div > input {
        border-radius: 10px;
    }
    .stNumberInput > div > div > input {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# DADOS DE CONFIGURACAO (VARIAVEIS EDITAVEIS)
# ============================================================

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
    "Moto": {"capacidade": "20kg", "volume": "0.1m3"},
    "Carro": {"capacidade": "300kg", "volume": "1.5m3"},
    "Fiorino": {"capacidade": "600kg", "volume": "3.5m3"},
    "Van": {"capacidade": "1.500kg", "volume": "12m3"},
    "VUC": {"capacidade": "3.000kg", "volume": "18m3"},
    "3/4": {"capacidade": "4.000kg", "volume": "25m3"},
    "Truck": {"capacidade": "12.000kg", "volume": "45m3"},
    "Carreta": {"capacidade": "25.000kg", "volume": "90m3"},
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
    "pico": 0.15,
    "noturno": 0.25,
    "sabado": 0.20,
    "domingo_feriado": 0.30,
    "zmrc": 0.10,
}

# ============================================================
# GOOGLE MAPS API KEY (via Streamlit Secrets)
# ============================================================
GOOGLE_MAPS_API_KEY = st.secrets.get("GOOGLE_MAPS_API_KEY", "")

# ============================================================
# FUNCOES DE ROTEIRIZACAO
# ============================================================

def calcular_distancia_google(origem, destinos, otimizar=True):
    if not GOOGLE_MAPS_API_KEY:
        return simular_distancias(origem, destinos, otimizar)

    try:
        url = "https://maps.googleapis.com/maps/api/directions/json"

        if len(destinos) == 1:
            params = {
                "origin": origem,
                "destination": destinos[0],
                "key": GOOGLE_MAPS_API_KEY,
                "language": "pt-BR",
            }
        else:
            waypoints_str = "|".join(destinos[:-1])
            opt = "optimize:true|" if otimizar else ""
            params = {
                "origin": origem,
                "destination": destinos[-1],
                "waypoints": f"{opt}{waypoints_str}",
                "key": GOOGLE_MAPS_API_KEY,
                "language": "pt-BR",
            }

        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if data["status"] == "OK":
            route = data["routes"][0]
            km_total = sum(leg["distance"]["value"] for leg in route["legs"]) / 1000
            ordem = route.get("waypoint_order", list(range(len(destinos))))

            detalhes = []
            for i, leg in enumerate(route["legs"]):
                idx = ordem[i] if i < len(ordem) else len(destinos) - 1
                detalhes.append({
                    "trecho": i + 1,
                    "km": round(leg["distance"]["value"] / 1000, 1),
                    "tempo": leg["duration"]["text"],
                    "endereco": destinos[idx] if idx < len(destinos) else destinos[-1]
                })

            return round(km_total, 1), ordem, detalhes

    except Exception:
        pass

    return simular_distancias(origem, destinos, otimizar)


def simular_distancias(origem, destinos, otimizar=True):
    import random
    random.seed(hash(origem + "".join(destinos)) % 100)

    n_pontos = len(destinos)
    distancias = [round(random.uniform(3, 18), 1) for _ in range(n_pontos)]

    if otimizar and n_pontos > 2:
        distancias.sort()

    km_total = sum(distancias)
    ordem = list(range(n_pontos))

    detalhes = []
    for i in range(n_pontos):
        detalhes.append({
            "trecho": i + 1,
            "km": distancias[i],
            "endereco": destinos[ordem[i]]
        })

    return round(km_total, 1), ordem, detalhes


# ============================================================
# FUNCOES DE CALCULO
# ============================================================

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
    if adicional_selecionado != "Nenhum":
        mapa_adicionais = {
            "Pico (+15%)": "pico",
            "Noturno (+25%)": "noturno",
            "Sabado (+20%)": "sabado",
            "Domingo/Feriado (+30%)": "domingo_feriado",
            "ZMRC (+10%)": "zmrc",
        }
        chave = mapa_adicionais.get(adicional_selecionado, "")
        if chave in ADICIONAIS:
            valor_adicional = subtotal * ADICIONAIS[chave]

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
        "protecao": valor_protecao,
        "total": round(total, 2),
        "tipo_carga": tipo_carga,
    }


# ============================================================
# INTERFACE PRINCIPAL
# ============================================================

st.markdown("""
<div class="header-container">
    <div class="header-title">TRANSFELOG APP</div>
    <div class="header-subtitle">Grupo Transfelog do Brasil  |  Cotacao e Roteirizacao</div>
</div>
""", unsafe_allow_html=True)

# SELECAO DE VEICULO
st.markdown('<p class="section-title">Tipo de Veiculo</p>', unsafe_allow_html=True)

veiculo_selecionado = st.radio(
    "Selecione o veiculo",
    list(VEICULOS_INFO.keys()),
    horizontal=True,
    label_visibility="collapsed"
)

info_v = VEICULOS_INFO[veiculo_selecionado]
st.caption(f"{veiculo_selecionado}  |  Capacidade: {info_v['capacidade']}  |  Volume: {info_v['volume']}")

# TIER E TIPO DE CARGA
col1, col2, col3 = st.columns(3)

with col1:
    tier = st.selectbox("Tier do Cliente", ["BASE", "PLUS", "PREMIUM"])

with col2:
    tipo_carga = st.selectbox("Tipo de Carga", ["Carga Completa", "Complemento"])

with col3:
    percentual_complemento = 100
    if tipo_carga == "Complemento":
        percentual_complemento = st.slider("% do espaco utilizado", 40, 100, 60)
    else:
        st.write("")
        st.caption("Veiculo exclusivo")

# ENDERECOS
st.markdown('<p class="section-title">Enderecos</p>', unsafe_allow_html=True)

origem = st.text_input("Endereco de Coleta (Origem)", placeholder="Ex: Rua das Flores, 123 - Santo Andre, SP")

st.caption("Pontos de Entrega")

if "n_paradas" not in st.session_state:
    st.session_state.n_paradas = 3

destinos = []
for i in range(st.session_state.n_paradas):
    endereco = st.text_input(
        f"Ponto {i+1}",
        key=f"destino_{i}",
        placeholder=f"Endereco do ponto de entrega {i+1}",
        label_visibility="collapsed"
    )
    if endereco:
        destinos.append(endereco)

col_add, col_remove, _ = st.columns([1, 1, 4])
with col_add:
    if st.button("+ Adicionar ponto"):
        if st.session_state.n_paradas < 20:
            st.session_state.n_paradas += 1
            st.rerun()
with col_remove:
    if st.button("- Remover ponto"):
        if st.session_state.n_paradas > 1:
            st.session_state.n_paradas -= 1
            st.rerun()

# PROTECAO DE CARGA
st.markdown('<p class="section-title">Protecao de Carga</p>', unsafe_allow_html=True)

col_p1, col_p2 = st.columns([1, 2])

with col_p1:
    protecao_ativa = st.toggle("Ativar Protecao", value=True)

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
    taxa_display = "0,23%" if tier == "BASE" else ("0,21%" if tier == "PLUS" else "0,18%")
    valor_protecao_display = calcular_protecao(valor_mercadoria, tier)
    st.caption(f"Taxa: {taxa_display}  |  Valor adicional: R$ {valor_protecao_display:.2f}")

# ADICIONAIS E MODO DE ROTA
col_ad1, col_ad2 = st.columns(2)
with col_ad1:
    adicional = st.selectbox(
        "Adicional de horario/dia",
        ["Nenhum", "Pico (+15%)", "Noturno (+25%)", "Sabado (+20%)", "Domingo/Feriado (+30%)", "ZMRC (+10%)"]
    )

with col_ad2:
    modo_rota = st.selectbox("Modo de Rota", ["Roteirizar (menor km)", "Manter ordem manual"])

# CALCULAR
st.markdown("---")

calcular = st.button("CALCULAR COTACAO", use_container_width=True)

if calcular:
    if not origem:
        st.warning("Preencha o endereco de coleta.")
    elif len(destinos) == 0:
        st.warning("Adicione ao menos um ponto de entrega.")
    else:
        otimizar = "Roteirizar" in modo_rota
        km_total, ordem, detalhes = calcular_distancia_google(origem, destinos, otimizar)

        km_manual = km_total
        if otimizar:
            km_manual_calc, _, _ = simular_distancias(origem, destinos, False)
            km_manual = km_manual_calc if km_manual_calc > km_total else km_total * 1.22

        resultado = calcular_cotacao(
            veiculo=veiculo_selecionado,
            tier=tier,
            km_total=km_total,
            n_pontos=len(destinos),
            tipo_carga=tipo_carga,
            percentual_complemento=percentual_complemento,
            protecao_ativa=protecao_ativa,
            valor_mercadoria=valor_mercadoria,
            adicional_selecionado=adicional
        )

        # RESULTADO
        st.markdown(f"""
        <div class="result-card">
            <div class="result-label">VALOR TOTAL DA COTACAO</div>
            <div class="result-total">R$ {resultado['total']:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)

        # KPIs
        col_k1, col_k2, col_k3, col_k4 = st.columns(4)

        with col_k1:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">DISTANCIA TOTAL</div>
                <div class="kpi-value">{km_total} km</div>
            </div>
            """, unsafe_allow_html=True)

        with col_k2:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">PARADAS</div>
                <div class="kpi-value">{len(destinos)}</div>
            </div>
            """, unsafe_allow_html=True)

        with col_k3:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">VEICULO</div>
                <div class="kpi-value">{veiculo_selecionado}</div>
            </div>
            """, unsafe_allow_html=True)

        with col_k4:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">TIER</div>
                <div class="kpi-value-highlight">{tier}</div>
            </div>
            """, unsafe_allow_html=True)

        # DETALHAMENTO
        st.markdown('<p class="section-title">Detalhamento</p>', unsafe_allow_html=True)

        col_d1, col_d2 = st.columns(2)

        with col_d1:
            st.markdown(f"""
            <div class="detail-row">
                <span class="detail-label">Taxa base ({veiculo_selecionado})</span>
                <span class="detail-value">R$ {resultado['taxa_base']:.2f}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Quilometragem ({km_total} km x R$ {PRECOS[tier][veiculo_selecionado]['valor_km']:.2f})</span>
                <span class="detail-value">R$ {resultado['valor_km']:.2f}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Paradas ({len(destinos)} pontos)</span>
                <span class="detail-value">R$ {resultado['taxa_pontos']:.2f}</span>
            </div>
            """, unsafe_allow_html=True)

            if resultado['adicional'] > 0:
                st.markdown(f"""
                <div class="detail-row">
                    <span class="detail-label">Adicional ({adicional})</span>
                    <span class="detail-value">R$ {resultado['adicional']:.2f}</span>
                </div>
                """, unsafe_allow_html=True)

            if resultado['protecao'] > 0:
                st.markdown(f"""
                <div class="detail-row">
                    <span class="detail-label">Protecao de Carga ({taxa_display})</span>
                    <span class="detail-value">R$ {resultado['protecao']:.2f}</span>
                </div>
                """, unsafe_allow_html=True)

        with col_d2:
            st.markdown("**Rota:**")
            for i, detalhe in enumerate(detalhes):
                st.markdown(f"""
                <div class="route-step">
                    <span class="route-number">{i+1}.</span>
                    <span class="route-address">{detalhe['endereco']}</span>
                    <span class="route-km"> | {detalhe['km']} km</span>
                </div>
                """, unsafe_allow_html=True)

        # ECONOMIA
        if otimizar and km_manual > km_total:
            economia_km = km_manual - km_total
            economia_pct = (economia_km / km_manual) * 100
            resultado_manual = calcular_cotacao(
                veiculo=veiculo_selecionado, tier=tier, km_total=km_manual,
                n_pontos=len(destinos), tipo_carga=tipo_carga,
                percentual_complemento=percentual_complemento,
                protecao_ativa=protecao_ativa, valor_mercadoria=valor_mercadoria,
                adicional_selecionado=adicional
            )
            economia_valor = resultado_manual['total'] - resultado['total']

            st.markdown(f"""
            <div class="savings-badge">
                Economia com roteirizacao: R$ {economia_valor:.2f} ({economia_pct:.1f}% menos km)
            </div>
            """, unsafe_allow_html=True)

        # ACOES
        st.markdown("---")
        col_b1, col_b2, col_b3 = st.columns(3)

        with col_b1:
            enderecos_formatados = f"COLETA: {origem}\n"
            for i, det in enumerate(detalhes):
                enderecos_formatados += f"{i+1}. {det['endereco']}\n"

            st.text_area("Copiar enderecos (ordem otimizada)", enderecos_formatados, height=150)

        with col_b2:
            msg_whatsapp = f"""*TRANSFELOG | Cotacao #{datetime.now().strftime('%d%m%y%H%M')}*

Veiculo: {veiculo_selecionado}
Distancia: {km_total} km
Paradas: {len(destinos)}
{'Protecao de Carga: Sim' if protecao_ativa else ''}

*TOTAL: R$ {resultado['total']:,.2f}*

Grupo Transfelog do Brasil"""

            st.text_area("Enviar por WhatsApp", msg_whatsapp, height=150)

        with col_b3:
            st.markdown("**Controle interno:**")
            custo_estimado = resultado['total'] * 0.55
            lucro_estimado = resultado['total'] - custo_estimado
            margem = (lucro_estimado / resultado['total']) * 100
            st.caption(f"Custo estimado: R$ {custo_estimado:.2f}")
            st.caption(f"Lucro estimado: R$ {lucro_estimado:.2f}")
            st.caption(f"Margem: {margem:.0f}%")

# FOOTER
st.markdown("""
<div class="footer">
    Transfelog App  |  Grupo Transfelog do Brasil  |  SP e ABC Paulista
</div>
""", unsafe_allow_html=True)
