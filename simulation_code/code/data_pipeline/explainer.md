### Production Data Pipeline is a DAG consistinng of three major items:
1. The Weather Module: For cleaning and resynthesizing weather from our data vendor (visualcrossing).
2. The Historical Demand Module:
   * clustering
   * demand discovery
3. Realtime Conditions Logic Module: for conditioning clustered demand according to availability.
