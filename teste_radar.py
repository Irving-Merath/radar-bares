import googlemaps
import json

# Substitua pela chave que está no seu bloco de notas
API_KEY = "AIzaSyDCJ438Qsie21zjw_jcf39fr7ckvhmc4lE" 

print("📡 Ligando o radar do Google Maps...")
gmaps = googlemaps.Client(key=API_KEY)

# Coordenadas de teste ao redor da Praça Saens Peña, na Tijuca
local_teste = "-22.9242,-43.2325"

try:
    # Lançando o radar: buscando bares num raio de 500m
    resposta = gmaps.places_nearby(
        location=local_teste,
        radius=500,
        type='bar'
    )
    
    bares_encontrados = resposta.get('results', [])
    
    print(f"✅ Sucesso! O radar detectou {len(bares_encontrados)} estabelecimentos na região.")
    
    if bares_encontrados:
        print("\n🔍 Espiando os dados do primeiro bar da lista:")
        # Mostrando as informações cruas (JSON) para entendermos o que o Google entrega
        print(json.dumps(bares_encontrados[0], indent=2, ensure_ascii=False))
        
except Exception as e:
    print(f"❌ Ops! O radar falhou. Verifique a chave e a internet. Erro: {e}")