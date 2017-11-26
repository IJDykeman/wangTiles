

class Map {
  Tile[][] tiles;
  int tileWidth;
  int mapWidth;


  int timeSinceMapBuild = 0;

  void updateAtLocation(TileLoc loc){
  }
  
  void update() {
  }

  Tile[][] getTilesCopy() {
    Tile[][] copy = new Tile[mapWidth][mapWidth];
      for (int x=0; x<mapWidth; x++) {
        for (int y=0; y<mapWidth; y++) {
          copy[x][y] = tiles[x][y];
        }
    }
    return copy;
  }

  void drawGrid() {
    for (int x=0; x<mapWidth; x++) {
      line(tileWidth*x, 0, tileWidth*x, height);
    }
    for (int y=0; y<mapWidth; y++) {
      line(0, tileWidth*y, width, tileWidth*y);
    }
  }

  boolean isWithinMap(TileLoc loc) {
    return loc.x<mapWidth && loc.x >= 0 && loc.y<mapWidth && loc.y >= 0;
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
  
  ArrayList<TileLoc> getTilesInRandomOrder(){
   ArrayList<TileLoc> tileLocs = new ArrayList<TileLoc>();
    for (int x=0; x<mapWidth; x++) {
      for (int y=0; y<mapWidth; y++) {
        tileLocs.add(new TileLoc(x, y));
      }
    }
    Collections.shuffle(tileLocs);
    return tileLocs; 
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

  boolean tileListContains(ArrayList<TileLoc> l, TileLoc t){
    for(TileLoc o : l){
      if(o.x == t.x && o.y == t.y){
        return true;
      }
    }
    return false;
  }

  ArrayList<TileLoc> BfsFrom(TileLoc startLoc){
//    println("up");
    ArrayList<TileLoc> queue = new ArrayList<TileLoc>();
    ArrayList<TileLoc> visited = new ArrayList<TileLoc>();
//    HashSet<TileLoc> visited = new HashSet<TileLoc>();
    queue.add(startLoc);
    while (queue.size() > 0){
      TileLoc current = queue.remove(0);
      visited.add(current);
      queue.remove(current);
      for (TileLoc neighbor : getNeighbors(current)){
        if (! tileListContains(visited, neighbor)){
          queue.add(neighbor);
        }
      }
    } 
    assert(visited.size() == mapWidth * mapWidth);
    print (".");
    return visited;
  }
  
  ArrayList<TileLoc> getNeighbors(TileLoc from){
    ArrayList<TileLoc> results = new ArrayList<TileLoc>(); 
    if (from.x < mapWidth - 1){
      results.add(new TileLoc(from.x + 1, from.y));
    }
    if (from.x >= 1){
      results.add(new TileLoc(from.x - 1, from.y));
    }
    if (from.y < mapWidth - 1){
      results.add(new TileLoc(from.x, from.y + 1));
    }
    if (from.y >= 1){
      results.add(new TileLoc(from.x, from.y - 1));
    }
    return results;
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
  
  boolean isValidNeighbor(Tile tile, int tileX, int tileY, Tile neighbor, int neighborX, int neighborY) {
    if (neighborX>=mapWidth || neighborY>=mapWidth || neighborX<0 || neighborY<0) {
      return true;
    } else {
      Directions direction = getDirectionFromDelta(neighborX-tileX, neighborY-tileY);             
      return tile.isValidNeighbor(neighbor, direction);
    }
  }
}