class TileProbabilityDistribution{
  Random rand = new Random();
//  HashMap<Tile, Double> logits = new HashMap<Tile, Double>();
  double[] probabilities = new double[wangTiles.size()];
  
  TileProbabilityDistribution(double[] _probabilities){
    probabilities = _probabilities;
  }
  
  TileProbabilityDistribution(double uniform){
    for (int i = 0; i < wangTiles.size(); i++){
      probabilities[i] = uniform;
    }
  }
  
  void printDist(){
    println("Distribution:");
    for (double p : probabilities){
      print("  ");
      println(p);
    }
  }
  
  float getTotalProbability(){
    float sum = 0;
    for (double p : probabilities){
      sum += p;
    }
    return sum;
  }
  
  Tile highestProbabilityTile(){
    double highest = -1;
    int best = 0;
    for (int i = 0; i < wangTiles.size(); i++){
      double p = probabilities[i];
      if (p > highest){
        highest = p;
        best = i;
      }
      
    }
    return wangTiles.get(best);
  }
  
  Tile weightedTileSelect(){
    double r = rand.nextFloat();
    assert(r <= 1);
    for (int i = 0; i < wangTiles.size(); i++){
      double p = probabilities[i];
      r-=p;
      if (r <= 0){
        return wangTiles.get(i);
      }
      
    }
    return null;
  }
  
  void normalize(){
    float sum =  getTotalProbability();
    assert(sum > 0);
    for (int i = 0; i < probabilities.length; i++){
      probabilities[i] = probabilities[i] / sum;
    }
  }
  
  double getProbability(Tile tile){
//    println(tile);
//    println(logits);
    assert(tile != null);
    return probabilities[tileToNum.get(tile)];
  }
  
  void setProbability(Tile tile, double val){
    probabilities[tileToNum.get(tile)] = val;
  }
  
  double entropy(){
    double sum = 0;
    for (double p : probabilities){
      if (p != 0){
        sum += p * Math.log(p);
      }
    }
    return -sum;
  }
    
}

TileProbabilityDistribution multiply(TileProbabilityDistribution a, TileProbabilityDistribution b){
  double[] probabilities = new double[wangTiles.size()];
  for (int i = 0; i < a.probabilities.length; i++){
    probabilities[i] = (a.probabilities[i] * b.probabilities[i]);
  }
  return new TileProbabilityDistribution(probabilities);
}

TileProbabilityDistribution add(TileProbabilityDistribution a, TileProbabilityDistribution b){
  double[] probabilities = new double[wangTiles.size()];
  for (int i = 0; i < a.probabilities.length; i++){
    probabilities[i] = (a.probabilities[i] + b.probabilities[i]);
  }
  return new TileProbabilityDistribution(probabilities);
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
      TileProbabilityDistribution result = new TileProbabilityDistribution(1d);
      result.normalize();
      return result;
    }
      
  }
  
  TileProbabilityDistribution calcDistAt(TileLoc loc){
    if(loc.x == mapWidth/2 && loc.y == mapWidth/2){
      TileProbabilityDistribution result = new TileProbabilityDistribution(0d);
      result.setProbability(centralTile, 1d);
      return result; 
    }
    TileProbabilityDistribution result = new TileProbabilityDistribution(0.000001d);
    for (TileLoc neighbor : getNeighbors(loc)){
      if(tileDistributions[neighbor.x][neighbor.y] != null){
        TileProbabilityDistribution dist = transitionDistribution(neighbor, loc);
        result = add(result, dist);
      }

    } 
    result.normalize();
    return result;
  }
  
  TileProbabilityDistribution transitionDistribution(TileLoc from, TileLoc to){
//      println("getting trans dist...");

    double[] probabilities = new double[wangTiles.size()]; 
    for (int i = 0; i < wangTiles.size(); i++){
      Tile tileTo = wangTiles.get(i);
      double p = 0d;
      for (int j = 0; j < wangTiles.size(); j++){
        Tile tileFrom = wangTiles.get(j);
        double valid = isValidNeighbor(tileTo, to.x, to.y, tileFrom, from.x, from.y) ? 1d : 0d;
        
        p += tileDistributions[from.x][from.y].getProbability(tileFrom) * valid;
      }
      probabilities[i] = p;
    }
//    println("got trans dist");
    return new TileProbabilityDistribution(probabilities);
  }
  

  
  
}
