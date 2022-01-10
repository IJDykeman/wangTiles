import java.util.Collections;
import java.util.*;


Map map;
boolean showLines = false;

final int tileWidth = 12;
final int sphereWidth = 5;
final int mapWidth = 64;
//String FILENAME = "dungeon.png";
//String FILENAME = "wangTiles_classic.png";
String FILENAME = "tiles.png";
//String FILENAME = "dungeon.png";
//String FILENAME = "wangTiles_classic.png";
ArrayList<Tile> wangTiles;
PImage tilesImage;
HashMap<Tile, Integer> tileToNum= new HashMap<Tile, Integer>();

void settings(){
  final int windowWidth = tileWidth * mapWidth;
  size(windowWidth, windowWidth);
  //noSmooth();
//  smooth(4);

}

void setup() {
  tilesImage = loadImage(FILENAME);
  wangTiles = parseTilesIntoSet();

  println("so");
  for (int i = 0; i < wangTiles.size(); i++){
    tileToNum.put(wangTiles.get(i),i);
  }
  frameRate(100);

  
  
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
  //map = new ConstrainedMap(mapWidth,tileWidth);

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
  //save("output/" + frames.toString() + ".png");
  saveFrame("frame-######.png");
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
