import streamlit as st
from datetime import datetime
import base64
import os
import urllib.parse

try:
    import gspread
    from google.oauth2.service_account import Credentials
    GSHEETS_DISPONIVEL = True
except ImportError:
    GSHEETS_DISPONIVEL = False

try:
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaIoBaseUpload
    import io
    GDRIVE_DISPONIVEL = True
except ImportError:
    GDRIVE_DISPONIVEL = False

st.set_page_config(page_title="Transfelog App", page_icon="favicon2.png", layout="centered", initial_sidebar_state="collapsed")

# ============================================================
# LOGO BASE64
# ============================================================
LOGO_FILENAME = "favicon2.png"
logo_b64 = ""
if os.path.exists(LOGO_FILENAME):
    with open(LOGO_FILENAME, "rb") as f:
        logo_b64 = base64.b64encode(f.read()).decode()

# ============================================================
# META TAGS IPHONE
# ============================================================
st.markdown(f"""
<link rel="apple-touch-icon" href="data:image/png;base64,{logo_b64}">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Transfelog">
<meta name="theme-color" content="#1a2332">
""", unsafe_allow_html=True)

# ============================================================
# CSS
# ============================================================
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

:root{
    --teal:#4A9BA8;
    --teal-light:#5fb8c7;
    --teal-dark:#2d7a85;
    --dark:#1a2332;
    --gray-50:#f8fafc;
    --gray-100:#f1f5f9;
    --gray-200:#e2e8f0;
    --gray-400:#94a3b8;
    --gray-500:#64748b;
    --gray-600:#475569;
    --green:#10b981;
    --white:#ffffff;
    --radius:16px;
    --radius-sm:12px;
}

*{font-family:'Inter',sans-serif !important}
.stApp{background:var(--gray-50)}

/* HEADER - LOGO BEM GRANDE */
.app-header{
    background:linear-gradient(160deg,var(--dark) 0%,#1e3040 50%,var(--teal-dark) 100%);
    padding:3rem 1rem 2.2rem;
    border-radius:0 0 28px 28px;
    display:flex;
    align-items:center;
    justify-content:center;
    margin:-1rem -1rem 0 -1rem;
    box-shadow:0 4px 20px rgba(26,35,50,0.15);
}
.app-header img{
    height:180px;
    object-fit:contain;
    mix-blend-mode:screen;
}

/* MENU TABS - FINO E CLEAN */
.stButton>button{
    background:transparent !important;
    color:var(--gray-400) !important;
    border:none !important;
    border-bottom:2px solid transparent !important;
    border-radius:0 !important;
    padding:0.35rem 0.6rem !important;
    font-weight:600 !important;
    font-size:0.68rem !important;
    letter-spacing:0.8px;
    text-transform:uppercase;
    box-shadow:none !important;
    transition:all 0.2s;
}
.stButton>button:hover{
    color:var(--teal) !important;
    border-bottom:2px solid var(--teal) !important;
    transform:none !important;
    box-shadow:none !important;
    background:transparent !important;
}
.stButton>button:focus{
    color:var(--teal) !important;
    box-shadow:none !important;
    background:transparent !important;
}

/* BOTAO CALCULAR (override especifico) */
.calc-btn button{
    background:linear-gradient(135deg,var(--teal) 0%,var(--teal-dark) 100%) !important;
    color:#fff !important;
    border:none !important;
    border-radius:12px !important;
    padding:0.7rem 1.5rem !important;
    font-weight:700 !important;
    font-size:0.8rem !important;
    letter-spacing:0.2px;
    text-transform:none !important;
    box-shadow:0 3px 10px rgba(74,155,168,0.15) !important;
}
.calc-btn button:hover{
    transform:translateY(-1px) !important;
    box-shadow:0 5px 16px rgba(74,155,168,0.25) !important;
    border-bottom:none !important;
    background:linear-gradient(135deg,var(--teal) 0%,var(--teal-dark) 100%) !important;
    color:#fff !important;
}

/* SECTION LABEL */
.sec-label{
    color:var(--gray-400);
    font-size:0.62rem;
    font-weight:600;
    text-transform:uppercase;
    letter-spacing:1.5px;
    margin:1.6rem 0 0.3rem 0;
}

/* RESULTADO */
.result-card{
    background:var(--white);
    border-radius:20px;
    padding:2rem 1.5rem;
    text-align:center;
    border:1px solid rgba(74,155,168,0.12);
    box-shadow:0 6px 30px rgba(74,155,168,0.05);
    margin:1.5rem 0;
    position:relative;
    overflow:hidden;
}
.result-card::before{
    content:'';position:absolute;top:0;left:0;right:0;height:3px;
    background:linear-gradient(90deg,var(--teal),var(--teal-light));
}
.result-card .label{color:var(--gray-400);font-size:0.62rem;text-transform:uppercase;letter-spacing:2px;font-weight:600}
.result-card .value{font-size:2.4rem;font-weight:900;color:var(--dark);margin:0.3rem 0;letter-spacing:-1.5px}
.result-card .sub{color:var(--gray-500);font-size:0.72rem;font-weight:400}

/* BADGES */
.badge{display:inline-flex;align-items:center;padding:0.15rem 0.55rem;border-radius:20px;font-size:0.62rem;font-weight:700;letter-spacing:0.3px}
.badge-premium{background:#fef9c3;color:#a16207}
.badge-plus{background:#ccfbf1;color:#0d9488}
.badge-base{background:var(--gray-100);color:var(--gray-600)}
.badge-cupom{background:#dcfce7;color:#166534}

/* KPI */
.kpi-row{display:flex;gap:0.4rem;margin:0.8rem 0}
.kpi-box{flex:1;background:var(--gray-50);border-radius:10px;padding:0.55rem 0.3rem;text-align:center;border:1px solid var(--gray-100)}
.kpi-box .n{font-size:0.95rem;font-weight:800;color:var(--dark)}
.kpi-box .l{font-size:0.52rem;color:var(--gray-400);text-transform:uppercase;letter-spacing:0.8px;margin-top:2px}

/* BREAKDOWN */
.bk{background:var(--white);border-radius:var(--radius);padding:1rem;border:1px solid var(--gray-100)}
.bk-row{display:flex;justify-content:space-between;align-items:center;padding:0.45rem 0;border-bottom:1px solid var(--gray-50)}
.bk-row:last-child{border-bottom:none}
.bk-row .n{color:var(--gray-500);font-size:0.72rem}
.bk-row .v{color:var(--dark);font-size:0.72rem;font-weight:600}
.bk-total{display:flex;justify-content:space-between;padding:0.6rem 0 0;margin-top:0.3rem;border-top:2px solid var(--teal)}
.bk-total .n{font-weight:700;color:var(--dark);font-size:0.82rem}
.bk-total .v{font-weight:800;color:var(--teal);font-size:1rem}

/* ALERTS */
.alert{border-radius:10px;padding:0.55rem 0.75rem;font-size:0.7rem;margin:0.5rem 0;line-height:1.4}
.alert-warn{background:#fefce8;border:1px solid #fde68a;color:#a16207}
.alert-ok{background:#f0fdf4;border:1px solid #bbf7d0;color:#166534}
.alert-info{background:#eff6ff;border:1px solid #bfdbfe;color:#1e40af}

/* WHATSAPP */
.wpp-btn{
    display:block;background:linear-gradient(135deg,#25D366 0%,#128C7E 100%);
    color:#fff !important;padding:0.75rem;border-radius:12px;font-weight:700;
    font-size:0.8rem;text-decoration:none;text-align:center;width:100%;
    box-shadow:0 3px 12px rgba(37,211,102,0.18);margin-top:1rem;
}
.wpp-btn:hover{opacity:0.9;color:#fff !important;text-decoration:none}

/* INFO CARD */
.info-card{background:var(--white);border-radius:var(--radius);padding:1.1rem;border:1px solid var(--gray-100);margin:0.5rem 0}

/* STREAMLIT INPUT OVERRIDES */
.stSelectbox>div>div{border-radius:10px !important;border-color:var(--gray-200) !important;font-size:0.8rem !important}
.stTextInput>div>div>input{border-radius:10px !important;border-color:var(--gray-200) !important;font-size:0.8rem !important;padding:0.5rem 0.7rem !important}
.stNumberInput>div>div>input{border-radius:10px !important;border-color:var(--gray-200) !important;font-size:0.8rem !important}
.stMultiSelect>div>div{border-radius:10px !important}
div[data-baseweb="select"]>div{border-radius:10px !important}

#MainMenu{visibility:hidden}
footer{visibility:hidden}
header{visibility:hidden}
.stDeployButton{display:none}

.app-footer{text-align:center;color:var(--gray-400);font-size:0.55rem;margin-top:2.5rem;padding:0.8rem 0;letter-spacing:0.5px;font-weight:500}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ============================================================
# CONSTANTES
# ============================================================
PASTA_DOCUMENTOS_ID = "1BZpEA9srVED0H5imA4_vMrxNpXlTGUeg"
WHATSAPP_TRANSFELOG = "5511978178226"
CODIGOS_TIER = {"15081996": "PREMIUM", "13092020": "PLUS", "06121990": "BASE"}
CUPONS_DESCONTO = {
    "TRANSFELOG10": {"desconto_pct": 10, "descricao": "10% de desconto", "validade": "2026-07-31"},
    "FRETE20": {"desconto_pct": 20, "descricao": "20% de desconto", "validade": "2026-07-15"},
    "INAUGURA15": {"desconto_pct": 15, "descricao": "15% de desconto", "validade": "2026-08-31"},
}
FATOR_CUBAGEM = 300
PROTECAO_MINIMO = 5.00
CUSTO_MOTORISTA_PCT = 0.50

PRECOS = {
    "BASE": {
        "Moto": {"taxa_base": 28, "valor_km": 4.50, "ponto_f1": 3, "ponto_f2": 5, "ponto_f3": 7},
        "Carro": {"taxa_base": 50, "valor_km": 5.50, "ponto_f1": 5, "ponto_f2": 7, "ponto_f3": 9},
        "Fiorino": {"taxa_base": 80, "valor_km": 7.00, "ponto_f1": 7, "ponto_f2": 9, "ponto_f3": 12},
        "Van": {"taxa_base": 130, "valor_km": 8.50, "ponto_f1": 9, "ponto_f2": 12, "ponto_f3": 16},
        "VUC": {"taxa_base": 160, "valor_km": 8.50, "ponto_f1": 10, "ponto_f2": 14, "ponto_f3": 18},
        "3/4": {"taxa_base": 220, "valor_km": 10.00, "ponto_f1": 12, "ponto_f2": 16, "ponto_f3": 20},
        "Toco": {"taxa_base": 300, "valor_km": 11.50, "ponto_f1": 14, "ponto_f2": 18, "ponto_f3": 24},
        "Truck": {"taxa_base": 400, "valor_km": 13.00, "ponto_f1": 16, "ponto_f2": 20, "ponto_f3": 28},
        "Carreta": {"taxa_base": 550, "valor_km": 16.00, "ponto_f1": 18, "ponto_f2": 24, "ponto_f3": 32},
    },
    "PLUS": {
        "Moto": {"taxa_base": 22, "valor_km": 3.60, "ponto_f1": 2.50, "ponto_f2": 4, "ponto_f3": 5.50},
        "Carro": {"taxa_base": 40, "valor_km": 4.40, "ponto_f1": 4, "ponto_f2": 5.50, "ponto_f3": 7},
        "Fiorino": {"taxa_base": 64, "valor_km": 5.60, "ponto_f1": 5.50, "ponto_f2": 7, "ponto_f3": 9.50},
        "Van": {"taxa_base": 104, "valor_km": 6.80, "ponto_f1": 7, "ponto_f2": 9.50, "ponto_f3": 13},
        "VUC": {"taxa_base": 128, "valor_km": 6.80, "ponto_f1": 8, "ponto_f2": 11, "ponto_f3": 14.50},
        "3/4": {"taxa_base": 176, "valor_km": 8.00, "ponto_f1": 9.50, "ponto_f2": 13, "ponto_f3": 16},
        "Toco": {"taxa_base": 240, "valor_km": 9.20, "ponto_f1": 11, "ponto_f2": 14.50, "ponto_f3": 19},
        "Truck": {"taxa_base": 320, "valor_km": 10.40, "ponto_f1": 13, "ponto_f2": 16, "ponto_f3": 22},
        "Carreta": {"taxa_base": 440, "valor_km": 12.80, "ponto_f1": 14.50, "ponto_f2": 19, "ponto_f3": 26},
    },
    "PREMIUM": {
        "Moto": {"taxa_base": 18, "valor_km": 2.90, "ponto_f1": 2, "ponto_f2": 3.50, "ponto_f3": 5},
        "Carro": {"taxa_base": 32, "valor_km": 3.60, "ponto_f1": 3.50, "ponto_f2": 5, "ponto_f3": 6.50},
        "Fiorino": {"taxa_base": 52, "valor_km": 4.50, "ponto_f1": 5, "ponto_f2": 6.50, "ponto_f3": 8.50},
        "Van": {"taxa_base": 84, "valor_km": 5.50, "ponto_f1": 6.50, "ponto_f2": 8.50, "ponto_f3": 11},
        "VUC": {"taxa_base": 104, "valor_km": 5.50, "ponto_f1": 7, "ponto_f2": 10, "ponto_f3": 13},
        "3/4": {"taxa_base": 143, "valor_km": 6.50, "ponto_f1": 8.50, "ponto_f2": 11, "ponto_f3": 14},
        "Toco": {"taxa_base": 195, "valor_km": 7.50, "ponto_f1": 10, "ponto_f2": 13, "ponto_f3": 17},
        "Truck": {"taxa_base": 260, "valor_km": 8.50, "ponto_f1": 11, "ponto_f2": 14, "ponto_f3": 20},
        "Carreta": {"taxa_base": 358, "valor_km": 10.40, "ponto_f1": 13, "ponto_f2": 17, "ponto_f3": 23},
    }
}

VEICULOS_INFO = {
    "Moto": {"peso": "20 kg", "volume": "0,1 m\u00b3", "pallets": "", "desc": "Documentos e pequenos volumes"},
    "Carro": {"peso": "300 kg", "volume": "1 m\u00b3", "pallets": "", "desc": "Urg\u00eancias e encomendas leves"},
    "Fiorino": {"peso": "600 kg", "volume": "3,5 m\u00b3", "pallets": "", "desc": "Entregas urbanas leves"},
    "Van": {"peso": "1.500 kg", "volume": "12 m\u00b3", "pallets": "6", "desc": "E-commerce e cargas m\u00e9dias"},
    "VUC": {"peso": "2.000 kg", "volume": "18 m\u00b3", "pallets": "8", "desc": "Carga urbana (entra na ZMRC)"},
    "3/4": {"peso": "3.500 kg", "volume": "25 m\u00b3", "pallets": "10", "desc": "Distribui\u00e7\u00f5es regionais"},
    "Toco": {"peso": "7.000 kg", "volume": "35 m\u00b3", "pallets": "12-14", "desc": "Eixo simples, m\u00e9dia-pesada"},
    "Truck": {"peso": "14.000 kg", "volume": "45 m\u00b3", "pallets": "16-18", "desc": "Eixo duplo, grandes volumes"},
    "Carreta": {"peso": "27.000 kg", "volume": "90 m\u00b3", "pallets": "24-28", "desc": "Carga completa pesada"},
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
# FUNCOES
# ============================================================
def get_credentials():
    creds_dict = dict(st.secrets["gcp_service_account"])
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    return Credentials.from_service_account_info(creds_dict, scopes=scopes)


def conectar_gsheets():
    if not GSHEETS_DISPONIVEL:
        return None
    try:
        return gspread.authorize(get_credentials())
    except Exception:
        return None


def get_drive_service():
    if not GDRIVE_DISPONIVEL:
        return None
    try:
        return build('drive', 'v3', credentials=get_credentials())
    except Exception:
        return None


def upload_file_to_drive(uploaded_file, nome_motorista, tipo_doc):
    service = get_drive_service()
    if service is None:
        return ""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        extensao = uploaded_file.name.split('.')[-1]
        nome_arquivo = f"{nome_motorista}_{tipo_doc}_{timestamp}.{extensao}"
        file_metadata = {'name': nome_arquivo, 'parents': [PASTA_DOCUMENTOS_ID]}
        media = MediaIoBaseUpload(io.BytesIO(uploaded_file.getvalue()), mimetype=uploaded_file.type, resumable=True)
        file = service.files().create(body=file_metadata, media_body=media, fields='id, webViewLink').execute()
        return file.get('webViewLink', '')
    except Exception as e:
        st.error(f"Erro no upload ({tipo_doc}): {str(e)}")
        return ""


def salvar_motorista_gsheets(dados):
    client = conectar_gsheets()
    if client is None:
        return False
    try:
        planilha = client.open("Transfelog - Motoristas")
        planilha.sheet1.append_row(dados)
        return True
    except Exception:
        return False


def salvar_cotacao_gsheets(dados):
    client = conectar_gsheets()
    if client is None:
        return False
    try:
        planilha = client.open("Transfelog - Cotacoes")
        planilha.sheet1.append_row(dados)
        return True
    except Exception:
        return False


def formatar_brl(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def identificar_tier(codigo):
    return CODIGOS_TIER.get(codigo.strip(), None)


def validar_cupom(cupom):
    cupom_upper = cupom.strip().upper()
    if cupom_upper in CUPONS_DESCONTO:
        dados = CUPONS_DESCONTO[cupom_upper]
        validade = datetime.strptime(dados["validade"], "%Y-%m-%d")
        if datetime.now() <= validade:
            return dados
    return None


def calcular_km_cobrado(km_ida):
    if km_ida <= 50:
        return km_ida
    elif km_ida <= 150:
        return km_ida + (km_ida * 0.50)
    else:
        return km_ida + (km_ida * 0.60)


def calcular_peso_taxado(peso_real_kg, volume_m3):
    peso_cubado = volume_m3 * FATOR_CUBAGEM
    return max(peso_real_kg, peso_cubado), peso_cubado


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
    taxas = {"PREMIUM": 0.0018, "PLUS": 0.0021, "BASE": 0.0023}
    taxa = taxas.get(tier, 0.0023)
    return max(valor_mercadoria * taxa, PROTECAO_MINIMO)


def calcular_cotacao(veiculo, tier, km_ida, n_pontos, tipo_carga, pct_complemento, protecao_ativa, valor_mercadoria, adicional_sel, cupom_dados):
    preco = PRECOS[tier][veiculo]
    km_cobrado = calcular_km_cobrado(km_ida)
    taxa_base = preco["taxa_base"]
    valor_km = km_cobrado * preco["valor_km"]
    taxa_pontos = calcular_taxa_pontos(n_pontos, preco)
    subtotal = taxa_base + valor_km + taxa_pontos
    if tipo_carga == "Complemento":
        subtotal = subtotal * (pct_complemento / 100)
    valor_adicional = subtotal * ADICIONAIS.get(adicional_sel, 0)
    valor_protecao = calcular_protecao(valor_mercadoria, tier) if protecao_ativa and valor_mercadoria > 0 else 0
    total_bruto = subtotal + valor_adicional + valor_protecao
    desconto = total_bruto * (cupom_dados["desconto_pct"] / 100) if cupom_dados else 0
    total = total_bruto - desconto
    custo_mot = total * CUSTO_MOTORISTA_PCT
    margem = total - custo_mot
    margem_pct = (margem / total * 100) if total > 0 else 0
    return {
        "taxa_base": taxa_base, "valor_km": valor_km, "km_cobrado": km_cobrado,
        "taxa_pontos": taxa_pontos, "subtotal": subtotal, "adicional": valor_adicional,
        "protecao": valor_protecao, "desconto": desconto, "total": round(total, 2),
        "custo_motorista": round(custo_mot, 2), "margem": round(margem, 2),
        "margem_pct": round(margem_pct, 1),
    }


def formato_veiculo(v):
    info = VEICULOS_INFO[v]
    texto = f"{v}  \u2022  {info['peso']}  \u2022  {info['volume']}"
    if info['pallets']:
        texto += f"  \u2022  {info['pallets']} pallets"
    return texto


# ============================================================
# HEADER - LOGO GRANDE
# ============================================================
logo_html = ""
if logo_b64:
    logo_html = f'<img src="data:image/png;base64,{logo_b64}">'

st.markdown(f'<div class="app-header">{logo_html}</div>', unsafe_allow_html=True)

# ============================================================
# MENU - FINO (TABS TEXTO)
# ============================================================
if "aba" not in st.session_state:
    st.session_state.aba = "Cotacao"

st.markdown("")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Cota\u00e7\u00e3o", key="t1", use_container_width=True):
        st.session_state.aba = "Cotacao"
        st.rerun()
with col2:
    if st.button("Rotas", key="t2", use_container_width=True):
        st.session_state.aba = "Roteirizador"
        st.rerun()
with col3:
    if st.button("Motorista", key="t3", use_container_width=True):
        st.session_state.aba = "Motorista"
        st.rerun()

aba = st.session_state.aba

# ============================================================
# ABA: COTACAO
# ============================================================
if aba == "Cotacao":

    st.markdown('<p class="sec-label">Acesso</p>', unsafe_allow_html=True)
    codigo_cliente = st.text_input("Codigo", type="password", placeholder="Digite seu c\u00f3digo de acesso", label_visibility="collapsed")
    tier_ativo = identificar_tier(codigo_cliente) if codigo_cliente else None

    if codigo_cliente and tier_ativo is None:
        st.error("C\u00f3digo inv\u00e1lido.")
    elif tier_ativo:
        badge_class = f"badge-{tier_ativo.lower()}"
        st.markdown(f'<span class="badge {badge_class}">{tier_ativo}</span>', unsafe_allow_html=True)

    if tier_ativo:

        st.markdown('<p class="sec-label">Cupom</p>', unsafe_allow_html=True)
        cupom_input = st.text_input("Cupom", placeholder="C\u00f3digo promocional (opcional)", label_visibility="collapsed")
        cupom_dados = validar_cupom(cupom_input) if cupom_input else None
        if cupom_input:
            if cupom_dados:
                st.markdown(f'<span class="badge badge-cupom">{cupom_dados["descricao"]}</span>', unsafe_allow_html=True)
            else:
                st.caption("Cupom inv\u00e1lido ou expirado.")

        st.markdown('<p class="sec-label">Ve\u00edculo</p>', unsafe_allow_html=True)
        veiculo_selecionado = st.selectbox("Veiculo", list(VEICULOS_INFO.keys()), format_func=formato_veiculo, label_visibility="collapsed")
        st.caption(VEICULOS_INFO[veiculo_selecionado]["desc"])

        st.markdown('<p class="sec-label">Carga</p>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            tipo_carga = st.selectbox("Tipo", ["Carga Completa", "Complemento"], label_visibility="collapsed")
        with col2:
            percentual_complemento = 100
            if tipo_carga == "Complemento":
                percentual_complemento = st.slider("Ocupa\u00e7\u00e3o (%)", 40, 100, 60)
            else:
                st.caption("Exclusivo")

        col_p, col_v = st.columns(2)
        with col_p:
            peso_real = st.number_input("Peso (kg)", min_value=1.0, value=500.0, step=50.0)
        with col_v:
            volume_carga = st.number_input("Volume (m\u00b3)", min_value=0.1, value=2.0, step=0.5)
        peso_taxado, peso_cubado = calcular_peso_taxado(peso_real, volume_carga)
        if peso_cubado > peso_real:
            st.caption(f"Cubado: {peso_cubado:.0f} kg \u2014 cobrado pelo volume.")
        else:
            st.caption(f"Peso real: {peso_real:.0f} kg")

        st.markdown('<p class="sec-label">Percurso</p>', unsafe_allow_html=True)
        col_km, col_par = st.columns(2)
        with col_km:
            km_ida = st.number_input("Dist\u00e2ncia ida (km)", min_value=1.0, max_value=1000.0, value=25.0, step=1.0)
        with col_par:
            n_paradas = st.number_input("Paradas", min_value=1, max_value=20, value=3, step=1)

        if km_ida > 0:
            km_cobrado = calcular_km_cobrado(km_ida)
            if km_ida > 50:
                pct = 50 if km_ida <= 150 else 60
                st.caption(f"Cobrado: {km_cobrado:.0f} km (ida + {pct}% retorno)")
            else:
                st.caption(f"{km_cobrado:.0f} km (somente ida)")

        st.markdown('<p class="sec-label">Endere\u00e7os (opcional)</p>', unsafe_allow_html=True)
        col_o, col_d = st.columns(2)
        with col_o:
            endereco_origem = st.text_input("Origem", placeholder="Rua, n\u00ba - Cidade")
        with col_d:
            endereco_destino = st.text_input("Destino", placeholder="Rua, n\u00ba - Cidade")

        st.markdown('<p class="sec-label">Per\u00edodo</p>', unsafe_allow_html=True)
        adicional = st.selectbox("Periodo", list(ADICIONAIS.keys()), label_visibility="collapsed")
        if ADICIONAIS[adicional] > 0:
            st.caption(f"+{int(ADICIONAIS[adicional]*100)}% sobre o subtotal")

        st.markdown('<p class="sec-label">Prote\u00e7\u00e3o de carga</p>', unsafe_allow_html=True)
        col_t, col_val = st.columns([1, 2])
        with col_t:
            protecao_ativa = st.toggle("Ativar", value=True)
        with col_val:
            valor_mercadoria = 0.0
            if protecao_ativa:
                valor_mercadoria = st.number_input("Valor mercadoria (R$)", min_value=0.0, value=10000.0, step=1000.0, format="%.2f")
                taxa_prot = {"PREMIUM": "0,18%", "PLUS": "0,21%", "BASE": "0,23%"}
                st.caption(f"Taxa: {taxa_prot[tier_ativo]} \u2022 M\u00edn. R$ 5,00")

        st.markdown('<div class="alert alert-warn">Ped\u00e1gio, taxas de acesso, estadias e ajudantes cobrados \u00e0 parte.</div>', unsafe_allow_html=True)

        st.markdown("")
        with st.container():
            st.markdown('<div class="calc-btn">', unsafe_allow_html=True)
            calcular = st.button("CALCULAR FRETE", use_container_width=True, key="btn_calc")
            st.markdown('</div>', unsafe_allow_html=True)

        if calcular:
            if km_ida <= 0:
                st.error("Informe a dist\u00e2ncia.")
            else:
                resultado = calcular_cotacao(
                    veiculo_selecionado, tier_ativo, km_ida, n_paradas,
                    tipo_carga, percentual_complemento, protecao_ativa,
                    valor_mercadoria, adicional, cupom_dados
                )

                dados_cotacao = [
                    datetime.now().strftime("%d/%m/%Y %H:%M"),
                    tier_ativo, veiculo_selecionado, tipo_carga,
                    f"{km_ida:.0f}", f"{resultado['km_cobrado']:.0f}",
                    str(n_paradas), adicional,
                    "Sim" if protecao_ativa else "N\u00e3o",
                    f"{valor_mercadoria:.2f}",
                    cupom_input if cupom_dados else "",
                    formatar_brl(resultado['total']),
                    formatar_brl(resultado['margem']),
                    endereco_origem, endereco_destino,
                ]
                salvar_cotacao_gsheets(dados_cotacao)

                st.markdown(f'''<div class="result-card">
                    <div class="label">Valor do frete</div>
                    <div class="value">{formatar_brl(resultado["total"])}</div>
                    <div class="sub">{veiculo_selecionado} \u2022 {resultado["km_cobrado"]:.0f} km \u2022 {n_paradas} parada{"s" if n_paradas > 1 else ""}</div>
                </div>''', unsafe_allow_html=True)

                st.markdown(f'''<div class="kpi-row">
                    <div class="kpi-box"><div class="n">{resultado["km_cobrado"]:.0f}</div><div class="l">KM</div></div>
                    <div class="kpi-box"><div class="n">{n_paradas}</div><div class="l">Paradas</div></div>
                    <div class="kpi-box"><div class="n">{veiculo_selecionado}</div><div class="l">Ve\u00edculo</div></div>
                </div>''', unsafe_allow_html=True)

                preco_km_unit = PRECOS[tier_ativo][veiculo_selecionado]['valor_km']
                bk = '<div class="bk">'
                bk += f'<div class="bk-row"><span class="n">Taxa base</span><span class="v">{formatar_brl(resultado["taxa_base"])}</span></div>'
                bk += f'<div class="bk-row"><span class="n">KM ({resultado["km_cobrado"]:.0f} x {formatar_brl(preco_km_unit)})</span><span class="v">{formatar_brl(resultado["valor_km"])}</span></div>'
                bk += f'<div class="bk-row"><span class="n">Paradas ({n_paradas}x)</span><span class="v">{formatar_brl(resultado["taxa_pontos"])}</span></div>'
                if tipo_carga == "Complemento":
                    bk += f'<div class="bk-row"><span class="n">Complemento ({percentual_complemento}%)</span><span class="v">Aplicado</span></div>'
                if resultado['adicional'] > 0:
                    bk += f'<div class="bk-row"><span class="n">{adicional}</span><span class="v">{formatar_brl(resultado["adicional"])}</span></div>'
                if resultado['protecao'] > 0:
                    bk += f'<div class="bk-row"><span class="n">Prote\u00e7\u00e3o de carga</span><span class="v">{formatar_brl(resultado["protecao"])}</span></div>'
                if resultado['desconto'] > 0:
                    bk += f'<div class="bk-row"><span class="n">Desconto cupom</span><span class="v" style="color:var(--green)">-{formatar_brl(resultado["desconto"])}</span></div>'
                bk += f'<div class="bk-total"><span class="n">Total</span><span class="v">{formatar_brl(resultado["total"])}</span></div>'
                bk += '</div>'
                st.markdown(bk, unsafe_allow_html=True)

                if peso_cubado > peso_real:
                    st.markdown(f'<div class="alert alert-warn">Peso cubado ({peso_cubado:.0f} kg) maior que real ({peso_real:.0f} kg). Cobran\u00e7a pelo volume.</div>', unsafe_allow_html=True)

                msg_wpp = f"Ol\u00e1! Solicito frete.\n\n*Cota\u00e7\u00e3o Transfelog*\nVe\u00edculo: {veiculo_selecionado}\nDist\u00e2ncia: {km_ida} km (cobrado: {resultado['km_cobrado']:.0f} km)\nPontos: {n_paradas}\nPer\u00edodo: {adicional}\nTipo: {tipo_carga}\nPeso: {peso_taxado:.0f} kg\n"
                if protecao_ativa:
                    msg_wpp += f"Prote\u00e7\u00e3o: Sim ({formatar_brl(valor_mercadoria)})\n"
                else:
                    msg_wpp += "Prote\u00e7\u00e3o: N\u00e3o\n"
                if endereco_origem:
                    msg_wpp += f"\nOrigem: {endereco_origem}\n"
                if endereco_destino:
                    msg_wpp += f"Destino: {endereco_destino}\n"
                msg_wpp += f"\n*TOTAL: {formatar_brl(resultado['total'])}*\nPed\u00e1gio \u00e0 parte.\n\nConfirmar frete."
                url_wpp = f"https://wa.me/{WHATSAPP_TRANSFELOG}?text={urllib.parse.quote(msg_wpp)}"
                st.markdown(f'<a href="{url_wpp}" target="_blank" class="wpp-btn">SOLICITAR VIA WHATSAPP</a>', unsafe_allow_html=True)

    else:
        if not codigo_cliente:
            st.markdown("")
            st.caption("Insira seu c\u00f3digo de acesso para come\u00e7ar.")

# ============================================================
# ABA: ROTEIRIZADOR
# ============================================================
elif aba == "Roteirizador":
    st.markdown('<p class="sec-label">Roteirizador</p>', unsafe_allow_html=True)
    st.markdown('<div class="alert alert-info">Em desenvolvimento. Previs\u00e3o: Vers\u00e3o 2.</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown("**Funcionalidades planejadas:**")
    st.markdown("")
    st.markdown("\u2022 Origem fixa + m\u00faltiplos destinos")
    st.markdown("\u2022 Otimiza\u00e7\u00e3o por menor km")
    st.markdown("\u2022 Reordenar paradas manualmente")
    st.markdown("\u2022 Endere\u00e7os prontos para colar no Lalamove")
    st.markdown("\u2022 C\u00e1lculo integrado com Google Maps")
    st.markdown('</div>', unsafe_allow_html=True)
    st.caption("Use o KM manual na aba Cota\u00e7\u00e3o.")

# ============================================================
# ABA: MOTORISTA
# ============================================================
elif aba == "Motorista":

    st.markdown('<p class="sec-label">Cadastro para aprova\u00e7\u00e3o</p>', unsafe_allow_html=True)
    st.caption("Retorno em at\u00e9 48h \u00fateis.")

    nome_completo = st.text_input("Nome completo")

    st.markdown('<p class="sec-label">Endere\u00e7o</p>', unsafe_allow_html=True)
    col_cep, col_rua = st.columns([1, 2])
    with col_cep:
        cep_motorista = st.text_input("CEP", placeholder="09720-000")
    with col_rua:
        endereco_mot = st.text_input("Rua, n\u00famero e bairro")
    col_cid, col_est = st.columns(2)
    with col_cid:
        cidade_motorista = st.text_input("Cidade")
    with col_est:
        estado_motorista = st.text_input("Estado", placeholder="SP")

    st.markdown('<p class="sec-label">Contato</p>', unsafe_allow_html=True)
    col_tel, col_wpp = st.columns(2)
    with col_tel:
        telefone = st.text_input("Telefone")
    with col_wpp:
        whatsapp_motorista = st.text_input("WhatsApp", placeholder="11 98765-4321")
    email_motorista = st.text_input("E-mail")

    st.markdown('<p class="sec-label">Ve\u00edculo</p>', unsafe_allow_html=True)
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        veiculo_motorista = st.selectbox("Tipo", list(VEICULOS_INFO.keys()), format_func=lambda v: f"{v} ({VEICULOS_INFO[v]['peso']})", key="veiculo_mot")
    with col_v2:
        placa = st.text_input("Placa", placeholder="ABC1D23")
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        capacidade_peso = st.number_input("Capacidade (kg)", min_value=1, value=2000, step=100)
    with col_c2:
        capacidade_volume = st.number_input("Capacidade (m\u00b3)", min_value=1.0, value=18.0, step=1.0)
    ano_veiculo = st.text_input("Ano do ve\u00edculo", placeholder="2020")
    possui_rastreador = st.radio("Possui rastreador?", ["Sim", "N\u00e3o"], horizontal=True)

    st.markdown('<p class="sec-label">Valor por km</p>', unsafe_allow_html=True)
    valor_km_desejado = st.number_input("R$/km", min_value=1.0, max_value=20.0, value=5.00, step=0.50)
    st.caption("R$ 3,00 a R$ 8,00/km \u2014 competitivo na regi\u00e3o.")

    st.markdown('<p class="sec-label">Disponibilidade</p>', unsafe_allow_html=True)
    disponibilidade = st.multiselect("Dias", ["Segunda", "Ter\u00e7a", "Quarta", "Quinta", "Sexta", "S\u00e1bado", "Domingo"], default=["Segunda", "Ter\u00e7a", "Quarta", "Quinta", "Sexta"])
    horario = st.selectbox("Hor\u00e1rio", ["Integral (08h \u00e0s 20h)", "Manh\u00e3 (06h \u00e0s 14h)", "Tarde (12h \u00e0s 20h)", "Noturno (18h \u00e0s 06h)", "Flex\u00edvel"])
    regiao_atuacao = st.text_input("Regi\u00e3o de atua\u00e7\u00e3o", placeholder="ABC Paulista, Grande SP...")

    st.markdown('<p class="sec-label">Documentos</p>', unsafe_allow_html=True)
    st.caption("PNG, JPG ou PDF.")
    cnh_upload = st.file_uploader("CNH (frente e verso)", type=["png", "jpg", "jpeg", "pdf"], key="cnh")
    doc_veiculo_upload = st.file_uploader("CRLV", type=["png", "jpg", "jpeg", "pdf"], key="doc_veic")
    foto_veiculo = st.file_uploader("Foto do ve\u00edculo (opcional)", type=["png", "jpg", "jpeg"], key="foto_veic")

    st.markdown("")
    aceite = st.checkbox("Declaro que as informa\u00e7\u00f5es s\u00e3o verdadeiras e aceito os termos.")
    st.markdown("")

    with st.container():
        st.markdown('<div class="calc-btn">', unsafe_allow_html=True)
        enviar = st.button("ENVIAR CADASTRO", use_container_width=True, key="btn_enviar")
        st.markdown('</div>', unsafe_allow_html=True)

    if enviar:
        obrigatorios = [nome_completo, cep_motorista, endereco_mot, cidade_motorista, estado_motorista, telefone, whatsapp_motorista, email_motorista, placa, cnh_upload, doc_veiculo_upload]
        if not all(obrigatorios):
            st.error("Preencha todos os campos obrigat\u00f3rios e anexe CNH + CRLV.")
        elif not aceite:
            st.error("Aceite os termos para continuar.")
        elif len(disponibilidade) == 0:
            st.error("Selecione ao menos um dia.")
        else:
            with st.spinner("Enviando cadastro..."):
                link_cnh = upload_file_to_drive(cnh_upload, nome_completo, "CNH") if cnh_upload else ""
                link_crlv = upload_file_to_drive(doc_veiculo_upload, nome_completo, "CRLV") if doc_veiculo_upload else ""
                link_foto = upload_file_to_drive(foto_veiculo, nome_completo, "FOTO_VEICULO") if foto_veiculo else ""
                dados_motorista = [
                    datetime.now().strftime("%d/%m/%Y %H:%M"),
                    nome_completo, cep_motorista, endereco_mot,
                    cidade_motorista, estado_motorista,
                    telefone, whatsapp_motorista, email_motorista,
                    veiculo_motorista, placa,
                    str(capacidade_peso), str(capacidade_volume),
                    ano_veiculo, possui_rastreador,
                    f"R$ {valor_km_desejado:.2f}",
                    ", ".join(disponibilidade), horario, regiao_atuacao,
                    "Pendente", link_cnh, link_crlv, link_foto,
                ]
                sucesso_sheets = salvar_motorista_gsheets(dados_motorista)

            if sucesso_sheets:
                st.markdown(f'<div class="alert alert-ok">Cadastro enviado! Retorno em at\u00e9 48h no WhatsApp: <b>{whatsapp_motorista}</b></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="alert alert-ok">Registrado! Contato: <b>{whatsapp_motorista}</b></div>', unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================
st.markdown('<div class="app-footer">Desenvolvido por Grupo Transfelog do Brasil</div>', unsafe_allow_html=True)
