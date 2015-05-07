class ScoredMap extends Map {

  ScoredMap(ScoredMap toCopy) {
    tiles = toCopy.getTilesCopy();
    mapWidth = toCopy.mapWidth;
    tileWidth = toCopy.tileWidth;
    timeSinceMapBuild = 0; //reset so that this map's processing time counts from 0
    wangTiles = toCopy.wangTiles;
  }

  ScoredMap(int imapWidth, int itileWidth) {
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
      placeRandomTileAt((int)test.x, (int)test.y);
    }
  }



  void randomizeRegion (int x1, int y1, int x2, int y2) {
    assert (x1<x2 && y1<y2);
    for (int x = x1; x<x2; x++) {
      for (int y = y1; y<y2; y++) {
        placeRandomTileAt(x,y);
      }
    }
  }
  
  void tryRandomizingRegion(){
    print("hello");
    ScoredMap otherOption = new ScoredMap(this);
    int x = int(random(mapWidth-10));
    int y = int(random(mapWidth-10));
    
    otherOption.randomizeRegion(x,y,x+10,y+10);
    
    if (otherOption.mapScore()>mapScore()){
      tiles = otherOption.tiles;
      print("found a better map");
    }
    
  }

  void update() {
    text(mapScore(), 20, 20);
    tryRandomizingRegion();
  }


  void placeRandomTileAt(int x, int y) {
    int ex = x;//(int)random(mapWidth);
    int why = y;//(int)random(mapWidth);
    Tile tile=null;

    tile =  getRandomChoice(wangTiles);
    tiles[ex][why] = tile;
    
  }

  float mapScore() {
    float result = 0;
    for (int x=0; x<mapWidth; x++) {
      for (int y=0; y<mapWidth; y++) {
        result += placementScore(tiles[x][y], x, y);
      }
    }
    return result;
  }

  float placementScore (Tile tile, int tileX, int tileY) {
    float result =  
      scoreOfNeighbor(tile, tileX, tileY, tileX+1, tileY) *
      scoreOfNeighbor(tile, tileX, tileY, tileX-1, tileY) *
      scoreOfNeighbor(tile, tileX, tileY, tileX, tileY+1) *
      scoreOfNeighbor(tile, tileX, tileY, tileX, tileY-1);

    return result;
  }

  float scoreOfNeighbor(Tile tile, int tileX, int tileY, int neighborX, int neighborY) {
    if (neighborX>=mapWidth || neighborY>=mapWidth || neighborX<0 || neighborY<0) {
      return 1;
    } else {

      Directions direction = getDirectionFromDelta(neighborX-tileX, neighborY-tileY);             
      return tile.edgeFractionInCommonWithNeighbor(tiles[neighborX][neighborY], direction);
    }
  }
}

