# A Network Flows Approach to Understanding Bikesharing as Mass Transit

**Author(s):** Peter Langer  
**Affiliation:**  Transit Ventures
**Date:**  November 1, 2024

## Abstract
*Provide a concise summary of the research goals, methods, and findings.*

---

## Table of Contents
1. [Introduction](#introduction)
2. [Literature Review](#literature-review)
3. [Domain Introduction](#domain-introduction)
4. [Data](#data)
5. [Experiments](#experiments)
6. [Conclusion](#conclusion)
7. [References](#references)

---

## Introduction
*Introduce the research problem, its context, and relevance. Outline the objectives and significance of the study.*

---

## Literature Review

### Geospatial Network Analysis
A significant amount of research has explored geospatial network analysis, focusing on the interactions and flow patterns within urban environments. Notable work by Xin et al. (2020) utilized network analysis to understand movement within bike-sharing systems, specifically during the COVID-19 pandemic, identifying shifts in usage patterns and the resulting operational challenges for rebalancing stations (Xin et al., 2023).

### OD Clustering in Urban Mobility
Understanding urban movement patterns often involves clustering origin-destination (OD) data to highlight key flow patterns and popular routes. In their work, Teixeira and Lopes (2020) applied OD clustering to urban bike-sharing data to uncover changes in commuting and recreational usage. This analysis is crucial for adaptive urban mobility systems, especially in response to external pressures like a pandemic.

### Network Analysis in Public Transport
Previous research has established the importance of network analysis in public transportation, examining how individual station connectivity impacts overall accessibility. Spink (2011) provided a foundational framework for this, leveraging a spatial network approach to map and evaluate travel flows in urban transit systems.

---

## Domain Introduction
Bike-sharing networks have become integral to urban mobility, allowing for efficient, eco-friendly, and accessible travel. The need for analysis tools that can model, simulate, and adapt to varying demand patterns is critical, particularly as factors like the COVID-19 pandemic alter user behavior.

This study employs geospatial network analysis and OD clustering on New York City's Citi Bike system data, drawing from methodologies presented in Xin et al. (2023), Teixeira and Lopes (2020), and Spink (2011).

---

## Data

### Sources
- **Bike-Sharing Ride Data**: Obtained from Citi Bike, New York City, covering the period from January 2019 to December 2020.
- **Station Information**: Latitude, longitude, and station identifiers for each location.

### Preprocessing
- Extracted coordinates and identified trips between unique station pairs.
- Filtered data for completeness and relevance, focusing on high-frequency station pairs.

---

## Experiments

### Experiment 1: Network Structure Analysis
Using geospatial network methods, we analyzed node degree, edge flows, and clustering coefficients across stations to understand network connectivity.

#### Methodology
1. **Network Construction**: Nodes represent stations, and edges indicate rides between stations.
2. **Metrics Computed**: Average node degree, flow variance, and clustering coefficients.

### Experiment 2: OD Clustering Analysis
Applying OD clustering, we grouped high-flow OD pairs to highlight dominant travel patterns and spatial proximities.

#### Methodology
1. **Pairwise Station Analysis**: Calculated distances and directional angles between station pairs.
2. **Clustering Parameters**: Used distance and flow thresholds to form clusters of high-activity OD pairs.

### Results
- *Summarize findings, patterns, and insights.*

---

## Conclusion
*Summarize the main findings, limitations, and potential applications. Discuss future research directions.*

---

## References

1. Xin, R., Ding, L., Ai, B., Yang, M., Zhu, R., Cao, B., & Meng, L. (2023). Geospatial Network Analysis and Origin-Destination Clustering of Bike-Sharing Activities during the COVID-19 Pandemic. *ISPRS International Journal of Geo-Information*, 12(1), 23. [https://doi.org/10.3390/ijgi12010023](https://www.mdpi.com/2220-9964/12/1/23)

2. Teixeira, J.F., & Lopes, M. (2020). The link between bike sharing and subway use during the COVID-19 pandemic: The case-study of New York’s Citi Bike. *ISPRS International Journal of Geo-Information*, 9(2), 128. [https://doi.org/10.3390/ijgi9020128](https://www.mdpi.com/2220-9964/9/2/128)

3. Spink, A. (2011). Analysis of Network Structure and Accessibility in Public Transit Networks. *PhD Thesis*, Ohio State University. [OhioLINK](https://etd.ohiolink.edu/acprod/odb_etd/ws/send_file/send?accession=osu1299688722&disposition=inline)

---

*End of Report*
