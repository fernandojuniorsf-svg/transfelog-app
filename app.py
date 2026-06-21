```python
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

st.set_page_config(page_title="Transfelog App", page_icon="T", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
.stApp{background:linear-gradient(160deg,#f0f4f7 0%,#e8eef3 50%,#f5f8fa 100%);font-family:'Inter',sans-serif}
.app-header{background:linear-gradient(135deg,#1a2332 0%,#243447 40%,#4A9BA8 100%);padding:3rem 2rem;border-radius:20px;margin-bottom:1rem;box-shadow:0 12px 40px rgba(74,155,168,0.2);display:flex;flex-direction:column;align-items:center;text-align:center}
.app-header img{height:280px;border-radius:0;object-fit:contain;mix-blend-mode:screen}
.section-label{color:#1a2332;font-size:0.85rem;font-weight:600;text-transform:uppercase;letter-spacing:0.8px;margin:2rem 0 0.8rem 0;padding-left:0.5rem;border-left:3px solid #4A9BA8}
.result-card{background:linear-gradient(135deg,#fff 0%,#f4fafb 100%);border-radius:20px;padding:2.5rem;box-shadow:0 8px 32px rgba(74,155,168,0.1);border:1px solid rgba(74,155,168,0.15);margin:1.5rem 0;text-align:center}
.result-label{color:#6b7280;font-size:0.75rem;text-transform:uppercase;letter-spacing:1px;font-weight:500}
.result-total{font-size:3rem;font-weight:800;background:linear-gradient(135deg,#4A9BA8 0%,#2d7a85 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin:0.5rem 0}
.tier-badge-premium{background:linear-gradient(135deg,#f59e0b,#d97706);color:#fff;padding:0.3rem 0.8rem;border-radius:6px;font-size:0.72rem;font-weight:600;display:inline-block}
.tier-badge-plus{background:linear-gradient(135deg,#4A9BA8,#3a7f8a);color:#fff;padding:0.3rem 0.8rem;border-radius:6px;font-size:0.72rem;font-weight:600;display:inline-block}
.tier-badge-base{background:linear-gradient(135deg,#6b7280,#4b5563);color:#fff;padding:0.3rem 0.8rem;border-radius:6px;font-size:0.72rem;font-weight:600;display:inline-block}
.kpi-row{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin:1.5rem 0}
.kpi-item{background:#fff;border-radius:14px;padding:1.2rem;text-align:center;box-shadow:0 2px 10px rgba(0,0,0,0.04);border:1px solid #f0f0f0}
.kpi-item-label{color:#9ca3af;font-size:0.7rem;text-transform:uppercase;letter-spacing:0.5px;font-weight:500}
.kpi-item-value{color:#1a2332;font-size:1.4rem;font-weight:700;margin-top:0.3rem}
.breakdown-card{background:#fff;border-radius:14px;padding:1.5rem;box-shadow:0 2px 10px rgba(0,0,0,0.04);margin:1rem 0}
.breakdown-row{display:flex;justify-content:space-between;align-items:center;padding:0.7rem 0;border-bottom:1px solid #f5f5f5}
.breakdown-row:last-child{border-bottom:none}
.breakdown-name{color:#4b5563;font-size:0.85rem}
.breakdown-value{color:#1a2332;font-size:0.85rem;font-weight:600}
.breakdown-total{display:flex;justify-content:space-between;align-items:center;padding:1rem 0 0 0;margin-top:0.5rem;border-top:2px solid #4A9BA8}
.breakdown-total-label{color:#1a2332;font-size:0.9rem;font-weight:700}
.breakdown-total-value{color:#4A9BA8;font-size:1.2rem;font-weight:800}
.info-box{background:#fffbeb;border:1px solid #fde68a;border-radius:10px;padding:0.8rem 1rem;font-size:0.8rem;color:#92400e;margin:1rem 0}
.success-box{background:#ecfdf5;border:1px solid #6ee7b7;border-radius:10px;padding:0.8rem 1rem;font-size:0.8rem;color:#065f46;margin:1rem 0}
.dev-box{background:#f0f4ff;border:1px solid #bfdbfe;border-radius:10px;padding:0.8rem 1rem;font-size:0.8rem;color:#1e40af;margin:1rem 0}
.cupom-badge{background:linear-gradient(135deg,#10b981,#059669);color:#fff;padding:0.3rem 0.8rem;border-radius:6px;font-size:0.72rem;font-weight:600;display:inline-block;margin-left:0.5rem}
.whatsapp-btn{display:block;background:linear-gradient(135deg,#25D366,#128C7E);color:#fff !important;padding:0.9rem 2rem;border-radius:14px;font-weight:600;font-size:1rem;text-decoration:none;text-align:center;width:100%;box-shadow:0 6px 20px rgba(37,211,102,0.3);margin-top:1rem}
.whatsapp-btn:hover{background:linear-gradient(135deg,#20bd5a,#0f7a6b);color:#fff !important;text-decoration:none}
.stButton>button{background:linear-gradient(135deg,#4A9BA8 0%,#3a7f8a 100%);color:#fff;border:none;border-radius:14px;padding:0.9rem 2.5rem;font-weight:600;font-size:1rem;box-shadow:0 6px 20px rgba(74,155,168,0.3)}
.stButton>button:hover{background:linear-gradient(135deg,#3d8a96 0%,#2d7580 100%);box-shadow:0 8px 28px rgba(74,155,168,0.4)}
.app-footer{text-align:center;color:#b0b8c4;font-size:0.68rem;margin-top:3rem;padding:1.5rem;border-top:1px solid #e8eef3}
#MainMenu{visibility:hidden}
footer{visibility:hidden}
header{visibility:hidden}
.stSelectbox>div>div{border-radius:12px}
.stTextInput>div>div>input{border-radius:12px}
.stNumberInput>div>div>input{border-radius:12px}
</style>
""", unsafe_allow_html=True)

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
    "Toco": {"peso": "7.000 kg", "volume": "35 m\u00b3", "pallets": "12-14", "desc": "Eixo simples, carga m\u00e9dia-pesada"},
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
# FUNCOES DE CONEXAO
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


# ============================================================
# FUNCOES DE CALCULO
# ============================================================
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


def calcular_custo_motorista(total_cotacao):
    return total_cotacao * CUSTO_MOTORISTA_PCT


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
    custo_mot = calcular_custo_motorista(total)
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
    texto = f"{v}  |  {info['peso']}  |  {info['volume']}"
    if info['pallets']:
        texto += f"  |  {info['pallets']} pallets"
    return texto


# ============================================================
# HEADER
# ============================================================
LOGO_FILENAME = "ChatGPT Image Jun 20, 2026, 07_39_44 PM.png"
logo_html = ""
if os.path.exists(LOGO_FILENAME):
    with open(LOGO_FILENAME, "rb") as f:
        logo_b64 = base64.b64encode(f.read()).decode()
    logo_html = f'<img src="data:image/png;base64,{logo_b64}">'

st.markdown(f'<div class="app-header">{logo_html}</div>', unsafe_allow_html=True)

# ============================================================
# MENU
# ============================================================
st.markdown("")
aba = st.radio("Menu", ["Cota\u00e7\u00e3o de Frete", "Roteirizador", "Cadastro de Motorista"], horizontal=True, label_visibility="collapsed")
st.markdown("")

# ============================================================
# ABA: COTACAO DE FRETE
# ============================================================
if aba == "Cota\u00e7\u00e3o de Frete":

    st.markdown('<div class="section-label">Acesso</div>', unsafe_allow_html=True)
    codigo_cliente = st.text_input("C\u00f3digo", type="password", placeholder="Insira seu c\u00f3digo de acesso", label_visibility="collapsed")
    tier_ativo = identificar_tier(codigo_cliente) if codigo_cliente else None

    if codigo_cliente and tier_ativo is None:
        st.error("C\u00f3digo inv\u00e1lido. Verifique com seu consultor.")
    elif tier_ativo:
        st.markdown(f'<span class="tier-badge-{tier_ativo.lower()}">{tier_ativo}</span>', unsafe_allow_html=True)

    if tier_ativo:

        st.markdown('<div class="section-label">Cupom de desconto</div>', unsafe_allow_html=True)
        cupom_input = st.text_input("Cupom", placeholder="Cupom (opcional)", label_visibility="collapsed")
        cupom_dados = validar_cupom(cupom_input) if cupom_input else None
        if cupom_input:
            if cupom_dados:
                st.markdown(f'<span class="cupom-badge">{cupom_dados["descricao"]}</span>', unsafe_allow_html=True)
            else:
                st.caption("Cupom inv\u00e1lido ou expirado.")

        st.markdown('<div class="section-label">Ve\u00edculo</div>', unsafe_allow_html=True)
        veiculo_selecionado = st.selectbox("Selecione", list(VEICULOS_INFO.keys()), format_func=formato_veiculo, label_visibility="collapsed")
        st.caption(VEICULOS_INFO[veiculo_selecionado]["desc"])

        st.markdown('<div class="section-label">Tipo de carga</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            tipo_carga = st.selectbox("Tipo", ["Carga Completa", "Complemento"], label_visibility="collapsed")
        with col2:
            percentual_complemento = 100
            if tipo_carga == "Complemento":
                percentual_complemento = st.slider("Espa\u00e7o utilizado (%)", 40, 100, 60)
            else:
                st.caption("Ve\u00edculo exclusivo")

        st.markdown('<div class="section-label">Peso e volume</div>', unsafe_allow_html=True)
        col_peso, col_vol = st.columns(2)
        with col_peso:
            peso_real = st.number_input("Peso real (kg)", min_value=1.0, value=500.0, step=50.0)
        with col_vol:
            volume_carga = st.number_input("Volume (m\u00b3)", min_value=0.1, value=2.0, step=0.5)
        peso_taxado, peso_cubado = calcular_peso_taxado(peso_real, volume_carga)
        if peso_cubado > peso_real:
            st.caption(f"Peso cubado: {peso_cubado:.0f} kg (volume x {FATOR_CUBAGEM}). Cobrado pelo volume.")
        else:
            st.caption(f"Cobrado pelo peso real ({peso_real:.0f} kg).")

        st.markdown('<div class="section-label">Percurso</div>', unsafe_allow_html=True)
        col_km, col_par = st.columns(2)
        with col_km:
            km_ida = st.number_input("Dist\u00e2ncia ida (km)", min_value=1.0, max_value=1000.0, value=25.0, step=1.0)
        with col_par:
            n_paradas = st.number_input("Pontos de entrega", min_value=1, max_value=20, value=3, step=1)

        if km_ida > 0:
            km_cobrado = calcular_km_cobrado(km_ida)
            if km_ida > 50:
                pct = 50 if km_ida <= 150 else 60
                st.caption(f"KM cobrado: {km_cobrado:.0f} km (ida {km_ida:.0f} km + {pct}% retorno)")
            else:
                st.caption(f"KM cobrado: {km_cobrado:.0f} km (somente ida, at\u00e9 50 km)")

        st.markdown('<div class="section-label">Endere\u00e7os (opcional)</div>', unsafe_allow_html=True)
        st.caption("Preencha para constar na solicita\u00e7\u00e3o via WhatsApp.")
        col_o, col_d = st.columns(2)
        with col_o:
            endereco_origem = st.text_input("Origem", placeholder="Rua, n\u00famero - Cidade, SP")
        with col_d:
            endereco_destino = st.text_input("Destino", placeholder="Rua, n\u00famero - Cidade, SP")

        st.markdown('<div class="section-label">Per\u00edodo</div>', unsafe_allow_html=True)
        adicional = st.selectbox("Per\u00edodo", list(ADICIONAIS.keys()), label_visibility="collapsed")
        if ADICIONAIS[adicional] > 0:
            st.caption(f"Acr\u00e9scimo de {int(ADICIONAIS[adicional]*100)}% sobre o subtotal.")

        st.markdown('<div class="section-label">Prote\u00e7\u00e3o de carga Transfelog</div>', unsafe_allow_html=True)
        col_p1, col_p2 = st.columns([1, 2])
        with col_p1:
            protecao_ativa = st.toggle("Ativar", value=True)
        with col_p2:
            valor_mercadoria = 0.0
            if protecao_ativa:
                valor_mercadoria = st.number_input("Valor da mercadoria (R$)", min_value=0.0, value=10000.0, step=1000.0, format="%.2f")
                taxa_prot = {"PREMIUM": "0,18%", "PLUS": "0,21%", "BASE": "0,23%"}
                st.caption(f"Taxa: {taxa_prot[tier_ativo]} sobre o valor declarado. M\u00ednimo R$ 5,00.")

        st.markdown('<div class="info-box">Ped\u00e1gio, taxas de acesso, estadias e ajudantes n\u00e3o inclusos. Cobrados \u00e0 parte conforme necessidade.</div>', unsafe_allow_html=True)

        st.markdown("")
        calcular = st.button("CALCULAR COTA\u00c7\u00c3O", use_container_width=True)

        if calcular:
            if km_ida <= 0:
                st.error("Informe a dist\u00e2ncia para calcular.")
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

                st.markdown(f'<div class="result-card"><div class="result-label">VALOR DA COTA\u00c7\u00c3O</div><div class="result-total">{formatar_brl(resultado["total"])}</div></div>', unsafe_allow_html=True)

                kpi_html = f'''<div class="kpi-row">
                    <div class="kpi-item"><div class="kpi-item-label">KM cobrado</div><div class="kpi-item-value">{resultado["km_cobrado"]:.0f} km</div></div>
                    <div class="kpi-item"><div class="kpi-item-label">Paradas</div><div class="kpi-item-value">{n_paradas}</div></div>
                    <div class="kpi-item"><div class="kpi-item-label">Ve\u00edculo</div><div class="kpi-item-value">{veiculo_selecionado}</div></div>
                </div>'''
                st.markdown(kpi_html, unsafe_allow_html=True)

                preco_km_unit = PRECOS[tier_ativo][veiculo_selecionado]['valor_km']
                breakdown_html = '<div class="breakdown-card">'
                breakdown_html += f'<div class="breakdown-row"><span class="breakdown-name">Taxa base ({veiculo_selecionado})</span><span class="breakdown-value">{formatar_brl(resultado["taxa_base"])}</span></div>'
                breakdown_html += f'<div class="breakdown-row"><span class="breakdown-name">Quilometragem ({resultado["km_cobrado"]:.0f} km x {formatar_brl(preco_km_unit)}/km)</span><span class="breakdown-value">{formatar_brl(resultado["valor_km"])}</span></div>'
                breakdown_html += f'<div class="breakdown-row"><span class="breakdown-name">Pontos de entrega ({n_paradas} paradas)</span><span class="breakdown-value">{formatar_brl(resultado["taxa_pontos"])}</span></div>'
                if tipo_carga == "Complemento":
                    breakdown_html += f'<div class="breakdown-row"><span class="breakdown-name">Complemento ({percentual_complemento}% do ve\u00edculo)</span><span class="breakdown-value">Aplicado</span></div>'
                if resultado['adicional'] > 0:
                    breakdown_html += f'<div class="breakdown-row"><span class="breakdown-name">{adicional} (+{int(ADICIONAIS[adicional]*100)}%)</span><span class="breakdown-value">{formatar_brl(resultado["adicional"])}</span></div>'
                if resultado['protecao'] > 0:
                    breakdown_html += f'<div class="breakdown-row"><span class="breakdown-name">Prote\u00e7\u00e3o de carga ({formatar_brl(valor_mercadoria)} declarado)</span><span class="breakdown-value">{formatar_brl(resultado["protecao"])}</span></div>'
                if resultado['desconto'] > 0:
                    breakdown_html += f'<div class="breakdown-row"><span class="breakdown-name">Desconto cupom ({cupom_dados["descricao"]})</span><span class="breakdown-value" style="color:#059669;">- {formatar_brl(resultado["desconto"])}</span></div>'
                breakdown_html += f'<div class="breakdown-total"><span class="breakdown-total-label">Total</span><span class="breakdown-total-value">{formatar_brl(resultado["total"])}</span></div>'
                breakdown_html += '</div>'
                st.markdown(breakdown_html, unsafe_allow_html=True)

                if peso_cubado > peso_real:
                    st.markdown(f'<div class="info-box">Peso cubado ({peso_cubado:.0f} kg) maior que peso real ({peso_real:.0f} kg). Cobran\u00e7a pelo volume.</div>', unsafe_allow_html=True)

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
                st.markdown(f'<a href="{url_wpp}" target="_blank" class="whatsapp-btn">SOLICITAR FRETE VIA WHATSAPP</a>', unsafe_allow_html=True)

    else:
        if not codigo_cliente:
            st.caption("Insira seu c\u00f3digo de acesso para calcular.")

# ============================================================
# ABA: ROTEIRIZADOR (EM DESENVOLVIMENTO)
# ============================================================
elif aba == "Roteirizador":
    st.markdown('<div class="section-label">Roteirizador inteligente</div>', unsafe_allow_html=True)
    st.markdown('<div class="dev-box">Funcionalidade em desenvolvimento. Em breve voc\u00ea poder\u00e1 adicionar m\u00faltiplos endere\u00e7os, otimizar a rota pelo menor KM e calcular automaticamente a dist\u00e2ncia total com integra\u00e7\u00e3o Google Maps.</div>', unsafe_allow_html=True)
    st.markdown("")
    st.caption("Previs\u00e3o de lan\u00e7amento: V2 do Transfelog App")
    st.markdown("")
    st.markdown("**O que estar\u00e1 dispon\u00edvel:**")
    st.markdown("- Endere\u00e7o de origem fixo (sua sede)")
    st.markdown("- M\u00faltiplos pontos de entrega")
    st.markdown("- Otimiza\u00e7\u00e3o autom\u00e1tica de rota (menor km)")
    st.markdown("- Op\u00e7\u00e3o de manter ordem manual")
    st.markdown("- C\u00e1lculo autom\u00e1tico de km total")
    st.markdown("- Endere\u00e7os prontos para colar na Lalamove")
    st.markdown("- Reordenar paradas manualmente")
    st.markdown("")
    st.caption("Por enquanto, use o modo KM manual na aba de Cota\u00e7\u00e3o.")

# ============================================================
# ABA: CADASTRO DE MOTORISTA
# ============================================================
elif aba == "Cadastro de Motorista":

    st.markdown('<div class="section-label">Cadastro para aprova\u00e7\u00e3o</div>', unsafe_allow_html=True)
    st.caption("Preencha todos os campos abaixo. An\u00e1lise e retorno em at\u00e9 48 horas \u00fateis.")
    st.markdown("")

    nome_completo = st.text_input("Nome completo")

    st.markdown('<div class="section-label">Endere\u00e7o</div>', unsafe_allow_html=True)
    col_cep, col_rua = st.columns([1, 2])
    with col_cep:
        cep_motorista = st.text_input("CEP", placeholder="Ex: 09720-000")
    with col_rua:
        endereco_mot = st.text_input("Rua, n\u00famero e bairro")
    col_cid, col_est = st.columns(2)
    with col_cid:
        cidade_motorista = st.text_input("Cidade")
    with col_est:
        estado_motorista = st.text_input("Estado", placeholder="SP")

    st.markdown('<div class="section-label">Contato</div>', unsafe_allow_html=True)
    col_tel, col_wpp = st.columns(2)
    with col_tel:
        telefone = st.text_input("Telefone fixo/celular")
    with col_wpp:
        whatsapp_motorista = st.text_input("WhatsApp (principal)", placeholder="11 98765-4321")
    email_motorista = st.text_input("E-mail")

    st.markdown('<div class="section-label">Ve\u00edculo</div>', unsafe_allow_html=True)
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        veiculo_motorista = st.selectbox("Tipo de ve\u00edculo", list(VEICULOS_INFO.keys()), format_func=lambda v: f"{v} ({VEICULOS_INFO[v]['peso']})", key="veiculo_mot")
    with col_v2:
        placa = st.text_input("Placa do ve\u00edculo", placeholder="ABC1D23")
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        capacidade_peso = st.number_input("Capacidade peso (kg)", min_value=1, value=2000, step=100)
    with col_c2:
        capacidade_volume = st.number_input("Capacidade volume (m\u00b3)", min_value=1.0, value=18.0, step=1.0)
    ano_veiculo = st.text_input("Ano do ve\u00edculo", placeholder="Ex: 2020")
    possui_rastreador = st.radio("Possui rastreador?", ["Sim", "N\u00e3o"], horizontal=True)

    st.markdown('<div class="section-label">Valor desejado por km</div>', unsafe_allow_html=True)
    valor_km_desejado = st.number_input("Quanto deseja receber por km rodado (R$)", min_value=1.0, max_value=20.0, value=5.00, step=0.50, help="Sujeito \u00e0 aprova\u00e7\u00e3o conforme tabela vigente da Transfelog.")
    st.caption("Valores entre R$ 3,00 e R$ 8,00/km s\u00e3o os mais competitivos na regi\u00e3o.")

    st.markdown('<div class="section-label">Disponibilidade</div>', unsafe_allow_html=True)
    disponibilidade = st.multiselect("Dias dispon\u00edveis", ["Segunda", "Ter\u00e7a", "Quarta", "Quinta", "Sexta", "S\u00e1bado", "Domingo"], default=["Segunda", "Ter\u00e7a", "Quarta", "Quinta", "Sexta"])
    horario = st.selectbox("Hor\u00e1rio de prefer\u00eancia", ["Integral (08h \u00e0s 20h)", "Manh\u00e3 (06h \u00e0s 14h)", "Tarde (12h \u00e0s 20h)", "Noturno (18h \u00e0s 06h)", "Flex\u00edvel (qualquer hor\u00e1rio)"])
    regiao_atuacao = st.text_input("Regi\u00e3o de atua\u00e7\u00e3o preferencial", placeholder="Ex: ABC Paulista, Grande SP, Interior")

    st.markdown('<div class="section-label">Documentos</div>', unsafe_allow_html=True)
    st.caption("Envie fotos leg\u00edveis e atualizadas. Formatos aceitos: PNG, JPG ou PDF.")
    cnh_upload = st.file_uploader("CNH (frente e verso)", type=["png", "jpg", "jpeg", "pdf"], key="cnh")
    doc_veiculo_upload = st.file_uploader("Documento do ve\u00edculo (CRLV)", type=["png", "jpg", "jpeg", "pdf"], key="doc_veic")
    foto_veiculo = st.file_uploader("Foto do ve\u00edculo (opcional)", type=["png", "jpg", "jpeg"], key="foto_veic")

    st.markdown("")
    aceite = st.checkbox("Declaro que as informa\u00e7\u00f5es s\u00e3o verdadeiras e aceito os termos de parceria.")
    st.markdown("")
    enviar = st.button("ENVIAR CADASTRO", use_container_width=True)

    if enviar:
        obrigatorios = [nome_completo, cep_motorista, endereco_mot, cidade_motorista, estado_motorista, telefone, whatsapp_motorista, email_motorista, placa, cnh_upload, doc_veiculo_upload]
        if not all(obrigatorios):
            st.error("Preencha todos os campos obrigat\u00f3rios e anexe CNH + CRLV.")
        elif not aceite:
            st.error("Aceite os termos para enviar.")
        elif len(disponibilidade) == 0:
            st.error("Selecione ao menos um dia de disponibilidade.")
        else:
            with st.spinner("Enviando documentos..."):
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
                st.markdown(f'<div class="success-box">Cadastro enviado com sucesso! Documentos salvos.<br>Retorno em at\u00e9 48h no WhatsApp: <b>{whatsapp_motorista}</b></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="success-box">Cadastro registrado! Entraremos em contato pelo WhatsApp: <b>{whatsapp_motorista}</b></div>', unsafe_allow_html=True)

            st.markdown("")
            st.caption("Resumo do cadastro:")
            resumo_items = [
                f"| Nome | {nome_completo} |",
                f"| WhatsApp | {whatsapp_motorista} |",
                f"| CEP | {cep_motorista} |",
                f"| Endere\u00e7o | {endereco_mot}, {cidade_motorista} - {estado_motorista} |",
                f"| Ve\u00edculo | {veiculo_motorista} |",
                f"| Placa | {placa} |",
                f"| Ano | {ano_veiculo} |",
                f"| Rastreador | {possui_rastreador} |",
                f"| Capacidade | {capacidade_peso} kg / {capacidade_volume} m\u00b3 |",
                f"| Valor/km | R$ {valor_km_desejado:.2f} |",
                f"| Disponibilidade | {', '.join(disponibilidade)} |",
                f"| Hor\u00e1rio | {horario} |",
                f"| Regi\u00e3o | {regiao_atuacao} |",
                f"| CNH | {'Enviada' if link_cnh else 'Erro no envio'} |",
                f"| CRLV | {'Enviado' if link_crlv else 'Erro no envio'} |",
                f"| Foto | {'Enviada' if link_foto else 'N\u00e3o enviada'} |",
            ]
            resumo = "| Campo | Informa\u00e7\u00e3o |\n|-------|------------|\n" + "\n".join(resumo_items)
            st.markdown(resumo)

# ============================================================
# FOOTER
# ============================================================
st.markdown('<div class="app-footer">Desenvolvido por Grupo Transfelog do Brasil</div>', unsafe_allow_html=True)
