'''
Helper/utility functions for analytical diffusion programme
'''

import numpy as np

def write_output(x,y,suffix='',out_file_path='',verbose=True):
    '''
    Write the time and outflux arrays to a csv file. The filename
    is appended with usr defined suffix and the file is written to
    the user defined output file path.
    '''

    # Combine the two arrays into 2d array
    data = np.vstack((x,y))

    # Set the output file path
    outpath = out_file_path + 'diffusion_out' + suffix + '.csv'

    # Write to csv
    print('Writing csv file at ',outpath) if verbose else None

    np.savetxt(outpath, data.T, 
              delimiter = ",")