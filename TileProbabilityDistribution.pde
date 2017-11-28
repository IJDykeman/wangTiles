class TileProbabilityDistribution{
  Random rand = new Random();
//  HashMap<Tile, Double> logits = new HashMap<Tile, Double>();
  double[] probabilities = new double[wangTiles.size()];
  
  TileProbabilityDistribution(double[] _probabilities){
    probabilities = _probabilities;
  }
  
  double ENTROPY_INVALID = -348273498;
  
  double entropyCached = ENTROPY_INVALID;
  
  TileProbabilityDistribution(double uniform){
    for (int i = 0; i < wangTiles.size(); i++){
      probabilities[i] = (double)Math.log(uniform);
    }
  }
  
  void printDist(){
    println("Distribution:");
    for (double p : probabilities){
      print("  ");
      println(Math.exp(p));
    }
  }
  
  double getTotalProbability(){
    double sum = 0;
    for (double p : probabilities){
      sum += Math.exp(p);
    }
    return sum;
  }
  
  Tile highestProbabilityTile(){
    double highest = -1;
    int best = 0;
    double p;
    for (int i = 0; i < wangTiles.size(); i++){
      p = probabilities[i];
      if (p > highest){
        highest = p;
        best = i;
      }
      
    }
    return wangTiles.get(best);
  }
  
  Tile weightedTileSelect(){
    double r = rand.nextFloat();
    double p;
    assert(r <= 1);
    for (int i = 0; i < wangTiles.size(); i++){
      p = (double)Math.exp(probabilities[i]);
      r-=p;
      if (r <= 0){
        return wangTiles.get(i);
      }
      
    }
    return null;
  }
  
  void normalize(){
    double sum =  getTotalProbability();
    assert(sum > 0);
    for (int i = 0; i < probabilities.length; i++){
      probabilities[i] = probabilities[i] - (double)Math.log(sum);
    }
    invalidateEntropyCache();
  }
  
  double getProbability(Tile tile){
//    println(tile);
//    println(logits);
    assert(tile != null);
    return (double)Math.exp(probabilities[tileToNum.get(tile)]);
  }
  
  void setProbability(Tile tile, double val){
    probabilities[tileToNum.get(tile)] = (double)Math.log(val);
    invalidateEntropyCache();
  }
  
  void invalidateEntropyCache(){
    entropyCached = ENTROPY_INVALID;
  }
  
  double entropy(){
    if (entropyCached != ENTROPY_INVALID){
      return entropyCached;
    }
    return calcEntropy();
  }
  
  double calcEntropy(){
    double sum = 0;
    for (double p : probabilities){
      if (p != 0){
        sum += p * Math.exp(p);
      }
    }
    entropyCached = -sum;
    return entropyCached;
  }
  
  void multiply(TileProbabilityDistribution a){
    for (int i = 0; i < a.probabilities.length; i++){
      probabilities[i] = (a.probabilities[i] + probabilities[i]);
    }
    invalidateEntropyCache();
  }
  
  void add(TileProbabilityDistribution a){
    for (int i = 0; i < a.probabilities.length; i++){
      probabilities[i] = (double)(Math.log(Math.exp(a.probabilities[i]) + Math.exp(probabilities[i])));
    }
    invalidateEntropyCache();
  }
    
}

TileProbabilityDistribution multiply(TileProbabilityDistribution a, TileProbabilityDistribution b){
  double[] probabilities = new double[wangTiles.size()];
  for (int i = 0; i < a.probabilities.length; i++){
    probabilities[i] = (a.probabilities[i] + b.probabilities[i]);
  }
  return new TileProbabilityDistribution(probabilities);
}

TileProbabilityDistribution add(TileProbabilityDistribution a, TileProbabilityDistribution b){
  double[] probabilities = new double[wangTiles.size()];
  for (int i = 0; i < a.probabilities.length; i++){
    probabilities[i] = (double)(Math.log(Math.exp(a.probabilities[i]) + Math.exp(b.probabilities[i])));
  }
  return new TileProbabilityDistribution(probabilities);
}






class TileProbabilitySphere extends Map{
  TileProbabilityDistribution[][] tileDistributions;
  Tile centralTile;
  
  TileProbabilitySphere(Tile _centralTile){
    
    mapWidth = sphereWidth;
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
      TileProbabilityDistribution result = new TileProbabilityDistribution((double)1);
      result.normalize();
      return result;
    }
      
  }
  
  TileProbabilityDistribution calcDistAt(TileLoc loc){
    if(loc.x == mapWidth/2 && loc.y == mapWidth/2){
      TileProbabilityDistribution result = new TileProbabilityDistribution((double)0.0000001);
      result.setProbability(centralTile, (double)1);
      result.normalize();
      return result; 
    }
    TileProbabilityDistribution result = new TileProbabilityDistribution((double)0.0000001);
    for (TileLoc neighbor : getNeighbors(loc)){
      if(tileDistributions[neighbor.x][neighbor.y] != null){
        TileProbabilityDistribution dist = transitionDistribution(neighbor, loc);
        result.add(dist);
      }

    } 
    result.normalize();
    return result;
  }
  
  TileProbabilityDistribution transitionDistribution(TileLoc from, TileLoc to){

    Tile tileFrom;
    Tile tileTo;
    double[] probabilities = new double[wangTiles.size()]; 
    for (int i = 0; i < wangTiles.size(); i++){
      tileTo = wangTiles.get(i);
      double p = (double)0;
      for (int j = 0; j < wangTiles.size(); j++){
        tileFrom = wangTiles.get(j);
        double valid = isValidNeighbor(tileTo, to.x, to.y, tileFrom, from.x, from.y) ? (double)1 : (double)0;
        
        p += tileDistributions[from.x][from.y].getProbability(tileFrom) * valid;
      }
      probabilities[i] = (double)Math.log(p);
    }

    return new TileProbabilityDistribution(probabilities);
  }
  

  
  
}