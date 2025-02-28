import requests    #Se utiliza Requests para el get de la PokeApi
import pandas as pd 

# se define la constante 
BASEURL = "https://pokeapi.co/api/v2/"

#se crea una lista para guardar los datos

pokedatos = []

#se obtiene la información de los 50 pokemon solicitados 
#se crea una función para hacer consultas get 

def get_request(url, full_url = False):
    if full_url: 
        response = requests.get(url)
    else: 
        response = requests.get(BASEURL + url)
    if response.status_code == 200:
        data = response.json()
        return data
    return {"status": "400", "message": "the information is not available."}


def get_pokemon_details(pokelist):
    poke_details= []
    for pokemon in pokelist:
        details = get_request(pokemon["url"], True)
        tipos = [t['type']['name'] for t in details['types']]
        
        poke_details.append({
            'ID': details['id'],
            'Nombre': details['name'],
            'Tipo(s)': ', '.join(tipos),
            'Altura': details['height'], 
            'Peso': details['weight'],
            'Nombre Invertido': details['name'][::-1]

        })
    return pd.DataFrame(poke_details)

limit_url = "pokemon?limit=50"
pokedatos = get_request(limit_url)
print (pokedatos)


df_pokemones = get_pokemon_details(pokedatos["results"])
print(df_pokemones)

#se extraen los datos solicitados (ID, nombre, tipo(s), altura y peso)

# peso más de 30 y menos de 80
df_peso = df_pokemones[(df_pokemones['Peso'] > 30) & (df_pokemones['Peso'] < 80)]
print (df_peso)

# tipo grass
df_grass = df_pokemones[df_pokemones['Tipo(s)'].str.contains('grass', case=False)]
print (df_grass)

# tipo flying, mide más de 10
df_flying = df_pokemones[(df_pokemones['Tipo(s)'].str.contains('flying', case=False)) & (df_pokemones['Altura'] > 10)]
print (df_flying)

# se exportan los datos en archivos CSV para PowerBi

df_pokemones.to_csv('pokedatos.csv', index=False)
df_peso.to_csv('pokepeso.csv', index=False)
df_flying.to_csv('pokealtura.csv', index=False)
df_grass.to_csv('pokegrass.csv', index=False)


