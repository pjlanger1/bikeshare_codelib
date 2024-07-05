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
- Re-reading the PCA features derived from [API endpoint wrapper for trip history](https://github.com/pjlanger1/bikeshare_codelib/blob/2bc199b78f185f1234d018b29703b193ecc01de0/model_estimation/v1.0/model_ready_data/data_get.py) and analysis library.


### Data Structure
- Sliced each station up into starting and ending counts at the end of each hour, take mean, variance measurements.
- each station has a 0 indexed vector for ex. (1,1,1,0,0,0,1,1,2,1,1,0,2,2,3,4,3,2,1,1,1,1,1,0), where the index represents the hour and the value represents the average demand for that hour for that station, over time.

### A Brain-Teaser
- Here's a lighthearted look into a side question: *does visibility of a station make much of a difference to demand on its bikes, relative to a nearby (arbitrarily close <0.1 miles away) station, see the images below.
  
- All the data we used for this section was a vector of mean demand values per hour, per station, which we sometimes aggregate further into cluster level measures.

![Cluster Distribution](/aws_suite/documentation/bin/bshare_psych2.png)

![Map of these Two Stations](/aws_suite/documentation/bin/cb_pp_map.png)
  
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

