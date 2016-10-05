
# DBLPA

DBLPA is analysis tool which can help you find out the research trend in Recent conference, by utilize urllib2, matplotlib and data in DBLP.  


hadoop tread:  
![](https://raw.githubusercontent.com/septicmk/DBLP_Analysis/master/hadoop.png)

GPU tread:  
![](https://raw.githubusercontent.com/septicmk/DBLP_Analysis/master/GPU.png)

# Requirement

python 2.7+    
- matplotlib  
- urllib2

# Quick Start  

## Download  
you should get the DBLPA via git clone:  
```shell
git clone https://github.com/septicmk/DBLP_Analysis.git
```

## Config  
With a little config in the DBLPA, you can set the conferences that you are interested in and the search keywords used to filter out the target. Don't forget to set the year!  
```python
conf_lists = ['usenix', 'eurosys', 'osdi', 'sosp', 'ics', 'spaa', 'ppopp', 'ipps', 'sc']
years = [ '2010', '2011', '2012', '2013', '2014', '2015', '2016']
key_words_include = [ 'GPU' ]
```


## Run  
Fetch the infomation about your conferences.(this step may take a **looooooooong** time.)  
```python
python DBLPA.py -f
```

   
Query the keywords  
```python
python DBLPA.py -q

```
It will generate a graph like above and a file named `ans.json` contained the targets for you.  

