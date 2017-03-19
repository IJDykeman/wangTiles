void setup(){
  size(900,900);
}
Integer i = 1;
void draw(){
  println(i.toString()+".png");
  PImage im = loadImage(i.toString()+".png");
  println(i);
  image(im,0,0,900,900);
  i +=1;
  
}
