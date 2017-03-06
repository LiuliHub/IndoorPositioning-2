
def format(im):
	return im[0]

def get_w(im):
	if len(im[1]) > 0:
		return len(im[1][0])
	else:
		return 0

def get_h(im):
	return len(im[1])
	
def white_rgb(w, h):
	fila = [(255, 255, 255) for i in range(w)]
	img = [fila for i in range(h)]
	return ("RGB", img)

def white_grey(w, h):
	fila = [255 for i in range(w)]
	img = [fila for i in range(h)]
	return ("L", img)

def white_bn(w, h):
	fila = [255 for i in range(w)]
	img = [fila for i in range(h)]
	return ("1", img)
	
def matrix(img):
	return img[1]
	
def subimg(img, ow, oh, w, h):
	imatge=img[1]
	imatge=imatge[oh:h+1][ow:w+1]
	return imatge

def img(m, model='DISCOVER'):
	if isinstance(m[0][0], tuple): 	# RGB
			return ("RGB", m)
	for a in m: 					#NO RGB
		for b in a:
			if b != 255 and b != 0: 
				return ("L", m)
			else:
				return ("1", m)

