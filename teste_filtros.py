import googlemaps

# 🔑 Cole sua chave aqui
API_KEY = "AIzaSyDCJ438Qsie21zjw_jcf39fr7ckvhmc4lE" 
gmaps = googlemaps.Client(key=API_KEY)

# Coordenadas da nossa base de testes
local_teste = "-22.9242,-43.2325"

print("🔎 Buscando locais bem avaliados com opções inclusivas no cardápio...")

# Lançando o radar com novos filtros (keyword)
resposta = gmaps.places_nearby(
    location=local_teste,
    radius=800, # Aumentei um pouco o raio de busca
    type='restaurant', # Usando restaurant para pegar bares que servem comida
    keyword='vegano OR vegetariano OR porções'
)

locais_encontrados = resposta.get('results', [])
locais_aprovados = []

# O Pente Fino: Passando por cada local encontrado
for local in locais_encontrados:
    nome = local.get('name')
    nota = local.get('rating', 0)
    avaliacoes = local.get('user_ratings_total', 0)
    
    # 🛑 Regra 3: Apenas estabelecimentos com nota maior que 4.0
    if nota > 4.0:
        locais_aprovados.append({
            'nome': nome,
            'nota': nota,
            'avaliacoes': avaliacoes
        })

# 🏆 Regra de Ouro: Ordenar a lista
# O Python vai ordenar primeiro pela nota (do maior pro menor) 
# e, em caso de empate, pelo número de avaliações.
locais_aprovados.sort(key=lambda x: (x['nota'], x['avaliacoes']), reverse=True)

print(f"\n✅ Passaram no pente fino: {len(locais_aprovados)} estabelecimentos!\n")

print("📋 Ranking dos Melhores:")
for lugar in locais_aprovados:
    print(f"⭐ {lugar['nota']} ({lugar['avaliacoes']} avaliações) - {lugar['nome']}")