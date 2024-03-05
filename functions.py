import numpy as np

def contrast(image, valeur_contraste):
    #Calculate the contrasted image by multiplying by the contrast value
    image_contrastee = np.clip(image * valeur_contraste, 0, 255).astype(np.uint8)
    
    return image_contrastee


def brightness(image, valeur_luminosite):
    # Calculate the image with adjusted brightness by adding the brightness value
    image_lumineuse = np.clip(image + valeur_luminosite, 0, 255).astype(np.uint8)
    
    return image_lumineuse

def moyennage_temporel(images, nb_images):
    #Calculate the temporal averages with a window of number of nb_images
    n,x,y = images.shape
    for i in range(n-nb_images+1):
        images[i] = np.mean(images[i:i+20,:,:], axis = 0)
    return images
    