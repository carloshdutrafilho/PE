import numpy as np


def contrast(images, factor):
    """
    Adjusts the contrast of images using a linear transform.

    Parameters
    -----------
    images : 3D numpy array (number_of_images, number_x_pixels, number_y_pixels)
        Pixel values must be floats between 0 and 1.
    factor : float
        Factor to adjust the contrast.

    Return
    -----------
    output : 3D numpy array
        Adjusted images.
    """
    mean_pixel_value = np.mean(images)
    
    adjusted_images = (images - mean_pixel_value) * factor + mean_pixel_value
    adjusted_images = np.clip(adjusted_images, 0, 1)

    return adjusted_images


def brightness(image, valeur_luminosite):
    """
    Adjusts the brightness of an image by adding a brightness value.

    Parameters
    -----------
    image : 3D numpy array (number_of_images, number_x_pixels, number_y_pixels)
        Pixel values must be floats between 0 and 1.
    brightness_value : float between -1 and 1
        Value to adjust the brightness.

    Return
    -----------
    output : 3D numpy array
        Image with adjusted brightness.
    """
    image_lumineuse = np.clip(image + valeur_luminosite, 0, 1)
    
    return image_lumineuse

def temporal_averaging(images, window):
    """
    Calculates the temporal averages of images using a window.

    Parameters
    -----------
    images : 3D numpy array (number_of_images, number_x_pixels, number_y_pixels)
        Pixel values must be floats between 0 and 1.
    window : Integer smaller than images.shape[0]
        Window size for averaging.

    Return
    -----------
    output : 3D numpy array
        Temporal averages of images.
    """
    n,x,y = images.shape
    output = np.copy(images)
    for i in range(n-window+1):
        output[i] = np.mean(images[i:i+window,:,:], axis = 0)
    return output  


def invert_colors(images):
    """
    Inverts the colors of images.

    Parameters
    -----------
    images : 3D numpy array (number_of_images, number_x_pixels, number_y_pixels)
        Pixel values must be floats between 0 and 1.

    Return
    -----------
    output : 3D numpy array 
        Inverted color images.
    """
    output = np.copy(images)
    return   1 - output

def threshold_min(images,threshold):
    """
   Applies a minimum threshold to images.

   Parameters
   -----------
   images : 3D numpy array (number_of_images, number_x_pixels, number_y_pixels)
       Pixel values must be floats between 0 and 1.
   threshold : Float between 0 and 1
       Threshold value.

   Return
   -----------
   output : 3D numpy array 
       Images with minimum threshold applied.
   """
    output = np.copy(images)
    output[images<threshold] = 0
    return output

def threshold_max(images,threshold):
    """
   Applies a maximum threshold to images.

   Parameters
   -----------
   images : 3D numpy array (number_of_images, number_x_pixels, number_y_pixels)
       Pixel values must be floats between 0 and 1.
   threshold : Float between 0 and 1
       Threshold value.

   Return
   --------------
   output : 3D numpy array 
       Images with maximum threshold applied.
   """
    output = np.copy(images)
    output[images>threshold] = 1
    return output