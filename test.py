import sys
import glob
import base64
import os
from PIL import Image

def xor(data, key): 
    return bytearray(a^b for a, b in zip(*map(bytearray, [data, key]))) 

key = '''
561CWxbxgRlmQjxEZ41EuE5YHOnD2hxQR0zvUEq
LwMs/EbPkNHCgeqOuLFtLEcMBI36CWUwdw80B0h
wja+OftrIuYNenqf6eP7pYXWTxoIIUbFey/ZoSS
U04X9KQb/ybjcvFfrcMAVd9I05PvUiEA5RRaCn4
z0tLOkMYVgg94ow='''.encode("UTF-8")
key = base64.b64decode(key)

if not os.path.isdir(sys.argv[1]+"\\decoded"):
	os.mkdir(sys.argv[1]+"\\decoded")

for fname in glob.glob(sys.argv[1]+"\\*.webp"):
	fdir = os.path.dirname(fname)+"\\decoded";
	if fname[-9:] == '_dec.webp': continue
	if os.path.isfile(fdir+"\\"+os.path.basename(fname).split('.webp')[0] + '_dec.webp'): continue
	print(fname)
	fin = open(fname, 'rb')
	fout = open(fdir+"\\"+os.path.basename(fname).split('.webp')[0] + '_dec.webp', 'wb')
	fout.write(xor(fin.read(128), key))
	fout.write(fin.read())
	fout.close()
	im = Image.open(fdir+"\\"+os.path.basename(fname).split('.webp')[0] + '_dec.webp')
	im.info.pop('background', (255, 255, 255, 255))
	im.info.pop('optimize', None)
	im.save(fdir+"\\"+os.path.basename(fname).split('.webp')[0] + '_dec.gif', 'gif', save_all=True)