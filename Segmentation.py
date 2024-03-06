import matplotlib.pyplot as plt


###################################################################################################
#                            Function : inPolygon(NbCorners,polyX,polyY,test)

#Args : 

# NbCorners : number of corners defining the polygon
# polyX : list of x coordonates of corners
# polyY : list of y coordonates of corners
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
#                            Function : inPolygon(NbCorners,polyX,polyY,test)

#Args : 

# NbCorners : number of corners defining the polygon
# polyX : list of x coordonates of corners
# polyY : list of y coordonates of corners
# test : the point [x,y] we want to know if it's inside the polygone or not

#Return : return true if the test point is inside the polygon and false if it's not.
###################################################################################################

def listIn(Nbcorners,polyX,polyY):
    left=int(min(polyX))
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
#                            Function : inPolygon(NbCorners,polyX,polyY,test)

#Args : 

# NbCorners : number of corners defining the polygon
# polyX : list of x coordonates of corners
# polyY : list of y coordonates of corners
# test : the point [x,y] we want to know if it's inside the polygone or not

#Return : return true if the test point is inside the polygon and false if it's not.
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
#                            Function : inPolygon(NbCorners,polyX,polyY,test)

#Args : 

# NbCorners : number of corners defining the polygon
# polyX : list of x coordonates of corners
# polyY : list of y coordonates of corners
# test : the point [x,y] we want to know if it's inside the polygone or not

#Return : return true if the test point is inside the polygon and false if it's not.
###################################################################################################

def meanOverTime(listImage,listX,listY):
    out=[]
    for e in listImage :
        out.append(mean(e,listX,listY))
    return out
    

# Calculating the distance between two points
def distance(p1, p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

#color given points
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

    

