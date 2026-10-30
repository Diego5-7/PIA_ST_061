import cv2

def main():
    opcion = input("Elige el tipo de cámara (0 para laptop, 1 para celular): ").strip()
    
    if opcion == "1":
        fuente = 1
        print("Cámara de celular seleccionada.")
    else:
        fuente = 0
        print("Cámara de la laptop seleccionada por defecto.")

    cap = cv2.VideoCapture(fuente)
    lector = cv2.QRCodeDetector()

    if not cap.isOpened():
        print("No se pudo abrir la cámara.")
        return

    print("Con la letra 'q' se cierra la ventana.\n")

    ultimo = ""
    preambulo = "UUUU|"

    while True:
        ret, frame = cap.read()
        if not ret:
            print("No se pudo leer el video de la cámara.")
            break

        data, bbox, _ = lector.detectAndDecode(frame)

        if data and data != ultimo:
            print(f"Mensaje: {data}")

            if data.startswith(preambulo):
                print("Preámbulo 'UUUU|' sincronizado correctamente.")

                cuerpo_bits = data[len(preambulo):]
                
                trama_bits_recuperados = ""
                errores_corregidos = 0
                for i in range(0, len(cuerpo_bits) - 6, 7):
                    bloque = cuerpo_bits[i:i+7]
                    if len(bloque) < 7:
                        break
                    
                    p1 = int(bloque[0])
                    p2 = int(bloque[1])
                    d3 = int(bloque[2])
                    p4 = int(bloque[3])
                    d5 = int(bloque[4])
                    d6 = int(bloque[5])
                    d7 = int(bloque[6])
                    
                    s1 = p1 ^ d3 ^ d5 ^ d7
                    s2 = p2 ^ d3 ^ d6 ^ d7
                    s4 = p4 ^ d5 ^ d6 ^ d7
                    
                    syndrome = s4 * 4 + s2 * 2 + s1 * 1
                    
                    bits_lista = [p1, p2, d3, p4, d5, d6, d7]
                    if syndrome != 0:
                        errores_corregidos += 1
                        idx = syndrome - 1
                        if 0 <= idx < 7:
                            bits_lista[idx] = 1 - bits_lista[idx]
                    
                    p1, p2, d3, p4, d5, d6, d7 = bits_lista
                    trama_bits_recuperados += f"{d3}{d5}{d6}{d7}"

                print(f"Bloques con errores corregidos: {errores_corregidos}")
                bytes_recuperados = bytearray()
                for i in range(0, len(trama_bits_recuperados) - 7, 8):
                    byte_str = trama_bits_recuperados[i:i+8]
                    if len(byte_str) == 8:
                        bytes_recuperados.append(int(byte_str, 2))

                clave_otp = b'3' * len(bytes_recuperados)
                mensaje_descifrado = bytes(a ^ b for a, b in zip(bytes_recuperados, clave_otp))
                
                try:
                    mensaje_reconstruido = mensaje_descifrado.decode('utf-8')
                    print(f"Mensaje final decodificado: {mensaje_reconstruido}\n")
                except Exception as e:
                    print(f"Error al decodificar texto: {e}\n")
            else:
                print("Error de sincronización: Preámbulo no reconocido.")
               
            ultimo = data

        cv2.imshow("Receptor H4", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
