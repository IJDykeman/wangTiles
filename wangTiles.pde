import java.util.Collections;

Tile[][] map;
int tileWidth = 6;
int mapWidth = 130;
boolean showLines = false;
ArrayList<Tile> wangTiles;
PImage tilesImage;
int timeSinceMapBuild =0;

void setup() {

  frameRate(10000);



  size(mapWidth*tileWidth, mapWidth*tileWidth);
  smooth();
  buildMap();

}

void buildMap() {
  timeSinceMapBuild = 0;
  wangTiles = parseTilesIntoSet();
  map = new Tile[mapWidth][mapWidth];

  
  ArrayList<PVector> tileLocs = new ArrayList<PVector>();
  for (int x=0; x<mapWidth; x++) {
    for (int y=0; y<mapWidth; y++) {
      tileLocs.add(new PVector(x,y));
    }
  }
  Collections.shuffle(tileLocs);
  for(PVector test:tileLocs){
    placeTileAt((int)test.x, (int)test.y);
  }
}

ArrayList<Tile> parseTilesIntoSet(){
  ArrayList<Tile> result= new ArrayList<Tile>();
  tilesImage = loadImage("wangTiles.png");
  if (tilesImage == null) {
    return result;
  }
  color black = color(0,0,0);
  for (int x=0; x< (tilesImage.width-3)/4+1; x++) {
    for (int y=0; y< (tilesImage.height-3)/4+1; y++) {
      PImage image = tilesImage.get(x*4, y*4, 3, 3);
      int likelyhood = (int)pow(255-(int)red(tilesImage.get(x*4, y*4+3)),1);
      if (!( new Tile(image,likelyhood).isAllWhite()) && ((int)tilesImage.get(x*4+1, y*4+3) != color(255,0,0)))
      {
        result.add(new Tile(image, likelyhood));
        if(tilesImage.get(x*4+3,y*4)==black){
          Tile rotation1 = new Tile( get90DegClockwiseRotation(image), likelyhood);
          Tile rotation2 = new Tile( get90DegClockwiseRotation(rotation1.image), likelyhood);
          Tile rotation3 = new Tile( get90DegClockwiseRotation(rotation2.image), likelyhood);
          result.add(rotation1);
          result.add(rotation2);
          result.add(rotation3);
          print("added one");
        }
      }
    }
  }
  
  return result;
}



void draw() {
  
  smooth();
  if (!imagesEqual(loadImage("wangTiles.png"), tilesImage)) {
    buildMap();
  }

  background(0);
  for (int x=0; x<mapWidth; x++) {
    for (int y=0; y<mapWidth; y++) {
      if (map[x][y] != null) {
        map[x][y].draw(x, y);
      } else {
        fill(0, 100, 0, 100);
        rect(x*tileWidth, y*tileWidth, tileWidth, tileWidth);
      }
    }
  }
  if (showLines) {
    for (int x=0; x<mapWidth; x++) {
      line(tileWidth*x, 0, tileWidth*x, height);
    }
    for (int y=0; y<mapWidth; y++) {
      line(0, tileWidth*y, width, tileWidth*y);
    }
  }
  
  int numIterations = 1;
  if(timeSinceMapBuild>10){
    numIterations = 20;
  }
  for(int i=0;i<numIterations;i++){
    flipTopLeft(timeSinceMapBuild>7);
  }
  timeSinceMapBuild++;
  
  /*background(255);
  for(int i=0;i<wangTiles.size();i++){
    image (wangTiles.get(i),60*(i%11),60*(i-i%11)/11,50,50);
  }*/
}


void keyPressed() {
  if (key == 'L' || key =='l') {
    showLines = !showLines;
  } else {
    buildMap();
  }
}

void flipTilesAndNeighbors(ArrayList<TileLoc> locs) {
  for (TileLoc loc : locs) {
    if (isWithinMap(loc)) {
      map[loc.x][loc.y] = null;
    }
  }
  for (TileLoc loc : locs) {
    if (isWithinMap(loc)) {
      placeTileAt(loc.x, loc.y);
    }
  }
}



void mouseClicked() {
  int x=mouseX/tileWidth;
  int y=mouseY/tileWidth;
  flipTilesAround(x, y,false);
}


