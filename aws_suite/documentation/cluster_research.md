# Cluster Research Summer 2024

## Introduction

This document presents the findings of our clustering analysis towards developing LSTM 1.0. 
The goal of this analysis is to identify meaningful clustering of stations within the system on the basis of geography and traffic patterns.

For LSTM1.0 model, we're trying to quantify and predict pick up and drop off demand on the station level, modeled as a network as well as with exogenous variables.

## Objectives

- To understand how stations' demand patterns vary over time, on average - interested in intraday seasonality.
- To contextualize those demand patterns in geography/ what we know about this transit network & transit networks, broadly.
- To identify distinct patterns, in magnitude or shape of average demand graphs, cluster into categories of volume [high, med, low]
- To analyze the characteristics that differentiate these groups.
- Explore the suitability of these clusters for inclusion in an embeddings layer of LSTM1.0

## Methodology

### Data Collection

Data was collected using Transit Ventures' [API endpoint wrapper for trip history](https://github.com/pjlanger1/bikeshare_codelib/blob/2bc199b78f185f1234d018b29703b193ecc01de0/model_estimation/v1.0/model_ready_data/data_get.py) and analysis library.

Notebook will be shared.

### Data Preprocessing

Data preprocessing steps included:
- Normalization of data to ensure uniform scale.
- Handling missing values through imputation or 0 replacement
- Removal of Hoboken/Jersey City Citibike Stations from the test set.

### Data Structure
- Sliced each station up into starting and ending counts at the end of each hour.
- Here's a lighthearted look into a side question: *does visibility of a station make much of a difference to demand on its bikes, relative to a nearby (arbitrarily close <0.1 miles away) station.
- Anyway all the data we used for this section was a vector of mean demand values per hour, per station, which we sometimes below aggregate further into cluster level measures.

![Cluster Distribution](/aws_suite/documentation/bin/bshare_psych.png)
  
  *These two stations are a block or ~0.07 mi from one another. Why is one used so much more? Because more people see it, we suspect*

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
**Demand for Pick-Ups from Clustered Stations**
[Cluster Distribution](/aws_suite/documentation/bin/bsharechart1a.png)
  *Figure 2: Visualization of clusters by mean hourly pick-up demand*

## Discussion

Discuss the implications of the findings and any interesting patterns observed. Highlight any trends or anomalies in the cluster characteristics.

## Conclusion

Summarize the key findings and potential applications of this clustering analysis. Discuss future work and improvements to the methodology.

## References

1. Author Name, Article Title, Journal, Year.
2. Author Name, Book Title, Publisher, Year.

## Appendix

Additional supporting information or data tables can be provided here.

