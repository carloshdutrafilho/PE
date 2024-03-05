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
    for i in range(n-window+1):
        images[i] = np.mean(images[i:i+window,:,:], axis = 0)
    return images  

def invert_colors(images):
    return   2**16 - images

def threshold_min(images,threshold):
    images[images<threshold] = 0
    return images

def threshold_max(images,threshold):
    images[images>threshold] = 2**16
    return images