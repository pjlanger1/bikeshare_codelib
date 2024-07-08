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




  
  *These two stations are a block or ~0.07 mi from one another. Why is one used so much more? Because more people see it, we suspect*

- These two stations are a block apart, and less than 1/10 of a mile apart. The more popular of the two exists right in front of the southwestern entrance of Prospect Park.  The less popular of the two exists a 2-3 min walk down the same street.

- This example should illustrate and inform the theory behind clustering stations on more than just geography.

- **The more popular of the two stations is classified by our clustering as a 'highest acivity' station**

- **The less popular is a middle-level activity station**

### Custom Algorithm for balancing community detection with clustering of historical average patterns
1. **Standard Scale (Lat,Lon) and 1 x 24 vector embedding of mean hourly historical demand**
2. **Run PCA on the 24 dimensional hourly demand** We're looking for linear separability, so we only want PC1 from any PCA we run on start demand.
   results can also be run on end_demand and weekend-weekday flavors of both measures.
3. **Once we've obtained that/those PCs, cluster on their basis.**
4. **Append cluster ID to (Lat,Lon) and run K-means clustering on it. We want to detect communities within communities, so clusters of different activity type in various geographic regions. Adjust resolution (k parameter) to achieve desired results.**


## Results

### Overview

The clustering process identified 4 distinct clusters.

Below are the summarized characteristics of each cluster as well as their proportion of stations in the system

- **Low Activity**: (54%) - Low Demand on Weekdays & Weekends (~1 bike/hour, on average). Geographically, these are the extents or areas to which citibike has recently moved.
- **Middle Activity**: (26%) - Middling Demand (>1 bike/hour, on average).
- **High Activity**: (16%) - High Demand (Daily Seasonality is much more apparent
- **Highest Activity** (4%) - Highest Demand, unique from high activity pattern


### Figures

![Geographic Distribution Clustered Stations](/aws_suite/documentation/bin/bikeshare_62024.png)
*Figure 1: Visualization of clusters by Lat-Lon based onn mean hourly net demand*

![Demand for Pick-Ups from Clustered Stations](/aws_suite/documentation/bin/bsharechart1a.png)
*Figure 2a: Visualization of clusters by mean hourly Pick-up demand*

![Demand for Drop-Offs from Clustered Stations](/aws_suite/documentation/bin/bsahrepe2.png)
*Figure 2b: Visualization of clusters by mean hourly Drop-off demand*

![Linear Separability of Demand Patterns](/aws_suite/documentation/bin/bshare_pca.png)  
*Figure 3: Visualization of Reduced Dimension Spaces (Pick-up Vs. Drop-Off) Lends linear separability well*


## Discussion

Figure 1 - the map lends itself well to our current understanding of the citibike system. the blue areas on the map overlap considerably and almost in all cases with areas to which the Citibike System has recently expanded. Bronx, Eastern Queens & SouthWest Brooklyn are the recent expansion zones, some of the installation projects ended as recntly as Q4 of 2023.

The hotspots (red and orange) also correspond well to locations of large commuting destinations (lower manhattan and midtown west, with hotspots emerging in Williamsburg Brooklyn, Downtown Brooklyn and near large city parks like Central and Prospect. respectively. 

The green stations are also providing an important gradient for understanding system evolution as a whole from creation. The colors of the map very clearly show the evolution of the system.

Figure 2a and 2b - demonstrate that to the standard of a 95% confidence interval (assuming gaussian) the differences in pattern appear to hold and be statistically significant.

Figure 3 - demonstration of linear separability in the reduced space: on the basis of orthogonal features intended to explain as much variance as possible, the clusters can be separated by intensity of demand. the PCA was fed scaled features corresponding to intensity of demand for pick-up and drop-off of bikes on both weekdays and weekends.
therefore, the separability can be interpreted in the same way.

## Conclusion

Clustering on the basis of a reduced dimension demand vector appears successful and defensible:
(a) cluster assignment was able to linearly separate stations on the basis of historical demand patterns
(b) clusters appeared to correspond to expert judgement on the function/dynamics/history of the network
(c) this opens up many possibilities as far as combining geographic and historical features in a unified, balanced clustering problem space.

## References

1. Author Name, Article Title, Journal, Year.
2. Author Name, Book Title, Publisher, Year.

