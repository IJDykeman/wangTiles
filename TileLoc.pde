class TileLoc{
  int x;
  int y;
  TileLoc(int nx, int ny){
    x= nx;
    y = ny;
  }
  
  public boolean equals(Object o){
    int ox = ((TileLoc)o).x;
    int oy = ((TileLoc)o).y;
    return x == ox && y == oy;
  }
}
