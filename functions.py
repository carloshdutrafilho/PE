import numpy as np

def contrast(images, factor):
    # Adjust contrast with linear transform
    mean_pixel_value = np.mean(images)
    
    adjusted_images = (images - mean_pixel_value) * factor + mean_pixel_value
    adjusted_images = np.clip(adjusted_images, 0, 2**16-1).astype(np.uint16)

    return adjusted_images


def brightness(image, valeur_luminosite):
    # Calculate the image with adjusted brightness by adding the brightness value
    image_lumineuse = np.clip(image + valeur_luminosite, 0, 2**16-1).astype(np.uint16)
    
    return image_lumineuse

def moyennage_temporel(images, window):
    #Calculate the temporal averages with a window 
    n,x,y = images.shape
    output = np.copy(images)
    for i in range(n-window+1):
        output[i] = np.mean(images[i:i+window,:,:], axis = 0)
    return output  

def invert_colors(images):
    output = np.copy(images)
    return   2**16 - output

def threshold_min(images,threshold):
    output = np.copy(images)
    output[images<threshold] = 0
    return output

def threshold_max(images,threshold):
    output = np.copy(images)
    output[images>threshold] = 2**16
    return images