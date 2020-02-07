import numpy as np
import png
import pydicom
import os

from pydicom.filebase import DicomBytesIO

def convert_dicom_to_png(filename, path_to_dicom, path_to_png):
    # safely creates dir
    if not os.path.exists(path_to_png):
        os.makedirs(path_to_png)


    ds = pydicom.dcmread(path_to_dicom + filename)

    #getting n files in dir
    DIR = path_to_png
    fileN =  len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
    # so it doesn't start with 0
    fileN = str( fileN +1)
    print('n files = ' + str( len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])))

    shape = ds.pixel_array.shape
    # Convert to float to avoid overflow or underflow losses.
    image_2d = ds.pixel_array.astype(float)
    # Rescaling grey scale between 0-255
    image_2d_scaled = (np.maximum(image_2d, 0) / image_2d.max()) * 255.0
    # Convert to uint
    image_2d_scaled = np.uint8(image_2d_scaled)

    # Write the PNG file
    with open(path_to_png + fileN  + '.png', 'wb') as png_file:
        w = png.Writer(shape[1], shape[0], greyscale=True)
        w.write(png_file, image_2d_scaled)
