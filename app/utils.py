from math import radians, sin, cos, sqrt, atan2
from django.db.models import F

def haversine(lat1, lon1, lat2, lon2):
    # """
    # Calcula a distância haversine entre dois pontos geográficos.

    # :param lat1: Latitude do ponto 1 em graus.
    # :param lon1: Longitude do ponto 1 em graus.
    # :param lat2: Latitude do ponto 2 em graus.
    # :param lon2: Longitude do ponto 2 em graus.
    # :return: Distância entre os dois pontos em quilômetros.
    # """
    # Raio médio da Terra em quilômetros
    R = 6371.0

    # if isinstance(lat1, F):
    #     lat1 = lat1.resolve_expression(None)
    # if isinstance(lon1, F):
    #     lon1 = lon1.resolve_expression(None)
    # if isinstance(lat2, F):
    #     lat2 = lat2.resolve_expression(None)
    # if isinstance(lon2, F):
    #     lon2 = lon2.resolve_expression(None)

    print(lat2, lon2)

    # Converte as coordenadas de graus para radianos
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Diferenças de coordenadas
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Fórmula de Haversine
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Distância em quilômetros
    distance = R * c

    return distance


# print(haversine(50,50,50.1,50.1))