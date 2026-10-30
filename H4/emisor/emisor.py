import qrcode

mensaje_inicial = "Somos el equipo 3 y este es nuestro mensaje"

print(f"Mensaje: {mensaje_inicial}")
print(f"Longitud: {len(mensaje_inicial)} caracteres")

mensaje_bytes = mensaje_inicial.encode('utf-8')

clave_otp = b'3' * len(mensaje_bytes)

mensaje_cifrado = bytes(a ^ b for a, b in zip(mensaje_bytes, clave_otp))

trama_datos = ""
for byte in mensaje_cifrado:
    trama_datos += f"{byte:08b}"

while len(trama_datos) % 4 != 0:
    trama_datos += '0'

trama_hamming = ""
for i in range(0, len(trama_datos), 4):
    d3 = int(trama_datos[i])    
    d5 = int(trama_datos[i+1])  
    d6 = int(trama_datos[i+2])  
    d7 = int(trama_datos[i+3])  
    
    p1 = d3 ^ d5 ^ d7        
    p2 = d3 ^ d6 ^ d7        
    p4 = d5 ^ d6 ^ d7        
    
    bloque_7 = f"{p1}{p2}{d3}{p4}{d5}{d6}{d7}"
    trama_hamming += bloque_7
preambulo = "UUUU|"
trama_completa = preambulo + trama_hamming

print(f"Trama con preámbulo: {trama_completa}")

img = qrcode.make(trama_completa)
img.save("codigo_qr_h3.png")
img.show()
