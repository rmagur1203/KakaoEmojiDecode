import sys
import glob
import base64
import os
import subprocess
from PIL import Image
from shutil import copyfile

def xor(data, key): 
    return bytearray(a^b for a, b in zip(*map(bytearray, [data, key])))

import requests
import urllib.request
from bs4 import BeautifulSoup

def webp2gif(fin):
    files = { 'new-image': fin }
    res = requests.post('https://s3.ezgif.com/webp-to-gif', files=files, data={'new-image-url': ''})
    print(res.url)
    soup = BeautifulSoup(res.text, 'html.parser')
    token = soup.select('input[name="token"]')[0]["value"]
    file = soup.select('input[name="file"]')[0]["value"]
    data = {'file': file, 'token': token}
    res = requests.post(res.url+'?ajax=true', data=data)
    soup = BeautifulSoup(res.text, 'html.parser')
    img = soup.select('img')[0]["src"]
    return 'https:' + img
def download_webp2gif(inputPath, outputPath):
    fin = open(inputPath, 'rb')
    url = webp2gif(fin)
    urllib.request.urlretrieve(url, outputPath)

key = '''
561CWxbxgRlmQjxEZ41EuE5YHOnD2hxQR0zvUEq
LwMs/EbPkNHCgeqOuLFtLEcMBI36CWUwdw80B0h
wja+OftrIuYNenqf6eP7pYXWTxoIIUbFey/ZoSS
U04X9KQb/ybjcvFfrcMAVd9I05PvUiEA5RRaCn4
z0tLOkMYVgg94ow='''.encode("UTF-8")
key = base64.b64decode(key)

path = ""

if len(sys.argv) < 2:
	path = os.getenv('LOCALAPPDATA')+"\\Kakao\\KakaoTalk\\users"
else:
	path = sys.argv[1]

#if not os.path.isdir(path+"\\decoded"):
#	os.mkdir(path+"\\decoded")

def decodeFiles(path):
	fdir = path+"_decoded"
	if not os.path.isdir(fdir):
		os.mkdir(fdir)
	for fname in glob.glob(path+"\\*"):
		if fname.endswith(".webp"):
			if fname[-9:] == '_dec.webp': continue
			if os.path.isfile(fdir+"\\"+os.path.basename(fname).split('.webp')[0] + '_dec.webp'): continue
			print(fname)
			fin = open(fname, 'rb')
			print(fdir+"\\"+os.path.basename(fname).split('.webp')[0] + '_dec.webp')
			fout = open(fdir+"\\"+os.path.basename(fname).split('.webp')[0] + '_dec.webp', 'wb')
			fout.write(xor(fin.read(128), key))
			fout.write(fin.read())
			fout.close()
			download_webp2gif(fdir+"\\"+os.path.basename(fname).split('.webp')[0] + '_dec.webp', fdir+"\\"+os.path.basename(fname).split('.webp')[0] + '_dec.gif')
			#im = Image.open(fdir+"\\"+os.path.basename(fname).split('.webp')[0] + '_dec.webp')
			#im.info.pop('background', (255, 255, 255, 255))
			#im.info.pop('optimize', None)
			#im.save(fdir+"\\"+os.path.basename(fname).split('.webp')[0] + '_dec.gif', 'gif', save_all=True)
		else:
			base = os.path.basename(fname)
			if not os.path.exists(fdir):
				os.makedirs(fdir)
			copyfile(fname, fdir+"\\"+os.path.splitext(base)[0]+'_dec'+os.path.splitext(base)[1])


for fd in glob.glob(path+"\\*"):
	if os.path.isdir(fd):
		#subprocess.Popen(r'explorer "'+fd+'\\DigitalItem\\c"')
		for emgs in glob.glob(fd + "\\DigitalItem\\c\\*"):
			if os.path.isdir(emgs):
				if not emgs.endswith("_decoded"):
					decodeFiles(emgs)
		decodeFiles(fd + "\\DigitalItem\\e")
		subprocess.Popen(r'explorer "'+fd+'\\DigitalItem"')