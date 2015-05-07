class ScoredMap extends Map {

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
      placeTileAt((int)test.x, (int)test.y);
    }
  }

  void placeTileAt(int x, int y) {
    int ex = x;//(int)random(mapWidth);
    int why = y;//(int)random(mapWidth);
    if (tiles[ex][why] == null) {
      Tile tile=null;

      tile =  getRandomChoice(wangTiles);
      tiles[ex][why] = tile;
    }
  }

  void update() {
    text(mapScore(), 20, 20);
  }

  float mapScore() {
    float result = 0;
    for (int x=0; x<mapWidth; x++) {
      for (int y=0; y<mapWidth; y++) {
        result += placementScore(tiles[x][y],x,y);
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

