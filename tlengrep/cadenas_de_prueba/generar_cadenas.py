import random

print("cantidad de cadenas")
cantidad = int(input(">"))
print("longitud de cadenas")
longitud = int(input(">"))

contenido = []
for _ in range(cantidad):
    cadena = ""
    for _ in range(longitud):
        if random.random() > 0.5:
            simbolo = 'a'
        else:
            simbolo = 'b'
        cadena += simbolo
    contenido.append(cadena)

nombre = str(cantidad) + "de" + str(longitud) + ".txt"
with open(nombre, "w") as file:
    file.write('\n'.join(contenido))

print("Creado en ./" + nombre)

