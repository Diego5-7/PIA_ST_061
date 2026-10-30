import qrcode

mensaje_inicial = "Somos el equipo 3 y este es nuestro mensaje"

print(f"Mensaje: {mensaje_inicial}")
print(f"Longitud: {len(mensaje_inicial)} caracteres")

preambulo = "UUUU|"

forma_ascii = " ".join(str(ord(c)) for c in mensaje_inicial)

trama_completa = preambulo + forma_ascii

print(f"Trama con preámbulo: {trama_completa}")

img = qrcode.make(trama_completa)
img.save("codigo_qr_h3.png")
img.show()
