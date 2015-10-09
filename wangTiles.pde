import java.util.Collections;

Map map;
boolean showLines = false;

int tileWidth = 10;
int mapWidth = 80;
String FILENAME = "wangTiles.png";


void setup() {
  frameRate(10000);
  final int windowWidth = tileWidth*mapWidth;
  size(windowWidth, windowWidth);
  noSmooth();
  resetMap();

}

void checkForUpdatedTileImage(){
  if (!imagesEqual(loadImage(FILENAME), map.tilesImage)) {
    resetMap();
  }
}



void resetMap(){
  map = new ConstrainedMap(mapWidth,tileWidth);
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
