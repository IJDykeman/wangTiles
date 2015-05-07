import java.util.Collections;

Map map;
boolean showLines = false;

int tileWidth = 6;
int mapWidth = 130;
String FILENAME = "wangTiles.png";


void setup() {
  frameRate(10000);
  size(mapWidth*tileWidth, mapWidth*tileWidth);
  smooth();
  resetMap();

}

void checkForUpdatedTileImage(){
  if (!imagesEqual(loadImage(FILENAME), map.tilesImage)) {
    resetMap();
  }
}



void resetMap(){
  map = new ScoredMap(mapWidth,tileWidth);
}


void draw() {
  checkForUpdatedTileImage();
  background(0);
  map.draw();
  if (showLines) {
    map.drawGrid();
  }
  map.update();


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


