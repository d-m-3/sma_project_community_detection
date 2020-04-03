# sma_project_community_detection
Social Media Analytics – Project 6 – Community Detection in a Youtube Network


## Girvan Newman

### Implementation of Girvan-Newman

The implementation is in two parts :

\itemize{begin}
    \item Edge-betweenness-centrality mesure
    \item Girvan-Newman algorithm
\itemize{end}

The Girvan-Newman implementation is straightforward : when it's still possible to remove edges it computes the edge betweenness centrality of the graph, removes the edge with the highest value and look for connected components, if a new component is create by removing the last edge, it yields a new level of iteration : the connected components (also called communities).

For the edge-betweenness-centrality mesure first we calculate a dictionary for every possible combinations of endpoints the number of shortest paths and the number of shortest path through each edges. Then for every edges we compute the edge betweenness according to the formula given in the course with the previous dictionary.

We didn't implement everything ourselves, for example we used for the shortest path networkx method and the connected component function.

The implementation can be found in the file girvan_newman.py

### Analysis of the results and findings

Since our algorithm isn't efficient, we choose to reduce the size of our graph.

We created a simple use case of the algorithm load the subgraph in the file : girvan_newman_usecase.py

Here are the result of our subgraph :

**gn-uc-2.png**
**gn-uc-4.png**
**gn-uc-6.png**

As we can see at any level of iteration the graph is spited into two distinct communities joined by a hub.

One of the community at level 2, only has a few edges connected to a central node, this is maybe due to the fact that we sliced our graph.

Since the graph is anonymous we can't draw more conclusions without having to guess what this structure means.

### Evaluation of the performance of the implementation and its correctness

We created a benchmark file to compare the performance of our algorithm with networkx implementation. Has we can see with the next plots, our algorithm is way slower then the networkx implementation, especially on the edge_betweenness_centrality where our curve seems to grow exponentially.

Since the edge-betweeness-centrality algorithm is called multiples time in an iteration of Girvan-Newman, we can clearly expect Girvan-Newman to be slow down by the inefficiency of our edge-betweeness-centrality implementation.

**benchmark_edge_betweenness_centrality.png**
**benchmark_girvan_newman.png**
**benchmark_girvan_newman_cumulative.png**

Regarding the correctness of the implementation we seems to have the same results has networkx. We wrote a few unite test to verify that our computations are the same as networkx, this can be found in the file girvan_newman_tests.py. With this strategy we can't ensure that our implementation is correct, but since networkx seems to be a old and opensource library it's should have correct result and so our algorithm.

Notice that in the test file we only tested our algorithm on social graph, since they are not symmetric but have less chance that our edge-betweeness-centrality will output edges with the same highest centrality. In this case we won't be able to compare the results of both algorithms.

### Potential limitations of the method (extreme cases) and new ideas/directions to improve it

Since our implementation of the edge-betweeness-centrality complexity grow exponentially we can't use it with big graphs.

We have multiple clues how we can improve this algorithm, one is clearly to find a way to compute the number of number shortest path for every node of the graph in a better manner, having to compute a combination of every edges seems a bit off.

We looked into the networkx source code and they seem to be using another algorithm for counting the paths, which is Dijkstra algorithm's. We are not really sure to understand how they compute the number of path passing through each edges but their technics seems to be a bit different then the one we saw in the lecture.

Regarding the Girvan-Newman implementation, we also look afterwise into the networkx source code and found that it was quite similar.

Our problem seems clearly be in the computation of the edge-betweeness-centrality.
