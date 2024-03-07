import matplotlib.pyplot as plt
import tifffile
from matplotlib.patches import Polygon
import numpy as np
import csv

###################################################################################################
#                            Function : inPolygon(NbCorners,polyX,polyY,test)

#Args : 

# NbCorners : number of corners defining the polygon
# polyX : list of x coordinates of corners
# polyY : list of y coordinates of corners
# test : the point [x,y] we want to know if it's inside the polygone or not

#Return : return true if the test point is inside the polygon and false if it's not.
###################################################################################################


def inPolygon(NbCorners,polyX,polyY,test):
    x,y=test
    i,j=NbCorners-1,NbCorners-1
    oddNodes=False
    for i in range(NbCorners):
        if (polyY[i]<y and polyY[j]>=y or polyY[j]<y and polyY[i]>=y):
            if (polyX[i]+(y-polyY[i])/(polyY[j]-polyY[i])*(polyX[j]-polyX[i])<x):
                oddNodes=not(oddNodes)
        j=i
    return oddNodes

###################################################################################################
#                            Function : listIn(Nbcorners,polyX,polyY)

#Args : 

# NbCorners : number of corners defining the polygon
# polyX : list of x coordinates of corners
# polyY : list of y coordinates of corners

#Return : return the list of pixels inside the polygon. 
###################################################################################################

def listIn(Nbcorners,polyX,polyY):
    left=int(min(polyX))# pixels inside the polygone are inside a known square
    right=int(max(polyX))
    top=int(max(polyY))
    bot=int(min(polyY))
    resX=[]
    resY=[]
    for x in range (left,right,1):
        for y in range(bot,top,1):
            if inPolygon(Nbcorners,polyX,polyY,(x,y)):
                resX.append(x)
                resY.append(y)
    return resX,resY
            
###################################################################################################
#                            Function : mean(image,listX,listY)

#Args : 

# image : the image containing the observed pixels
# listX : list of x coordinates of pixelsto be averaged
# listY : list of y coordinates of pixelsto be averaged


#Return : The mean of the image pixels in the list
###################################################################################################


def mean(image,listX,listY):
    print("Nbre de points moyennés X: ", len(listX) )
    print("Nbre de points moyennés Y: ", len(listY) )
    out=0
    for i in range(0,len(listX)):
        out+=image[listY[i]][listX[i]]
    out=out/len(listX)
    return out

###################################################################################################
#                            Function : meanOverTime(listImage,listX,listY)

#Args : 

# listImage : list of sucessive images in time
# listX : list of x coordinates of pixels to be averaged on each instant
# listY : list of y coordinates of pixels to be averaged on each instant


#Return : A list containing the mean on images at each instant
###################################################################################################

def meanOverTime(listImage,listX,listY):
    out=[]
    for e in listImage :
        out.append(mean(e,listX,listY))
    return out
    
###################################################################################################
#                            Function : distance(p1, p2)

#Args : 

# p1,p2 : Two points 


#Return : Distance between two points
###################################################################################################

def distance(p1, p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

###################################################################################################
#                            Function : color_points(x_coords, y_coords, colors):

#Args : 

#x_coords : list of x coordinates of points to be colored
#y_coords : list of y coordinates of points to be colored


#Effect : color given points

#No return
###################################################################################################

def color_points(x_coords, y_coords, colors):
    plt.figure()
    plt.scatter(x_coords, y_coords, cmap='viridis')
    plt.colorbar(label='Valeur de couleur')
    plt.title('Nuage de points coloré')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)
    plt.xlim(0, 519) 
    plt.ylim(0, 512)  
    plt.show()



#######################################################################################################
    #                            Function : Segmentation(images,index):

#Args : 

#images : list of images to apply segmentation
#index : index of the image on which the region of interest is drawn




#No return
#######################################################################################################

def Segmentation(images,index):


    # Open the image where detecting activation is easy (thanks to scroll images). To do : implement scrolling before segmentation
    green = images[0][index]

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

    # Detect click to draw the region of interest
    def onclick(event):
        nonlocal x_coords, y_coords
        
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

    # Connect the onclick function to the mouse click event
    fig.canvas.mpl_connect('button_press_event', onclick)

    # Plot the figure to draw polygon
    plt.show()

    # X stores x coordonates of pixels inside the drawn polygon
    X,Y=listIn(len(x_coords),x_coords,y_coords)

    # Color given points
    color_points(X,Y,1)


    # List of intensities
    res=meanOverTime(images[1],X,Y)

    # Plot intensities over time
    plt.plot(range(len(res)), res)
    plt.xlabel('Image index')
    plt.ylabel('Intensity')
    plt.show()

    # Define CSV file name
    file_name = 'data.csv'

    # Write to the CSV file
    with open(file_name, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
    
        # Write headers if needed
        writer.writerow(['Column1', 'Column2'])
    
     # Write data from lists
        for value1, value2 in zip(res, range(len(res))):
            writer.writerow([value1, value2])




def import_csv(filePath):

    # Initialize lists for each column
    column1 = []
    column2 = []

    # Read from the CSV file and populate the lists
    with open(filePath, mode='r', newline='', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # Skip header row if exists
        for row in reader:
            # Assuming two columns, if more columns, adjust indices accordingly
            column1.append(row[0])
            column2.append(row[1])

    return column1,column2


def fileToGraph(filePath):
    l1,l2=import_csv(filePath)
    plt.plot(l1,l2)
    plt.xlabel('Image index')
    plt.ylabel('Intensity')
    plt.show()

    

#range(len(res)), res
############################################################################################
#                               Example of use case
############################################################################################

imstack= tifffile.imread('220728-S2_04_500mV.ome.tiff')  
Segmentation(imstack, 352)

#fileToGraph('data.csv')