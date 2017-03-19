import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;


ArrayList<TileProbabilitySphere> getSpheres(){
ExecutorService EXEC = Executors.newCachedThreadPool();
List<Callable<TileProbabilitySphere>> tasks = new ArrayList<Callable<TileProbabilitySphere>>();
//for (Tile tile: wangTiles) {

for (int i = 0; i< wangTiles.size(); i++){
    final Tile tile = wangTiles.get(i);
    Callable<TileProbabilitySphere> c = new Callable<TileProbabilitySphere>() {
        @Override
        public TileProbabilitySphere call() throws Exception {
            return new TileProbabilitySphere(tile);
        }
    };
    tasks.add(c);
}
try{
  List<Future<TileProbabilitySphere>> results = EXEC.invokeAll(tasks);
  ArrayList<TileProbabilitySphere> toReturn = new ArrayList<TileProbabilitySphere>(); //<>//
  for (Future<TileProbabilitySphere> fut : results){
    toReturn.add(fut.get());
  }
}
catch(Exception e){}
finally{}
return null;
}