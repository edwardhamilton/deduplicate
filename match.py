import numpy as np
import logging
import model
class match:
    def __init__(self, filter, model):
        self.filter = filter
        self.model = model
    def run(self, indices):
        matches = []
        if ((len(indices) > 1)): # & False): # no need to check if region only has 1 item
            logging.info('matching partition of size = ' + str(len(indices)))
            indices = np.array(indices)
            filtered = self.filter.run(indices)
            matches = self.model.run(filtered)
        logging.info('adding to results: partition = ' + str(len(indices)) + ', # matches = ' + str(len(matches)))
        return (indices, matches)
