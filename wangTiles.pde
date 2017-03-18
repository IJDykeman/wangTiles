import java.util.Collections;
import java.util.*;

Map map;
boolean showLines = false;

int tileWidth = 9;
int sphereWidth = 5;
int mapWidth = 64;
//String FILENAME = "wangTiles_adjusted_for_wave.png";
String FILENAME = "dungeon.png";
//String FILENAME = "wangTiles_classic.png";
ArrayList<Tile> wangTiles;
PImage tilesImage;
HashMap<Tile, Integer> tileToNum= new HashMap<Tile, Integer>();

void setup() {
  tilesImage = loadImage(FILENAME);
  wangTiles = parseTilesIntoSet();
  for (int i = 0; i < wangTiles.size(); i++){
    tileToNum.put(wangTiles.get(i),i);
  }
  frameRate(100);
  final int windowWidth = tileWidth * mapWidth;
  size(windowWidth, windowWidth);
  noSmooth();
  resetMap();
  background(0);

}

void checkForUpdatedTileImage(){
  if (!imagesEqual(loadImage(FILENAME), tilesImage)) {
    resetMap();
  }
}



void resetMap(){
  map = new WaveCollapseMap(mapWidth,tileWidth);
//  map = new ConstrainedMap(mapWidth,tileWidth);

}

void mouseDown(){
}

Integer frames = 1;
void draw() {
  checkForUpdatedTileImage();
  if(mousePressed){
    TileLoc mouse = new TileLoc(mouseX /  tileWidth, mouseY /  tileWidth);
    if(map.isWithinMap(mouse)){
      map.updateAtLocation(mouse);
    }
  }
  else{
    map.update();
  }


  map.draw();
  if (showLines) {
    map.drawGrid();
  }
//  save(frames.toString() + ".png");
  frames++;
}

void keyPressed() {
  if (key == 'L' || key =='l') {
    showLines = !showLines;
  } else {
    //resetMap();
  }
}



void mouseClicked() {
  int x=mouseX/tileWidth;
  int y=mouseY/tileWidth;
  //map.flipTilesAround(x, y);
}
