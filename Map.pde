class Map {
  Tile[][] tiles;
  int tileWidth;
  int mapWidth;

  ArrayList<Tile> wangTiles;
  PImage tilesImage;
  int timeSinceMapBuild =0;

  Map(int imapWidth, int itileWidth) {
    tilesImage = loadImage(FILENAME);
    mapWidth = imapWidth;
    tileWidth = itileWidth;
    timeSinceMapBuild = 0; //reset so that this map's processing time counts from 0
    wangTiles = parseTilesIntoSet();
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
      flipTopLeft(timeSinceMapBuild>7);
    }
    timeSinceMapBuild++;
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
  void flipTilesAround(int x, int y, boolean aggressive) {
    ArrayList<TileLoc> toReset = new ArrayList<TileLoc>();
    if (aggressive) {
      //toReset.add(new TileLoc(x-1, y-1));
      //toReset.add(new TileLoc(x+1, y+1));
    }
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
    flipTilesAndNeighbors(toReset);
  }
  void drawGrid() {
    for (int x=0; x<mapWidth; x++) {
      line(tileWidth*x, 0, tileWidth*x, height);
    }
    for (int y=0; y<mapWidth; y++) {
      line(0, tileWidth*y, width, tileWidth*y);
    }
  }

  void draw() {
    for (int x=0; x<mapWidth; x++) {
      for (int y=0; y<mapWidth; y++) {
        if (tiles[x][y] != null) {
          tiles[x][y].draw(x, y);
        } else {
          fill(0, 100, 0, 100);
          rect(x*tileWidth, y*tileWidth, tileWidth, tileWidth);
        }
      }
    }
  }

  void flipTopLeft(boolean aggressive) {
    for (int x=0; x<mapWidth; x++) {
      for (int y=0; y<mapWidth; y++) {
        if (tiles[x][y]==null) {
          flipTilesAround(x, y, false);
        }
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

