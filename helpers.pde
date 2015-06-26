
ArrayList<Tile> parseTilesIntoSet(){
  ArrayList<Tile> result= new ArrayList<Tile>();
  PImage tilesImage = loadImage(FILENAME);
  if (tilesImage == null) {
    return result;
  }
  color black = color(0,0,0);
  for (int x=0; x< (tilesImage.width-3)/4+1; x++) {
    for (int y=0; y< (tilesImage.height-3)/4+1; y++) {
      PImage image = tilesImage.get(x*4, y*4, 3, 3);
      int likelyhood = (int)pow(255-(int)red(tilesImage.get(x*4, y*4+3)),1);
      if (!( new Tile(image,likelyhood).isAllWhite()) && ((int)tilesImage.get(x*4+1, y*4+3) != color(255,0,0)))
      {
        result.add(new Tile(image, likelyhood));
        if(tilesImage.get(x*4+3,y*4)==black){
          Tile rotation1 = new Tile( get90DegClockwiseRotation(image), likelyhood);
          Tile rotation2 = new Tile( get90DegClockwiseRotation(rotation1.image), likelyhood);
          Tile rotation3 = new Tile( get90DegClockwiseRotation(rotation2.image), likelyhood);
          result.add(rotation1);
          result.add(rotation2);
          result.add(rotation3);
        }
      }
    }
  }
  
  return result;
}

boolean imagesEqual(PImage image1, PImage image2) {
  if (image1 == null || image2==null) {
    return false;
  }
  for (int x=0; x<image1.width; x++) {
    for (int y=0; y<image1.height; y++) {
      if (image1.get(x, y) != image2.get(x, y)) {
        return false;
      }
    }
  }
  return true;
}


float fractionOfImagesEqual(PImage image1, PImage image2) {
  float size = image1.width*image1.height;
  float numMatchingPixels = 0;
  if (image1 == null || image2==null) {
    return 1;
  }
  for (int x=0; x<image1.width; x++) {
    for (int y=0; y<image1.height; y++) {
      if (image1.get(x, y) == image2.get(x, y)) {
        numMatchingPixels++;
      }
    }
  }
  return numMatchingPixels/size;
}



Directions opposite (Directions in) {
  if (in == Directions.up) {
    return Directions.down;
  }
  if (in == Directions.down) {
    return Directions.up;
  }
  if (in == Directions.left) {
    return Directions.right;
  } else {
    return Directions.left;
  }
}



Tile getRandomChoice(ArrayList<Tile> list){
  int weightSum =0;
  for (Tile test : list){
    weightSum += test.likelyhood;
   
  }
  int choice = (int)random(weightSum);
  Collections.shuffle(list);
  for (Tile test2 : list){
    choice -= test2.likelyhood;
    if(choice<=0){
      return test2;
    }
  }
  return null;
}





Directions getDirectionFromDelta(int dX, int dY) {
  if (dX==0 && dY == -1) {
    return Directions.up;
  } else if (dX==0 && dY == 1) {
    return Directions.down;
  } else if (dX==1 && dY == 0) {
    return Directions.right;
  } else {
    return Directions.left;
  }
}

PImage get45DegClockwiseRotation(PImage toRotate) {
  PImage result = toRotate.get(0, 0, 3, 3);

  result.set(1, 0, toRotate.get(0, 0));
  result.set(2, 0, toRotate.get(1, 0));
  result.set(2, 1, toRotate.get(2, 0));
  result.set(2, 2, toRotate.get(2, 1));

  result.set(1, 2, toRotate.get(2, 2));
  result.set(0, 2, toRotate.get(1, 2));
  result.set(0, 1, toRotate.get(0, 2));
  result.set(0, 0, toRotate.get(0, 1));
  
  return result;
}

PImage get90DegClockwiseRotation(PImage toRotate) {
  PImage result = get45DegClockwiseRotation(toRotate);
  return get45DegClockwiseRotation(result);
}

void normalizeTileLikelyhoods(ArrayList<Tile> tiles){
  float totalWeights = 0;
  for (Tile tile: tiles){
    totalWeights += tile.likelyhood;
  }
  for (Tile tile: tiles){
    tile.likelyhood /= totalWeights;
  }
}
