class ConstrainedMap extends Map {


  ConstrainedMap(int imapWidth, int itileWidth) {
    tilesImage = loadImage(FILENAME);
    mapWidth = imapWidth;
    tileWidth = itileWidth;
    timeSinceMapBuild = 0; //reset so that this map's processing time counts from 0
    wangTiles = parseTilesIntoSet();
    //normalizeTileLikelyhoods(wangTiles);
    tiles = new Tile[mapWidth][mapWidth];
    ArrayList<PVector> tileLocs = new ArrayList<PVector>();
    for (int x=0; x<mapWidth; x++) {
      for (int y=0; y<mapWidth; y++) {
        tileLocs.add(new PVector(x, y));
      }
    }
    Collections.shuffle(tileLocs);
    for (PVector test : tileLocs) {
      placeTileAt((int)test.x, (int)test.y);
    }
  }

  void update() {
    int numIterations = 1;
    if (timeSinceMapBuild>10) {
      numIterations = 20;
    }
    // if the simulation has been running a long time,
    // up the amount of modification done per frame.
    for (int i=0; i<numIterations; i++) {
      flipTopLeft();
    }
    timeSinceMapBuild++;
  }





  void flipTopLeft() {
    for (int x=0; x<mapWidth; x++) {
      for (int y=0; y<mapWidth; y++) {
        if (tiles[x][y]==null) {
          flipTilesAround(x, y);
        }
      }
    }
  }
  void flipTilesAndNeighbors(ArrayList<TileLoc> locs) {
    for (TileLoc loc : locs) {
      if (isWithinMap(loc)) {
        tiles[loc.x][loc.y] = null;
      }
    }
    for (TileLoc loc : locs) {
      if (isWithinMap(loc)) {
        placeTileAt(loc.x, loc.y);
      }
    }
  }
  void placeTileAt(int x, int y) {
    int ex = x;//(int)random(mapWidth);
    int why = y;//(int)random(mapWidth);
    if (tiles[ex][why] == null) {
      ArrayList<Tile> options = validTilesAt(x, y);
      Tile tile=null;
      if (options.size()>0) {
        tile =  getRandomChoice(options);
      }
      tiles[ex][why] = tile;
    }
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
      toReset.add((int)random(1,3), new TileLoc(x, y));
      toReset.add(2, new TileLoc(x, y));

    } else {
      toReset.add(3, new TileLoc(x, y));
    }
    flipTilesAndNeighbors(toReset);
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
      return tile.isValidNeighbor(tiles[neighborX][neighborY], direction);
    }
  }
}

