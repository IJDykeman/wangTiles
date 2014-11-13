
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


void flipTilesAround(int x, int y) {
  ArrayList<TileLoc> toReset = new ArrayList<TileLoc>();

  toReset.add(new TileLoc(x-1, y));

  toReset.add(new TileLoc(x+1, y));

  toReset.add(new TileLoc(x, y+1));

  toReset.add(new TileLoc(x, y-1));
  if (random(1)<.5) {
    Collections.reverse(toReset);
  }
  if (random(1)<.5) {
    toReset.add(1, new TileLoc(x, y));
  } else {
    toReset.add(3, new TileLoc(x, y));
  }
  //Collections.shuffle(toReset);
  flipTilesAndNeighbors(toReset);
}

void flipTopLeft() {

  for (int x=0; x<mapWidth; x++) {
    for (int y=0; y<mapWidth; y++) {
      //for (int i=0; i<400; i++) {
      //int x=(int)random(mapWidth);
      //int y=(int)random(mapWidth);
      if (map[x][y]==null) {
        flipTilesAround(x, y);
      }
      //}
    }
  }
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

boolean isWithinMap(TileLoc loc) {
  return loc.x<mapWidth && loc.x >= 0 && loc.y<mapWidth && loc.y >= 0;
}


void placeTileAt(int x, int y) {
  int ex = x;//(int)random(mapWidth);
  int why = y;//(int)random(mapWidth);
  if (map[ex][why] == null) {
    ArrayList<Tile> options = validTilesAt(x, y);
    Tile tile=null;
    if (options.size()>0) {
      tile =  getRandomChoice(options);
    }
    map[ex][why] = tile;
  }
}

Tile getRandomChoice(ArrayList<Tile> list){
  int weightSum =0;
  for (Tile test : list){
    weightSum += test.likelyhood;
   
  }
   println("like um "+ weightSum);
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


ArrayList<Tile> validTilesAt(int tileX, int tileY) {
  ArrayList<Tile> result = new ArrayList<Tile>();
  for (Tile test : wangTiles) {
    if (isValidPlacement(test, tileX, tileY)) {
      result.add(test);
    }
  }
  return result;
}

boolean isValidPlacement(Tile tile, int tileX, int tileY) {
  boolean result =  
    isValidNeighbor(tile, tileX, tileY, tileX+1, tileY) &&
    isValidNeighbor(tile, tileX, tileY, tileX-1, tileY) &&
    isValidNeighbor(tile, tileX, tileY, tileX, tileY+1) &&
    isValidNeighbor(tile, tileX, tileY, tileX, tileY-1);

  return result;
}

boolean isValidNeighbor(Tile tile, int tileX, int tileY, int neighborX, int neighborY) {
  if (neighborX>=mapWidth || neighborY>=mapWidth || neighborX<0 || neighborY<0) {
    return true;
  } else {

    Directions direction = getDirectionFromDelta(neighborX-tileX, neighborY-tileY);             
    return tile.isValidNeighbor(map[neighborX][neighborY], direction);
  }
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

