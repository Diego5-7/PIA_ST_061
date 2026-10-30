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
    preambulo_esperado = "UUUU|"

    while True:
        ret, frame = cap.read()
        if not ret:
            print("No se pudo leer el video de la cámara.")
            break

        data, bbox, _ = lector.detectAndDecode(frame)

        if data and data != ultimo:
            print(f"Mensaje: {data}")

            if data.startswith(preambulo_esperado):
                print("Preámbulo 'UUUU|' sincronizado correctamente.")
                
                cuerpo_ascii = data[len(preambulo_esperado):]
                
                try:
                    mensaje_reconstruido = "".join(chr(int(codigo)) for codigo in cuerpo_ascii.split())
                    print(f"Mensaje decodificado: {mensaje_reconstruido}")
                except Exception as e:
                    print(f"Error al decodificar los caracteres ASCII: {e}")
            else:
                print("Error de sincronización: Preámbulo no reconocido.")

            ultimo = data

        cv2.imshow("Receptor OWC - FCFM (H3)", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
