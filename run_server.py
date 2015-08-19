from repast import app
import sys

arglen = len(sys.argv)

if __name__ == '__main__':
    if arglen == 3:
        app.run(host=sys.argv[1], port=int(sys.argv[2]))
    else:
    	print("Error args number, need ip and port");
