class TileProbabilityDistribution{
  Random rand = new Random();
//  HashMap<Tile, Double> logits = new HashMap<Tile, Double>();
  double[] probabilities = new double[wangTiles.size()];
  
  TileProbabilityDistribution(double[] _probabilities){
    probabilities = _probabilities;
  }
  
  TileProbabilityDistribution(double uniform){
    for (int i = 0; i < wangTiles.size(); i++){
      probabilities[i] = Math.log(uniform);
    }
  }
  
  void printDist(){
    println("Distribution:");
    for (double p : probabilities){
      print("  ");
      println(Math.exp(p));
    }
  }
  
  float getTotalProbability(){
    float sum = 0;
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
      p = Math.exp(probabilities[i]);
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
      probabilities[i] = probabilities[i] - Math.log(sum);
    }
  }
  
  double getProbability(Tile tile){
//    println(tile);
//    println(logits);
    assert(tile != null);
    return Math.exp(probabilities[tileToNum.get(tile)]);
  }
  
  void setProbability(Tile tile, double val){
    probabilities[tileToNum.get(tile)] = Math.log(val);
  }
  
  double entropy(){
    double sum = 0;
    for (double p : probabilities){
      if (p != 0){
        sum += p * Math.exp(p);
      }
    }
    return -sum;
  }
  
  void multiply(TileProbabilityDistribution a){
    for (int i = 0; i < a.probabilities.length; i++){
      probabilities[i] = (a.probabilities[i] + probabilities[i]);
    }
  }
  
  void add(TileProbabilityDistribution a){
    for (int i = 0; i < a.probabilities.length; i++){
      probabilities[i] = (Math.log(Math.exp(a.probabilities[i]) + Math.exp(probabilities[i])));
    }
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
    probabilities[i] = (Math.log(Math.exp(a.probabilities[i]) + Math.exp(b.probabilities[i])));
  }
  return new TileProbabilityDistribution(probabilities);
}






class TileProbabilitySphere extends Map{
  TileProbabilityDistribution[][] tileDistributions;
  Tile centralTile;
  
  TileProbabilitySphere(Tile _centralTile, ArrayList<Tile> _wangTiles){
    
    wangTiles = _wangTiles;
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
      TileProbabilityDistribution result = new TileProbabilityDistribution(1d);
      result.normalize();
      return result;
    }
      
  }
  
  TileProbabilityDistribution calcDistAt(TileLoc loc){
    if(loc.x == mapWidth/2 && loc.y == mapWidth/2){
      TileProbabilityDistribution result = new TileProbabilityDistribution(0.0000001d);
      result.setProbability(centralTile, 1d);
      result.normalize();
      return result; 
    }
    TileProbabilityDistribution result = new TileProbabilityDistribution(0.0000001d);
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
//      println("getting trans dist...");
    Tile tileFrom;
    Tile tileTo;
    double[] probabilities = new double[wangTiles.size()]; 
    for (int i = 0; i < wangTiles.size(); i++){
      tileTo = wangTiles.get(i);
      double p = 0d;
      for (int j = 0; j < wangTiles.size(); j++){
        tileFrom = wangTiles.get(j);
        double valid = isValidNeighbor(tileTo, to.x, to.y, tileFrom, from.x, from.y) ? 1d : 0d;
        
        p += tileDistributions[from.x][from.y].getProbability(tileFrom) * valid;// * ((double)(1+tileTo.likelyhood) / 255.0) ;
      }
      probabilities[i] = Math.log(p);
    }
//    println("got trans dist");
    return new TileProbabilityDistribution(probabilities);
  }
  

  
  
}
