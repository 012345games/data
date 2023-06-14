## Automation tool for iogames

TODO: readme

TODO: populate list of remote game sources (e.g., html5.gamedristribution.com, html5.iclouds.io,)

TODO: itch sometimes block hotlink stealing, which makes it hard to separately execute the iframe, e.g. v6p9d9t4.ssl.hwcdn.net/html/1171829/ArcheryClub Trimmed/index.html?v=1574336303

*example: run tool on a single game url:*

```
python3 tool/run_cli.py --url www.crazygames.com/game/gangsters
```

*example: run tool in headless mode and select chrome debugging port*

```
python3 tool/run_cli.py --url www.crazygames.com/game/gangsters --port 9200 --headless
```

*example: run tool on a list of urls*

```
python3 tool/run_cli.py --urllist ./tool/games.txt
```
where *games.txt* has 1 url per line. 
