import sys
import requests

url = 'http://trivialcapstone.herokuapp.com/'

def dehaze(image,token):
    files = {'file': open(image, 'rb')}
    r = requests.post(url+token+'/transform', files=files)
    print "hello"
    return r.text,r

if __name__ == '__main__':
    if len(sys.argv)==3:
        print dehaze(image = sys.argv[1], token = sys.argv[2])
    else:
        print " Invalid Parameters"
        exit()
