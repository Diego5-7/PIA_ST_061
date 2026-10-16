import qrcode

mensaje = "1"
img = qrcode.make(mensaje)
img.save("codigo_qr.png")
img.show()
