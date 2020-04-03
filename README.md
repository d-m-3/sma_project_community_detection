# Social Media Analytics - Project 6 – Community Detection in a Youtube Network

## Install
```bash
git clone https://github.com/d-m-3/sma_project_community_detection
cd sma_project_community_detection
pip install -r requirements.txt
```

## Use

To test the project, run the following bash commands

### Betweenness Centrality
```bash
python betweenness_centrality_usecase.py
python betweenness_centrality_tests.py
python betweenness_centrality_benchmark.py
```

### Girvan-Newman
```bash
python girvan_newman_usecase.py
python girvan_newman_tests.py
python girvan_newman_benchmark.py
```

## External usage

You can import the library in your own modules.

```python
from girvan_newman import girvan_newman
import betweenness_centrality import betweenness_centrality
```
