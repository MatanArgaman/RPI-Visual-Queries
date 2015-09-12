#Use google OCR called Tesseract to get the text written in the image

#imgPath - a file path of the image
def readImage(imgPath):
	try:
		import Image
	except ImportError:
		from PIL import Image
	import pytesseract
	return pytesseract.image_to_string(Image.open(imgPath))

