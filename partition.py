class partition: # requires that context has a geopanda dataframe named gdf
    def __init__(self, context, region):
		if (len(region) == 0):
			return []
		trace('partition_or_match_region size = ' + str(len(region)))
		xmin, ymin, xmax, ymax, region_size, region_span = self.get_region_bounds(context, region)
		avg_dim = (((xmax-xmin) + (ymax-ymin)) / 2.0)
		cell_size = max(tolerance, (avg_dim / math.sqrt(_region_division_size)))
		xsize = ((xmax-xmin) / avg_dim) * cell_size
		ysize = ((ymax-ymin) / avg_dim) * cell_size
		cell_size = (xmax-xmin)/_region_division_size
		grid_cells = []
		for x0 in np.arange(xmin, xmax+cell_size, cell_size ):
			for y0 in np.arange(ymin, ymax+cell_size, cell_size):
				x1 = x0-cell_size
				y1 = y0+cell_size
				grid_cells.append( shapely.geometry.box(x0, y0, x1, y1)  )			
		cells = geopandas.GeoDataFrame(grid_cells, columns=['geometry'])
		rf = context.gdf.iloc[region]
		merged = geopandas.sjoin(rf, cells, how='inner', op='within')
		groups = merged.groupby('index_right').groups
		trace('groups = ' + str(len(groups.values())))
		self.result = []
		for r in groups.values():
			self.result.append(r) #, timeout=_timeout)
	def get_bounds(self, context, region):
		rf = context.gdf.iloc[region]
		tolerance = .0001 # about 11 meters.   Need this, otherwise we lose some records
		xmin, ymin, xmax, ymax= rf.total_bounds
		xmin=xmin - tolerance
		ymin=ymin - tolerance
		xmax=xmax + tolerance
		ymax=ymax + tolerance
		region_size = len(rf) # we want to keep regions small enough so cross-product matching will not be too slow
		region_span = haversine(xmin, ymin, xmax, ymax	
		return xmin, ymin, xmax, ymax, region_size, region_span
	def done(self, context, region):
		xmin, ymin, xmax, ymax, region_size, region_span = self.get_region_bounds(context, region)
		return (region_span < _max_region_span) & (region_size < _max_region_size)

