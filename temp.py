import pyqrcode
import qrtools
qr = pyqrcode.create("HORN O.K. PLEASE.")
qr.png("horn.png", scale=6)


qr = qrtools.QR()
qr.tobytes("horn.png")
print qr.data
