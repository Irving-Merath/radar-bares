import streamlit as st
import folium
from streamlit_folium import st_folium
import googlemaps

# 1. Configuração da Página
st.set_page_config(layout="wide", page_title="Radar do Chopp")
st.title("🍺 Radar do Chopp & Metrô")
st.write("Encontre o bar ideal a menos de 200m do metrô e em regiões seguras.")

# CHAVE
API_KEY = st.secrets["GOOGLE_MAPS_API_KEY"]

# 2. Dicionário Mestre de Estações (Suas coordenadas)
ESTACOES = {
    "Jardim Oceânico": "-23.0076,-43.3135",
    "São Conrado": "-22.9918,-43.2536",
    "Antero de Quental": "-22.9845,-43.2230",
    "Jardim de Alah": "-22.9836,-43.2146",
    "Nossa Senhora da Paz": "-22.9837,-43.2066",
    "General Osório": "-22.9847,-43.1947",
    "Cantagalo": "-22.9764,-43.1923",
    "Siqueira Campos": "-22.9673,-43.1866",
    "Cardeal Arcoverde": "-22.9646,-43.1812",
    "Botafogo": "-22.9511,-43.1837",
    "Flamengo": "-22.9312,-43.1764",
    "Largo do Machado": "-22.9311,-43.1774",
    "Catete": "-22.9260,-43.1767",
    "Glória": "-22.9195,-43.1765",
    "Cinelândia": "-22.9114,-43.1752",
    "Carioca": "-22.9073,-43.1776",
    "Presidente Vargas": "-22.9032,-43.1863",
    "Afonso Pena": "-22.9181,-43.2178",
    "São Francisco Xavier": "-22.9209,-43.2244",
    "Saens Peña": "-22.9242,-43.2325",
    "Uruguai": "-22.9333,-43.2384"
}

# 3. Superpoder de Memória: Cache
@st.cache_data
def buscar_bares_api(lista_estacoes):
    if not lista_estacoes:
        return []
        
    gmaps = googlemaps.Client(key=API_KEY)
    bares_aprovados = []
    
    # Roda o radar para CADA estação selecionada
    for estacao in lista_estacoes:
        coordenadas = ESTACOES[estacao]
        
        try:
            resposta = gmaps.places_nearby(
                location=coordenadas,
                radius=200, 
                type='bar',
                keyword='cerveja artesanal OR batata frita OR petiscos',
                max_price=2
            )
            
            for local in resposta.get('results', []):
                if local.get('rating', 0) >= 4.0:
                    nivel_preco = local.get('price_level', '?')
                    simbolo_preco = "$" * nivel_preco if isinstance(nivel_preco, int) else "?"
                    
                    # Evitar duplicatas caso a mesma busca encontre o bar
                    if not any(b['id'] == local['place_id'] for b in bares_aprovados):
                        bares_aprovados.append({
                            'id': local['place_id'],
                            'nome': local.get('name'),
                            'nota': local.get('rating', 0),
                            'aval': local.get('user_ratings_total', 0),
                            'lat': local['geometry']['location']['lat'],
                            'lng': local['geometry']['location']['lng'],
                            'endereco': local.get('vicinity'),
                            'preco': simbolo_preco,
                            'estacao_proxima': estacao
                        })
        except Exception as e:
            st.error(f"Erro ao buscar na estação {estacao}: {e}")
            
    # Ordenar pelos melhores bares no geral
    bares_aprovados.sort(key=lambda x: (x['nota'], x['aval']), reverse=True)
    return bares_aprovados

# --- LADO ESQUERDO: BARRA LATERAL (Filtros) ---
st.sidebar.header("🚇 Escolha as Estações")

# Caixa de Seleção Múltipla
estacoes_selecionadas = st.sidebar.multiselect(
    "Selecione de quais bairros quer ver as opções:",
    options=list(ESTACOES.keys()),
    default=["Nossa Senhora da Paz", "Uruguai"] # Começa com duas para testar
)

# Buscando dados reais!
lista_bares = buscar_bares_api(estacoes_selecionadas)

st.sidebar.markdown("---")
st.sidebar.header(f"🔍 Resultados ({len(lista_bares)})")

# Memória do bar selecionado na interface
if 'bar_selecionado' not in st.session_state or st.session_state.bar_selecionado not in lista_bares:
    st.session_state.bar_selecionado = lista_bares[0] if lista_bares else None

# Botões dos bares na lateral
for bar in lista_bares:
    rotulo = f"⭐ {bar['nota']} | {bar['nome']} (Perto de: {bar['estacao_proxima']})"
    if st.sidebar.button(rotulo, key=bar['id'], use_container_width=True):
        st.session_state.bar_selecionado = bar

bar_atual = st.session_state.bar_selecionado

# --- LADO DIREITO: MAPA E DETALHES ---
if not lista_bares:
    st.warning("👆 Selecione pelo menos uma estação na barra lateral para ver os resultados.")
else:
    col_mapa, col_detalhes = st.columns([2, 1])

    with col_mapa:
        st.subheader("🗺️ Mapa de Estabelecimentos")
        
        # Centraliza no bar selecionado
        m = folium.Map(location=[bar_atual['lat'], bar_atual['lng']], zoom_start=16)
        
        # Pinos no mapa
        for bar in lista_bares:
            cor = "red" if bar['id'] == bar_atual['id'] else "blue"
            icone = "star" if bar['id'] == bar_atual['id'] else "info-sign"
            
            folium.Marker(
                [bar['lat'], bar['lng']],
                popup=bar['nome'],
                tooltip=f"{bar['nome']} ({bar['estacao_proxima']})",
                icon=folium.Icon(color=cor, icon=icone)
            ).add_to(m)
        
        st_folium(m, width=800, height=500, key="mapa_principal")

    with col_detalhes:
        st.subheader("📌 Detalhes do Local")
        st.markdown(f"### **{bar_atual['nome']}**")
        st.write(f"**Nota:** ⭐ {bar_atual['nota']} ({bar_atual['aval']} avaliações)")
        st.write(f"**Preço:** {bar_atual['preco']}")
        st.write(f"**Endereço:** {bar_atual['endereco']}")
        st.write(f"**Estação mais próxima:** {bar_atual['estacao_proxima']}")
        
        link_maps = f"https://www.google.com/maps/search/?api=1&query={bar_atual['lat']},{bar_atual['lng']}&query_place_id={bar_atual['id']}"
        st.markdown(f"[➡️ Abrir no Google Maps]({link_maps})")