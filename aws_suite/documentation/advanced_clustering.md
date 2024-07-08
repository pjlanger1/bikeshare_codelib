# Advanced Cluster Research - BikeShare station-level demand forecasting

## Summer 2024

## Introduction

This document presents the findings of our refined clustering analysis towards developing LSTM 1.0. 
The goal of this analysis is to to build on the previous work done in linearly separating various types of demand patterns on the station level.

To recap, for the LSTM1.0 model, we're trying to quantify and predict pick up and drop off demand on the station level, modeled as a network as well as with exogenous variables.

## Objectives

- To test various clustering methodologies to capture the spatial and demand-level differences in low dimensions.
    We will use DBSCAN, HDBSCAN, KMeans, an algorithm of our own design and Label Propagation
- To test various ways of representing spatial data for the purposes of clustering (Uber's H3 methodology)
- To contextualize those demand patterns in geography/ what we know about this transit network & transit networks, broadly.
- To identify meaningful clusters that balance demand pattern features with locality, and validate their signficance
- Explore ways of including these covariates in the LSTM1.0 model.

## Methodology

### Data Collection

Data was collected using Transit Ventures' [API endpoint wrapper for trip history](https://github.com/pjlanger1/bikeshare_codelib/blob/2bc199b78f185f1234d018b29703b193ecc01de0/model_estimation/v1.0/model_ready_data/data_get.py) and analysis library.

Notebook will be shared.

### Data Preprocessing

Data preprocessing steps included:
- Re-reading the PCA features and clusters derived from [Cluster Research Pt 1](https://github.com/pjlanger1/bikeshare_codelib/blob/4e79b2c9cec2cc39f841d57d2ae5be568e65a484/aws_suite/documentation/cluster_research.md)
- Loading H3 networkx and the necessary sklearn utilities.

### DBSCAN ON LAT-LON PAIRS
- DBSCAN or Density-Based Spatial Clustering of Applications with Noise was our first pass attempt at refining our demand intensity clustering. We were especially interested if there were ways of pooling stations with common geography & demand patterns.
Although we didn't know exactly how the clusters should be formed, we knew some properties we wanted them to have:

--cover a distance smaller than a full neighborhood, eg. one cluster containing an enntire borough, county or even neighborhood would be unsuitable to the type of features we wanted to create, but we also did not at all want to create 2000 clusters out of the 2044 stations in scope.  

DBSCAN and HDBSCAN 

DBSCAN takes an epsilon (max dist from cluster centroid) and min cluster size parameters, which we estimated at first using K-distance. Visually, we see an elbow around 0.3, meaning that, for the underlying data (in the underlying data's units), most observations are within 0.3 units of their neighbors. 

![K-Distance 0.3 implied](/aws_suite/documentation/bin/clust2/kdist_dbscan_.png)

After some numerical tuning, we found optimal clusters.  However, there are some problems with this.

![DBSCAN BEST CLUSTER RESULT](/aws_suite/documentation/bin/clust2/dbscan.png)

1. DBSCAN classified many of the points in the most dense parts of the network as noise, which is not how we want to express the network topology, if anything we want to focus on the nuanced properties of those stations in particular.
   
2. DBSCAN also classified many fairly homogenous (in terms of being low-demand stations, contiguous to one another in uptown manhattan & the south bronx) - see the maroon cloud at the top of the above graphic. While technically accurate, we want more geographic differentiation.
   
3. We ran a battery of statistical tests on the optimal clustering from DBSCAN such as the Davies-Bouldin Index, the Calinski-Harabasz Index and the Silhouette Score (all from sklearn), and these optimal clusters poorly differentiated between clusters on both geography and demand intensity.


HDBSCAN incorporates a hierarchical component to the clustering and doesn't require hyperparameter tuning.

![HDBSCAN BEST CLUSTER RESULT](/aws_suite/documentation/bin/clust2/hdbscan_.png)

Upon fitting this to our data, we found that again, HDBSCAN may be unsuitable to this problem or data, as the algorithm selected 8 clusters, most of which were non-contiguous. 


### H3 SPATIAL REPRESENTATION

About a decade ago, Uber released something called H3, which is a hexagonal spatial indexing system that tiles the globe with various sizes of hexagonal grid. Level 15 is extremely granular (think like almost address-level) and 7 Level 15 units comprise 1 Level 14 unit, and 7 Level 14 units comprise 1 Level 13 unit and so on. 

In an effort to simplify the clustering away from methods that required numerical analysis of lat-lon pairs, we began exploring alternative representations of where stations lie on a map.

![H3 Representation of Citibike Network in 11 and 10 resolution](/aws_suite/documentation/bin/clust2/h3_10res.png)

Each lat-lon pair is generalized to a hexagonal area. In the plot above, we can see two different sizes the more granular resolution 11 and the larger resolution 10, colored by demand intensity.

We see some of the gradient visible in the PCA reduction we did in our previous cluster research. 

Perhaps by forming a network graph off of the adjacency concept we inherit from H3 representation, we can simplify community detection.

![Overlapping Clusters on Epsilon <= .24](/aws_suite/documentation/bin/clust2/h3overlap.png)

Here we created our own algorithm that colored an NYC representation in H3 by the average demand intensity value in its hexagon.

We began by representing our data in H3 at Resolution 11

If a hexagon and its nearest 7 neighbors were within more or less the same demand intensity strata, we'd allow them to agglomorate into a new cluster at lower Resolution 10. clusters that were unable to agglomorate remained at their latest resolution level.

This was semi successful, but the clusters didn't appear to be significant, and again struggled with the large uptown cluster problem we encountered with DBSCAN.

Ultimately, we found a very simple method, Label Propagation to be effective and significant.

![Label Propagation Clustering k = 86](/aws_suite/documentation/bin/clust2/h3_final_clust.png).

Our best case performed quite well the task of balancing the densities of geography with those in the feature space, proposing 86 different clusters.

![Focus: Cluster 21](/aws_suite/documentation/bin/clust2/bushw.png).
  


## Results

### Overview

The clustering process identified 4 distinct clusters.

Below are the summarized characteristics of each cluster as well as their proportion of stations in the system

- **Low Activity**: (54%) - Low Demand on Weekdays & Weekends (~1 bike/hour, on average). Geographically, these are the extents or areas to which citibike has recently moved.
- **Middle Activity**: (26%) - Middling Demand (>1 bike/hour, on average).
- **High Activity**: (16%) - High Demand (Daily Seasonality is much more apparent
- **Highest Activity** (4%) - Highest Demand, unique from high activity pattern




