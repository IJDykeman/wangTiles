class TileProbabilityDistribution{
  Random rand = new Random();
  HashMap<Tile, Double> logits = new HashMap<Tile, Double>();
  
  TileProbabilityDistribution(ArrayList<Tile> tiles, ArrayList<Double> probabilities){
    for (int i = 0; i < tiles.size(); i++){
      logits.put(tiles.get(i), probabilities.get(i));
    }
  }
  
  TileProbabilityDistribution(ArrayList<Tile> tiles, double uniform){
    for (int i = 0; i < tiles.size(); i++){
      logits.put(tiles.get(i), uniform);
    }
  }
  
  TileProbabilityDistribution(HashMap<Tile, Double> _logits){
    logits = _logits;
  }
  
  void printDist(){
    println("Distribution:");
    for (Tile tile : logits.keySet()){
      print("  ");
      println(logits.get(tile));
    }
  }
  
  float getTotalProbability(){
    float sum = 0;
    for (Tile tile : logits.keySet()){
      sum += logits.get(tile);
    }
    return sum;
  }
  
  Tile highestProbabilityTile(){
    double highest = -1;
    Tile best = null;
    for (Tile tile : logits.keySet()){
      double p = logits.get(tile);
      if (p > highest){
        highest = p;
        best = tile;
      }
      
    }
    return best;
  }
  
  Tile weightedTileSelect(){
    double r = rand.nextFloat();
    assert(r <= 1);
    for (Tile tile : logits.keySet()){
      double p = logits.get(tile);
      r-=p;
      if (r <= 0){
        return tile;
      }
      
    }
    return null;
  }
  
  void normalize(){
    float sum =  getTotalProbability();
    assert(sum > 0);
    for (Tile tile : logits.keySet()){
      logits.put(tile, logits.get(tile) / sum);
    }
  }
  
  double getProbability(Tile tile){
//    println(tile);
//    println(logits);
    assert(logits != null);
    assert(tile != null);
    return logits.get(tile);
  }
  
  double setProbability(Tile tile, double val){
    return logits.put(tile, val);
  }
  
  double entropy(){
    double sum = 0;
    for (Tile tile : logits.keySet()){
      if(logits.get(tile) != 0){
        sum += logits.get(tile)*Math.log(logits.get(tile));
      }
    }
    return -sum;
  }
    
}

TileProbabilityDistribution multiply(TileProbabilityDistribution a, TileProbabilityDistribution b){
  HashMap<Tile, Double> result = new HashMap<Tile, Double>();
  for (Tile tile : a.logits.keySet()){
    result.put(tile, a.getProbability(tile) * b.getProbability(tile));
  }
  return new TileProbabilityDistribution(result);
}

TileProbabilityDistribution add(TileProbabilityDistribution a, TileProbabilityDistribution b){
  HashMap<Tile, Double> result = new HashMap<Tile, Double>();
  for (Tile tile : a.logits.keySet()){
    result.put(tile, a.getProbability(tile) + b.getProbability(tile));
  }
  return new TileProbabilityDistribution(result);
}






class TileProbabilitySphere extends Map{
  TileProbabilityDistribution[][] tileDistributions;
  Tile centralTile;
  
  TileProbabilitySphere(Tile _centralTile, ArrayList<Tile> _wangTiles){
    
    wangTiles = _wangTiles;
    mapWidth = 9;
    tileDistributions = new TileProbabilityDistribution[mapWidth][mapWidth];
    centralTile = _centralTile;
//    tiles[tileWidth/2][tileWidth/2] = centralTile;
    for (TileLoc cur : BfsFrom(new TileLoc(mapWidth/2,mapWidth/2))){
      tileDistributions[cur.x][cur.y] = calcDistAt(cur);
//      print(cur.x); print(" "); println(cur.y);
//      tileDistributions[cur.x][cur.y].printDist();
//      delay(400);
    }
    
  }
  
  TileProbabilityDistribution getDistributionAt(TileLoc loc){
    loc.x = loc.x - mapWidth / 2;
    loc.y = loc.y - mapWidth / 2;
    if (loc.x < mapWidth && loc.y < mapWidth && loc.x >= 0 && loc.y >=0 ){
      return tileDistributions[loc.x][loc.y];
    }
    else{
      TileProbabilityDistribution result = new TileProbabilityDistribution(wangTiles, 1d);
      result.normalize();
      return result;
    }
      
  }
  
  TileProbabilityDistribution calcDistAt(TileLoc loc){
    if(loc.x == mapWidth/2 && loc.y == mapWidth/2){
      TileProbabilityDistribution result = new TileProbabilityDistribution(wangTiles, 0d);
      result.setProbability(centralTile, 1d);
      return result; 
    }
    TileProbabilityDistribution result = new TileProbabilityDistribution(wangTiles, 0.000001d);
    for (TileLoc neighbor : getNeighbors(loc)){
      if(tileDistributions[neighbor.x][neighbor.y] != null){
        TileProbabilityDistribution dist = transitionDistribution(neighbor, loc);
        result = add(result, dist);
      }
      else{
//        result = add(result, new TileProbabilityDistribution(wangTiles, 1d));
      }
    } 
    result.normalize();
    return result;
  }
  
  TileProbabilityDistribution transitionDistribution(TileLoc from, TileLoc to){
//      println("getting trans dist...");

    ArrayList<Double> probabilities = new ArrayList<Double>(); 
    for (Tile tileTo : wangTiles){
      double p = 0d;
      for (Tile tileFrom : wangTiles){
        double valid = isValidNeighbor(tileTo, to.x, to.y, tileFrom, from.x, from.y) ? 1d : 0d;
        
        p += tileDistributions[from.x][from.y].getProbability(tileFrom) * valid;
      }
      probabilities.add(p);
    }
//    println("got trans dist");
    return new TileProbabilityDistribution(wangTiles, probabilities);
  }
  

  
  
}
