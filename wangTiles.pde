import java.util.Collections;
import java.util.*;

Map map;
boolean showLines = false;

int tileWidth = 16;
int sphereWidth = 9;
int mapWidth = 35;
String FILENAME = "wangTiles.png";
ArrayList<Tile> wangTiles;
PImage tilesImage;
HashMap<Tile, Integer> tileToNum= new HashMap<Tile, Integer>();

void setup() {
  tilesImage = loadImage(FILENAME);
  wangTiles = parseTilesIntoSet();
  for (int i = 0; i < wangTiles.size(); i++){
    tileToNum.put(wangTiles.get(i),i);
  }
  frameRate(10);
  final int windowWidth = tileWidth * mapWidth;
  size(windowWidth, windowWidth);
  noSmooth();
  resetMap();

}

void checkForUpdatedTileImage(){
  if (!imagesEqual(loadImage(FILENAME), tilesImage)) {
    resetMap();
  }
}



void resetMap(){
  map = new WaveCollapseMap(mapWidth,tileWidth);
}


void draw() {
  checkForUpdatedTileImage();
    map.update();

  background(0);
  map.draw();
  if (showLines) {
    map.drawGrid();
  }
}

void keyPressed() {
  if (key == 'L' || key =='l') {
    showLines = !showLines;
  } else {
    resetMap();
  }
}



void mouseClicked() {
  int x=mouseX/tileWidth;
  int y=mouseY/tileWidth;
  //map.flipTilesAround(x, y);
}
