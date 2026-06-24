import googlemaps

# 🔑 Cole sua chave aqui
API_KEY = "AIzaSyDCJ438Qsie21zjw_jcf39fr7ckvhmc4lE" 
gmaps = googlemaps.Client(key=API_KEY)

# Estações seguras
estacoes_seguras = {
    "Nossa Senhora da Paz (Ipanema)": "-22.9837,-43.2066",
    "Largo do Machado (Catete/Laranjeiras)": "-22.9311,-43.1774",
    "Uruguai (Tijuca)": "-22.9333,-43.2384"
}

estacao_escolhida = "Nossa Senhora da Paz (Ipanema)"
coordenadas_estacao = estacoes_seguras[estacao_escolhida]

print(f"🚇 Vasculhando os arredores da Estação {estacao_escolhida}...")

# 🍺 Novos Filtros: Foco em Bares, Cerveja Artesanal e Preço Acessível (Nível 1 e 2)
resposta = gmaps.places_nearby(
    location=coordenadas_estacao,
    radius=200, 
    type='bar', # Trocamos 'restaurant' por 'bar'
    keyword='cerveja artesanal OR batata frita OR petiscos',
    max_price=2 # Filtro de preço médio/barato
)

locais_encontrados = resposta.get('results', [])
locais_aprovados = []

for local in locais_encontrados:
    nome = local.get('name')
    nota = local.get('rating', 0)
    avaliacoes = local.get('user_ratings_total', 0)
    endereco = local.get('vicinity')
    nivel_preco = local.get('price_level', 'Não informado')
    
    # Adicionando um visualizador de cifrões para o preço
    if isinstance(nivel_preco, int):
        simbolo_preco = "$" * nivel_preco
    else:
        simbolo_preco = "?"
    
    if nota >= 4.0:
        locais_aprovados.append({
            'nome': nome,
            'nota': nota,
            'avaliacoes': avaliacoes,
            'endereco': endereco,
            'preco': simbolo_preco
        })

locais_aprovados.sort(key=lambda x: (x['nota'], x['avaliacoes']), reverse=True)

print(f"\n✅ Encontramos {len(locais_aprovados)} bares bacanas a menos de 200m do metrô!\n")

for lugar in locais_aprovados:
    print(f"⭐ {lugar['nota']} ({lugar['avaliacoes']} aval.) | Preço: {lugar['preco']} - {lugar['nome']}")
    print(f"   📍 {lugar['endereco']}\n")