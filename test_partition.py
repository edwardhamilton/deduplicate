import numpy as np
import pandas as pd
import shapely
import geopandas
import statistics
import partition



size = 1000
data = { 'id': list(range(0, size)), 'lng' : list(np.random.randint(1, 1000, size = size)),  'lat' : list(np.random.randint(1, 1000, size = size)) }
df = pd.DataFrame(data)
gdf = geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(df.lng, df.lat))

if __name__ == '__main__':
    print(len(gdf.index))
    #print(partition.partition(gdf=gdf, divisor=10, max_span=10, max_size=10).run(gdf.index))
