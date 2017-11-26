class WaveCollapseMap extends Map {
  TileProbabilityDistribution[][] tileDistributions;
  HashMap<Tile, TileProbabilitySphere> spheres;
  boolean[][] screenValid;
  double[] priorTileProbabilities;
  int numInitialPlacements = 190;
  Random rand = new Random();
  ArrayList<TileLoc> tileLocs = new ArrayList<TileLoc>();
  
  
  WaveCollapseMap(int imapWidth, int itileWidth) {


    mapWidth = imapWidth;
    tileWidth = itileWidth;
    timeSinceMapBuild = 0; //reset so that this map's processing time counts from 0
    //normalizeTileLikelyhoods(wangTiles);
    tiles = new Tile[mapWidth][mapWidth];
    tileDistributions = new TileProbabilityDistribution[mapWidth][mapWidth];
    screenValid = new boolean[mapWidth][mapWidth];
    
    priorTileProbabilities = new double[wangTiles.size()];
    for (int i = 0; i < wangTiles.size(); i++){
      priorTileProbabilities[i] = (double)Math.log(max(1, wangTiles.get(i).likelyhood )/ 255.0);
      println(wangTiles.get(i).likelyhood);
    }

    for (int x=0; x<mapWidth; x++) {
      for (int y=0; y<mapWidth; y++) {
        tileDistributions[x][y] = new TileProbabilityDistribution(priorTileProbabilities.clone());
//        tileDistributions[x][y] = new TileProbabilityDistribution(1d);
        tileDistributions[x][y].normalize();
        screenValid[x][y]=true;
      }
    }
    
    spheres = new HashMap<Tile, TileProbabilitySphere>();
    print("we have "); print(wangTiles.size()); println(" Wang tiles."); 
    print("initializing spheres ");
    ArrayList<TileProbabilitySphere> allSpheres = new ArrayList<TileProbabilitySphere>(getSpheres());
    for (int i =0; i< wangTiles.size(); i++){
      //spheres.put(wangTiles.get(i), new TileProbabilitySphere(wangTiles.get(i))); 
      spheres.put(wangTiles.get(i), allSpheres.get(i));
    }
    println(" done.");
    
    
    for (int x=0; x<mapWidth; x++) {
      for (int y=0; y<mapWidth; y++) {
        tileLocs.add(new TileLoc(x, y));
      }
    }
    
    ArrayList<TileLoc> RandomTileLocs = new ArrayList<TileLoc>(tileLocs);
    Collections.shuffle(RandomTileLocs);
    for (int i =0; i< numInitialPlacements; i++){
      TileLoc test = RandomTileLocs.get(i);
      placeTileAt(test.x, test.y);
    }
    println("finished map constructor.");
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
  
  void updateAtLocation(TileLoc loc){
      TileLoc nextChoice = loc;
      if (nextChoice != null){
        Tile tileToPlace = tileDistributions[nextChoice.x][nextChoice.y].weightedTileSelect();
        multiplyInRectifiedTile(tileToPlace, nextChoice);
      }
  }

  void update() {
//    println("entropy:");
//    printEntropy();
//    println("sums:");
//    printSums();
    int numIterations = 1;
    if (timeSinceMapBuild>0) {
      numIterations = 20;
    }
    println(timeSinceMapBuild);
    // if the simulation has been running a long time,
    // up the amount of modification done per frame.
    for (int i=0; i<numIterations; i++) {
//      flipTopLeft();
      TileLoc nextChoice = lowestEntopy();
      if (nextChoice != null){
        Tile tileToPlace = tileDistributions[nextChoice.x][nextChoice.y].weightedTileSelect();
        multiplyInRectifiedTile(tileToPlace, nextChoice);
        

        //print("tile location placed: "); print((nextChoice.x)); print("  ");println((nextChoice.y));
      }
      else{
        delay(100000);
      }
    }

    timeSinceMapBuild++;
  }

  void multiplyInRectifiedTile(Tile tileToPlace, TileLoc loc){
    if(tiles[loc.x][loc.y] != null){
      return;
    }
    TileProbabilitySphere sphere = spheres.get(tileToPlace);
    TileLoc editing = new TileLoc(0,0);
    for (int x=  max(loc.x - sphereWidth/2-1,0); x < min(loc.x  + sphereWidth/2+1, mapWidth) ; x++) {
      for (int y=max(loc.y - sphereWidth/2-1,0); y < min(loc.y  + sphereWidth/2+1, mapWidth); y++) {
        editing.x = x - loc.x + (sphereWidth-1);
        editing.y = y - loc.y + (sphereWidth-1);
        tileDistributions[x][y].add(sphere.getDistributionAt(editing));
        tileDistributions[x][y].normalize();
        screenValid[x][y] = false;
      }
    }
    tiles[loc.x][loc.y] = tileToPlace;
    
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
//    ArrayList<Double> entropies = new ArrayList<Double>();
//    double sum = 0;
//    for (TileLoc loc : tileLocs){
//      double entropy = tileDistributions[loc.x][loc.y].entropy();
//      sum += entropy;
//      entropies.add(entropy);
//    }
//    
//    double psum = 0;
//    for (int i = 0; i<entropies.size();i++){
//      double p = entropies.get(i) / sum;
//      entropies.set(i, p);
//      psum += p;
//    }
//    
//    for (int i = 0; i<entropies.size();i++){
//      entropies.set(i, entropies.get(i) / psum);
//    }
//    
//    double r = rand.nextFloat();
//    assert(r <= 1);
//    for (int i = 0; i < entropies.size(); i++){
//      double p = entropies.get(i);
//      r-=p;
//      if (r <= 0){
//        return tileLocs.get(i);
//      }
//  }
//  return null;
  }
  
 
  void placeTileAt(int x, int y) {
    int ex = x;//(int)random(mapWidth);
    int why = y;//(int)random(mapWidth);
    if (tiles[ex][why] == null) {
      Tile tileToPlace = tileDistributions[ex][why].weightedTileSelect();
      multiplyInRectifiedTile(tileToPlace, new TileLoc(ex,why));
    }
    
  }

  void draw() {
    println("drawing...");
    for (int x=0; x<mapWidth; x++) {
      for (int y=0; y<mapWidth; y++) {
        if (!screenValid[x][y]){
          fill(0);
          noStroke();
          rect(x*tileWidth, y*tileWidth, tileWidth, tileWidth);
          if (tiles[x][y] != null) {
            tint(255,(int)255);
            tiles[x][y].draw(x, y);
            
          } 
          else {
            
            for (Tile tile : wangTiles){        
              double p = tileDistributions[x][y].getProbability(tile);
//              if(p > 1.0 / wangTilkes.size()){
                tint(255,(int)(255*p));

                tile.draw(x, y);
                
//              }
            }
          }
          screenValid[x][y] = true;
        }
      }
    }
    println("done.");
  }
  

}