class WaveCollapseMap extends Map {
  TileProbabilityDistribution[][] tileDistributions;
  HashMap<Tile, TileProbabilitySphere> spheres;

  WaveCollapseMap(int imapWidth, int itileWidth) {


    mapWidth = imapWidth;
    tileWidth = itileWidth;
    timeSinceMapBuild = 0; //reset so that this map's processing time counts from 0
    //normalizeTileLikelyhoods(wangTiles);
    tiles = new Tile[mapWidth][mapWidth];
    tileDistributions = new TileProbabilityDistribution[mapWidth][mapWidth];
    for (int x=0; x<mapWidth; x++) {
      for (int y=0; y<mapWidth; y++) {
        tileDistributions[x][y] = new TileProbabilityDistribution(1d);
        tileDistributions[x][y].normalize();
      }
    }
    
    spheres = new HashMap<Tile, TileProbabilitySphere>();
    println("initializing spheres...");
    for (Tile tile : wangTiles){
      spheres.put(tile, new TileProbabilitySphere(tile, wangTiles)); 
    }
    println("    done.");
  }
  



  void printEntropy(){
    for (int x=0; x<mapWidth; x++) {
      for (int y=0; y<mapWidth; y++) {
        print(tileDistributions[x][y].entropy());
        print(" ");
      }
      println("");
    }
  }
  
  void printSums(){
    for (int x=0; x<mapWidth; x++) {
      for (int y=0; y<mapWidth; y++) {
        print(tileDistributions[x][y].getTotalProbability());
        print(" ");
      }
      println("");
    }
  }

  void update() {
//    println("entropy:");
//    printEntropy();
//    println("sums:");
//    printSums();
    int numIterations = 1;
    if (timeSinceMapBuild>7) {
      numIterations = 10;
    }
    println(timeSinceMapBuild);
    // if the simulation has been running a long time,
    // up the amount of modification done per frame.
    for (int i=0; i<numIterations; i++) {
//      flipTopLeft();
      TileLoc nextChoice = lowestEntopy();
      Tile tileToPlace = tileDistributions[nextChoice.x][nextChoice.y].weightedTileSelect();
      tiles[nextChoice.x][nextChoice.y] = tileToPlace;
      multiplyInRectifiedTile(spheres.get(tileToPlace), nextChoice);
      print("tile location placed: "); print((nextChoice.x)); print("  ");println((nextChoice.y));
      
    }

    timeSinceMapBuild++;
  }

  void multiplyInRectifiedTile(TileProbabilitySphere sphere, TileLoc loc){
    for (int x=0; x < mapWidth; x++) {
      for (int y=0; y < mapWidth; y++) {
        tileDistributions[x][y] = multiply(tileDistributions[x][y], sphere.getDistributionAt(new TileLoc(x - loc.x + 9, y - loc.y + 9)));
        tileDistributions[x][y].normalize();
      }
    }
  }
  
  TileLoc lowestEntopy(){
    double lowest = 10113034;
    TileLoc best = null;//new TileLoc(0,0);
    for (int x=0; x<mapWidth; x++) {
      for (int y=0; y<mapWidth; y++) {
        if (tileDistributions[x][y].entropy() < lowest && tiles[x][y] == null){
          lowest = tileDistributions[x][y].entropy();
          best = new TileLoc(x,y);
        }
      }
    }
    return best;
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

  void draw() {
    for (int x=0; x<mapWidth; x++) {
      for (int y=0; y<mapWidth; y++) {
        if (tiles[x][y] != null) {
          tiles[x][y].draw(x, y);
        } else {
          for (Tile tile : wangTiles){        
            double p = tileDistributions[x][y].getProbability(tile);
            tint(255,(int)(255*p));
            tile.draw(x, y);
            tint(255,(int)255*1);

          }
        }
      }
    }
  }
  

}

