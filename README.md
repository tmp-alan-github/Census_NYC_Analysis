#                                                         Census_NYC_Analysis
### Using government provided data to analyze certain metrics and stats concerning incidents reported in NYC.


#### [TODO/Improvements](https://github.com/tmp-alan-github/Census_NYC_Analysis/blob/master/todo.md)

### Installation Tips
The script is developed in python3, mostly tested in an EC2 Instance.

Dependencies include: pandas, numpy, glob and fuzzywuzzy. 

Automatically downloads JSONs if not detected already in data folder, through the use of SODA url queries.

Cloning the git and running the script:
```
git clone https://github.com/tmp-alan-github/Census_NYC_Analysis.git
python3 Census_NYC_Analysis/main.py
```
##### Possible options
```
1. Aggregate incidents per zip code
2. Aggregate incidents per boroughs
3. Analyze incidents per 10k capita by zip
4. Analyze incidents per 10k capita by Borough
5. (DEV) - String Similarity Comparison FuzzyWuzzy
```

<div align='center'>

### Individual zip codes can be observed inflating as parsed info maneuvers and increments
![](https://i.imgur.com/tXDhuLV.gif)


</div>
