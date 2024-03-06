import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np
from  Segmentation import listIn
from Segmentation import mean
from Segmentation import meanOverTime
from Segmentation import distance
from Segmentation import color_points
import tifffile



#################################################################################################################
# Detect click to draw polygon
def onclick(event):
    global x_coords, y_coords
    
    # Check if click is within image boundaries
    if event.xdata is not None and event.ydata is not None:
        # Add click coordinates to polygon point list
        x_coords.append(event.xdata)
        y_coords.append(event.ydata)
        
        # Draw polygon with current vertices
        if len(x_coords) > 1:
            polygon = Polygon(list(zip(x_coords, y_coords)), closed=False, fill=None, edgecolor='red')
            ax.add_patch(polygon)
        
        # Check polygon closure
        if len(x_coords) > 2 and distance((x_coords[0], y_coords[0]), (event.xdata, event.ydata)) < 5:
            polygon = Polygon(list(zip(x_coords, y_coords)), closed=True, fill=None, edgecolor='red')
            ax.add_patch(polygon)
            x_coords.pop(),y_coords.pop()
        
        # Update display
        fig.canvas.draw()



###############################################################################################################




# Read tiff file
chemin_fichier = '220728-S2_04_500mV.ome.tiff'
imstack = tifffile.imread(chemin_fichier)





# Open the image where detecting activation is easy (thanks to scroll images). To do : implement scrolling before segmentation
green = imstack[0][352]


# Rescale 16-bit data to 8-bit 
green_channel_8bit = (green - np.min(green))/ (2**16 -np.max(green)) * 255

# Swap White/Black
image = 255-green_channel_8bit

# Initialize figure

fig, ax = plt.subplots()
ax.imshow(image.astype(int), cmap='gray')
ax.invert_yaxis()

# Initialize two lists to store the coordinates of polygon vertices
x_coords = []
y_coords = []



# Connect the onclick function to the mouse click event
fig.canvas.mpl_connect('button_press_event', onclick)

# Plot the figure to draw polygon
plt.show()

# X stores x coordonates of pixels inside the drawn polygon
X,Y=listIn(len(x_coords),x_coords,y_coords)

# Color given points
color_points(X,Y,1)


# List of intensities
res=meanOverTime(imstack[1],X,Y)

# Plot intensities over time
plt.plot(range(len(res)), res)
plt.xlabel('Image index')
plt.ylabel('Intensity')
plt.show()

