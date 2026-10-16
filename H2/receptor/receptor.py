import cv2

def main():

    fuente = 0

    cap = cv2.VideoCapture(fuente)
    
    lector = cv2.QRCodeDetector()

    if not cap.isOpened():
        print("No se pudo abrir la cámara de la computadora.")
        return

    print("Con la letra 'q' se cierra la ventana.\n")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("No se pudo leer el video de la cámara.")
            break

        data, bbox, _ = lector.detectAndDecode(frame)

        if data:
            print(f"Mensaje: {data}")

        cv2.imshow("Receptor del QR", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
