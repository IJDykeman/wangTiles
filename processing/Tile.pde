class Tile{
 PImage image;
 int likelyhood;
 Tile(PImage nimage, int nlikelyhood){
    image = nimage;
    likelyhood = nlikelyhood;
    
 }
 
 Tile (Tile toCopy){
   image = toCopy.image;
   likelyhood = toCopy.likelyhood;
 }
 
  void draw(int xIndex, int yIndex){
    
    image(image,tileWidth*xIndex,tileWidth*yIndex,tileWidth,tileWidth);
  }
  
  boolean isValidNeighbor(Tile neighbor, Directions directionToNeighbor){
    if( neighbor == null){
      return true;
    }
    boolean edgesMatch =imagesEqual( getStrip(directionToNeighbor),neighbor.getStrip(opposite(directionToNeighbor)));
    //println (directionToNeighbor);
    return edgesMatch;

  }
  
  
  float edgeFractionInCommonWithNeighbor(Tile neighbor, Directions directionToNeighbor){
    if( neighbor == null){
      return 0;
    }
    return fractionOfImagesEqual( getStrip(directionToNeighbor),neighbor.getStrip(opposite(directionToNeighbor)));

  }

  
  PImage getStrip(Directions direction){
    switch(direction){
      case up:
       return image.get(0,0,3,1);
      case down:
       return image.get(0,2,3,1);
      case left:
       return image.get(0,0,1,3);
      default: //right
       return image.get(2,0,1,3);
    }
  }
  
  
  boolean isAllWhite(){
    for (int x=0;x<2;x++){
      for (int y=0;y<2;y++){
        int hue = image.get(x,y);
        if(red(hue) != 255 || green(hue) != 255 || blue(hue) != 255){
          return false;
        }
      }
    }
    return true;
  }
  
  
  
}
