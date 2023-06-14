import logging
import marketplaces
import os

def check_and_proceed(game):
    #check if results already exist
    if os.path.exists("./PATH_DOM/"+game+'.flatteneddom') and \
    os.path.exists("./PATH_TRACING/"+game) and \
    os.path.exists("./PATH_STATIC_SCRIPT/"+game) and \
    os.path.exists("./PATH_DYNAMIC_SCRIPT/"+game) and \
    os.path.exists("./PATH_SCREENSHOT/"+game):
        logging.warning("Already executed (files exist). Exiting")
        return False #already executed
    elif os.path.exists("./PATH_DOM/"+game+'.flatteneddom') or \
    os.path.exists("./PATH_TRACING/"+game) or \
    os.path.exists("./PATH_STATIC_SCRIPT/"+game) or \
    os.path.exists("./PATH_DYNAMIC_SCRIPT/"+game) or \
    os.path.exists("./PATH_SCREENSHOT/"+game):
        #clean
        logging.warning("Removing previous files and starting experiment...")
        os.system("rm ./PATH_DOM/"+game+'*')
        os.system("rm ./PATH_COOKIES/"+game+'*')
        os.system("rm ./PATH_PROFILER/"+game+'*')
        os.system("rm -r ./PATH_STATIC_SCRIPT/"+game+'*')
        os.system("rm -r ./PATH_DYNAMIC_SCRIPT/"+game+'*')
        os.system("rm -r ./PATH_TRACING/"+game+'*')
        os.system("rm -r ./PATH_SCREENSHOT/"+game+'*')
        return True
    else:
        return True

def checkurl_and_proceed(url):
    processed_urls = [line[0:-1] for line in open("processed_urls.log")]
    if url in processed_urls:
        logging.warning("Already executed (in processed_urls.log). Exiting")
        return False
    else:
        return True


def launch(url, marketplace, game, chrome):
    #TODO chech if experiment folder already exists
    if check_and_proceed(game) == False:
        return
    if checkurl_and_proceed(url) == False:
        return
    #select codebase for the experiment
    if "poki" in marketplace:
        #case: Poki.com
        marketplaces.poki.execute(url, game, chrome)
    elif "y8" in marketplace:
        #case: Y8.com
        marketplaces.y8.execute(url, game, chrome)
    elif "crazygames" in marketplace:
        #case: Crazygames.com
        marketplaces.crazygames.execute(url, game, chrome)
    elif "friv" in marketplace:
        #case: Friv.com
        marketplaces.friv.execute(url, game, chrome)
    elif "miniclip" in marketplace:
        #case: Miniclip.com
        marketplaces.miniclip.execute(url, game, chrome)
    elif "ufreegames" in marketplace:
        #case: Ufreegames.com
        marketplaces.ufreegames.execute(url, game, chrome)
    elif "coolmathgames" in marketplace:
        #case: Coolmathgames.com
        marketplaces.coolmathgames.execute(url, game, chrome)
    elif "itch" in marketplace:
        #case: Itch.com
        marketplaces.itch.execute(url, game, chrome)
    elif "iogame.app" in marketplace:
        #case: Iogame.app
        marketplaces.iogameapp.execute(url, game, chrome)
    elif "addictinggames" in marketplace:
        #case: Addictinggames.com
        marketplaces.addictinggames.execute(url, game, chrome)
    elif "vseigru" in marketplace:
        #case: Vseigru.net
        marketplaces.vseigru.execute(url, game, chrome)
    elif "gameflare" in marketplace:
        #case: Gameflare.com
        marketplaces.gameflare.execute(url, game, chrome)
    elif "mousebreaker" in marketplace:
        #case: MouseBreaker.com
        marketplaces.mousebreaker.execute(url, game, chrome)
    elif "webgameapp" in marketplace:
        #case: Webgameapp.com
        marketplaces.webgameapp.execute(url, game, chrome)
    elif "yourgames" in marketplace:
        #case: Yourgames.io
        marketplaces.yourgamesio.execute(url, game, chrome)
    elif "yupi" in marketplace:
        #case: Yupi.com
        marketplaces.yupi.execute(url, game, chrome)
    elif "fukgames" in marketplace:
        #case: Fukgames.com
        marketplaces.fukgames.execute(url, game, chrome)
    elif "bestgames" in marketplace:
        #case: Bestgames.com
        marketplaces.bestgames.execute(url, game, chrome)
    elif "yad" in marketplace:
        #case: Yad.com
        marketplaces.yad.execute(url, game, chrome)
    elif "babygames" in marketplace:
        #case: Babygames.com
        marketplaces.babygames.execute(url, game, chrome)
    else:
        #default case: game homepage only
        marketplaces.generic_mp.execute(url, game, chrome)

    #add to processed_urls.log
    with open("processed_urls.log", 'a') as fout:
        fout.write(url+'\n') 
