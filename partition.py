import logging
import utils
import geopandas
import numpy as np
import shapely
# partitions a panda dataframe (with geometry)
class partition: # requires that context has a geopanda dataframe named gdf and a context object with partition_divisor, max_partition_span, and max_partition_size
    def __init__(self, data, divisor, max_span, max_size):
        self.gdf = data
        self.divisor = divisor
        self.max_span = max_span
        self.max_size = max_size
    def run(self, indices):
        result = []
        if (len(indices) == 0):
            return result
        logging.info('partition_or_match_region size = ' + str(len(indices)))
        xmin, ymin, xmax, ymax, partition_size, partition_span = self.get_bounds(indices)
        cell_xsize = (xmax-xmin)/self.divisor
        cell_ysize = (ymax-ymin)/self.divisor
        grid_cells = []
        for x0 in np.arange(xmin, xmax+cell_xsize, cell_xsize ):
            for y0 in np.arange(ymin, ymax+cell_ysize, cell_ysize):
                x1 = x0-cell_xsize
                y1 = y0+cell_ysize
                grid_cells.append(shapely.geometry.box(x0, y0, x1, y1))
        cells = geopandas.GeoDataFrame(grid_cells, columns=['geometry'])
        logging.info('# cells = ' + str(len(cells)) + ', xrange = ' + str(xmax - xmin) + ', yrange = ' + str(ymax - ymin))
        merged = geopandas.sjoin(self.gdf.iloc[indices], cells, how='inner', op='within')
        groups = merged.groupby('index_right').groups
        for r in groups.values():
            result.append(list(r)) #, timeout=_timeout)
        return result
    def get_bounds(self, indices):
        tolerance = .0001 # about 11 meters.   Need this, otherwise we lose some records
        xmin, ymin, xmax, ymax= self.gdf.iloc[indices].total_bounds
        xmin=xmin - tolerance
        ymin=ymin - tolerance
        xmax=xmax + tolerance
        ymax=ymax + tolerance
        partition_size = len(indices) # we want to keep regions small enough so cross-product matching will not be too slow
        partition_span = utils.haversine(xmin, ymin, xmax, ymax)
        return xmin, ymin, xmax, ymax, partition_size, partition_span
    def done(self, indices):
        xmin, ymin, xmax, ymax, partition_size, partition_span = self.get_bounds(indices)
        return (partition_span < self.max_span) & (partition_size < self.max_size)
