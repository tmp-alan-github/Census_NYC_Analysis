#                                                         Census_NYC_Analysis
### Using government provided data, namely a bulky csv, to analyze certain metrics and stats concerning incidents reported in NYC.


#### [TODO/Improvements](https://github.com/tmp-alan-github/Census_NYC_Analysis/blob/master/todo.md)

### Installation Tips
The script is developed in python3, mostly tested in an EC2 Instance.

Make sure dependancies like pandas and numpy are installed.

Use tmux/screen to allow for the script to behave in the background, especially considering the 10Gb file that it awaits.

Some steps and method to get the CSV that is being parsed through:
```
cd ~
git clone https://github.com/tmp-alan-github/Census_NYC_Analysis.git
mkdir data
cd data
wget https://data.cityofnewyork.us/api/views/erm2-nwe9/rows.csv
cd ..
python3 main.py
```
##### Possible options
```
1. Aggregate incidents per zip code
2. Aggregate incidents per boroughs
3. Analyze incidents per 10k capita by zip
4. Analyze incidents per 10k capita or by Borough
```

<div align='center'>


###  Early parsing shown


![](https://i.imgur.com/VBmmhMB.gif)

### Individual zip codes can be observed inflating as parsed info maneuvers and increments
![](https://i.imgur.com/tXDhuLV.gif)


</div>
