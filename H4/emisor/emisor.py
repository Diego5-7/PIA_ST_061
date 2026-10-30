import qrcode

mensaje_inicial = "Somos el equipo 3 y este es nuestro mensaje"

print(f"Mensaje: {mensaje_inicial}")
print(f"Longitud: {len(mensaje_inicial)} caracteres")

mensaje_bytes = mensaje_inicial.encode('utf-8')

clave_otp = b'3' * len(mensaje_bytes)

mensaje_cifrado = bytes(a ^ b for a, b in zip(mensaje_bytes, clave_otp))

preambulo = "UUUU|"
trama_completa = preambulo + forma_ascii

print(f"Trama con preámbulo: {trama_completa}")

img = qrcode.make(trama_completa)
img.save("codigo_qr_h3.png")
img.show()
