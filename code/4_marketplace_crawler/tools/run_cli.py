import pandas as pd
import time
import subprocess
import time
import argparse
import logging
import os

#local modules
import utils
import exp_interface


def process_url(url, chrome):
    url = utils.sanitize_url(url)
    #get game name
    game = url.split('/')[-1]
    #get marketplace name
    marketplace = url.split('/')[0]
    if "miniclip" in marketplace:
    	#handle weird miniclip game naming
    	game = url.split('games/')[1].split('/en')[0]
    if "friv" in marketplace:
    	#handle weird friv game naming
    	game = url.split('games/')[1].split('/game')[0]
    logging.info("url=%s, marketplace=%s, game=%s" % (url, marketplace, game))
    #annotate marketplace in "game"
    if "itch" in marketplace:
        game = game + '_itch'
    else:
        game = game + '_' + marketplace.replace('www.',"").split('.')[0]
    #launch experiment
    exp_interface.launch(url, marketplace, game, chrome)#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< calls exp_interface.launch


if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="game url", type=str)
    parser.add_argument("--urllist", help="file with list of game urls, one per line", type=str)
    parser.add_argument("--port", help="chrome debugging interface port", type=int)
    parser.add_argument("--headless", help="use headless chrome", action='store_true')

    args = parser.parse_args()

    #chrome listening at port
    if args.port:
        port = args.port
    else:
        port = 9222 #default
    chrome = ['google-chrome',
              '--remote-debugging-port='+str(port),
              '--allow-insecure-content',
              '--start-fullscreen',
              '--incognito']
    if args.headless:
        chrome.append('--headless')
    print(chrome)

    if not args.url and not args.urllist:
        logging.error("Not enough arguments")

    if args.url and args.urllist:
        logging.error("Either one url, or a list of urls")

    if args.url and not args.urllist:
        logging.info("Starting data collection for url %s" % args.url)
        process_url(args.url, chrome)

    if not args.url and args.urllist:
        logging.info("Starting data collection on urls from file %s" % args.urllist)
        if not os.path.exists(args.urllist):
            logging.error('File does not exists')
        else:
            for line in open(args.urllist):
                process_url(line[0:-1], chrome) #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< processes the urllist
