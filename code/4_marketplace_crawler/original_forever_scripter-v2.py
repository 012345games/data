import argparse
import subprocess
from tqdm import tqdm
import time
import logging
import psutil

TIMEOUT = 400 #seconds
total_urls = 313286


def chunkIt(seq, num):
    avg = len(seq) / int(num)
    out = []
    last = 0
    ranges=[]
    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg
    return out

if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument("--urllist", help="file with list of game urls, one per line", type=str, required=True)
    parser.add_argument("--headless", help="use headless chrome", action='store_true')
    parser.add_argument("--port", help="chrome debugging interface port", type=int)
    parser.add_argument("--total_instances", help="how many instances we want", type=int)
    parser.add_argument("--instance_no", help=" instance ID ", type=int)

    args = parser.parse_args()

    #set headless / port options
    cmd = "python3 tool/run_cli.py"
    if args.headless:
        cmd += " --headless"
    if args.port:
        cmd += (" --port " + str(args.port))

    #load urls
    urls = [line[0:-1] for line in open(args.urllist, 'r')]

    #set boundaries (if provided)
 
    instances = args.total_instances 
    instance_number = args.instance_no-1 
    lsst=chunkIt(range(total_urls),instances)
    instance_range=lsst[instance_number]
    start=instance_range[0]+1
    end=instance_range[-1]+1
	


    #keeps looking on same urls range
    while True:
        for i, url in enumerate(tqdm(urls[start:end])):
            print(cmd + " --url " + url)
            print("Range of urls is from : " +str(start)+ " to "+str(end))
            p = subprocess.Popen(cmd + " --url " + url, shell=True)
            try:
                p.wait(timeout=TIMEOUT)
            except subprocess.TimeoutExpired:
                for child in psutil.Process(p.pid).children(recursive=True):
                    child.kill()
                p.kill()
                logging.error('Chrome script has taken too long. Shutted down.')

        print("Countdown until restart: ")
        seconds_to_sleep = 30
        for _ in tqdm(list(range(seconds_to_sleep))):
            time.sleep(1)
