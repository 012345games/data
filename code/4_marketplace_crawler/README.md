## This folder contains script for running games from different marketplaces.
## Iogames data collection

### Forever scripter usage:


*Data collection, game urls from all_gamelinks.txt (1 per line)*

```
python3 forever_scripter.py --urllist all_gamelinks.txt
```

*Read urls from all_gamelinks.txt with ranges [NLOW, NHIGH]*

```
python3 forever_scripter.py --urllist all_gamelinks.txt --nlow NLOW --nhigh NHIGH
```

*Set chrome port=PORT_NUMBER*

```
python3 forever_scripter.py --urllist all_gamelinks.txt --port PORT_NUMBER
```

*Set chrome headless (no chrome window)*

```
python3 forever_scripter.py --urllist all_gamelinks.txt --headless
```

**Suggested for parallel executions** (each with different NLOW, NHIGH, PORT_NUMBER)

```
python3 forever_scripter.py --urllist all_gamelinks.txt --nlow NLOW --nhigh NHIGH --headless --port PORT_NUMBER
```
*** forever_scripter2.py *** 
```
python3 forever_scripter-v2.py --urllist all_gamelinks.txt --headless --port 9222 [must change for every instances] --instance_id [1-20]
Note : creates single instance. Maximum 20 instances can be created.
```

### Requirements

- Node js (tested on v14.15.4)
- The following python packages:  **tqdm**, **psutil**, **pandas**.



### More about the node js application [here](https://github.com/gtngari/iogames/tree/master/static_analysis/old_js/README.md)


### Utils

*Get iframe detection rate (global and per marketplace)*

```
python3 utils/iframe_ratio.py ./PATH_DOM/
```

*Zip all game folders (to save space)*

```
for folder in ./PATH_DYNAMIC_SCRIPT/*; do echo $folder; zip -r $folder.zip $folder; done
for folder in ./PATH_STATIC_SCRIPT/*; do echo $folder; zip -r $folder.zip $folder; done
for folder in ./PATH_TRACING/*; do echo $folder; zip -r $folder.zip $folder; done
for folder in ./PATH_SCREENSHOT/*; do echo $folder; zip -r $folder.zip $folder; done
```

### extract_sld.py (reads all the files from PATH_DOM and makes a list of extracted slds and a txt file of urls in incorrect formet)
```
python3 extract_sld.py --path "/home/hinaqayyum/Downloads/new/PATH_DOM/*.flatteneddom"
*note: path has to be for reading a speicific type of file extension (.flatteneddom in this case)
```
