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

##Structure
- ![Cluster Distribution](/aws_suite/documentation/bin/bshare_psych.png)
  *Figure 1: Visualization of clusters*

### Clustering Algorithm


We employed the K-means clustering algorithm for this analysis:
1. **Initialization**: Set the number of clusters K and randomly initialize the cluster centroids.
2. **Assignment**: Assign each data point to the nearest cluster centroid.
3. **Update**: Recompute the centroids based on the assignments.
4. **Repeat**: Continue the assignment and update steps until convergence.

## Results

### Overview

The clustering process identified X distinct clusters. Below are the summarized characteristics of each cluster:

- **Cluster 1**: Description or dominant characteristics.
- **Cluster 2**: Description or dominant characteristics.
- **Cluster 3**: Description or dominant characteristics.

### Figures

- ![Cluster Distribution](aws_suite/documentation/bin/bshare_psych.png)
  *Figure 1: Visualization of clusters*

## Discussion

Discuss the implications of the findings and any interesting patterns observed. Highlight any trends or anomalies in the cluster characteristics.

## Conclusion

Summarize the key findings and potential applications of this clustering analysis. Discuss future work and improvements to the methodology.

## References

1. Author Name, Article Title, Journal, Year.
2. Author Name, Book Title, Publisher, Year.

## Appendix

Additional supporting information or data tables can be provided here.

