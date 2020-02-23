import java.util.*;
//import javafx.util.Pair; 
import java.lang.reflect.Array;

public class farziheap<T extends Comparable, E extends Comparable>{
    ArrayList<T> keys = new ArrayList<T>();
    ArrayList<E> values= new ArrayList<E>();
    //public HashMap<T, E> hashmap =new HashMap<>();
    public farziheap(){ 
    }
    public void insert(T key,E value){
        if(values.size()==0){
            keys.add(key);
            values.add(value);
        }
        else{
            keys.add(key);
            values.add(value);
            perlocate(value);
        }


    }
    public void delete(T key){
        E value=findvaluegivenkey(key);
        int index=getindex(values,value);
        //System.out.println(index);
        updater(key,value);
        E newvalue=values.get(index);
        System.out.println(newvalue);
        values.remove(values.size()-1);
        keys.remove(keys.size()-1);
        //System.out.println(values);
        perlocatefordelete(newvalue);

    }
    
    public void update(T key,E value){
        int index=getindexk(keys, key);
        //System.out.println(("bb"));
        Collections.swap(values,index, values.size()-1);
        Collections.swap(keys,index,values.size()-1);
        values.remove(values.size()-1);
        keys.remove(keys.size()-1);
        values.add(value);
        keys.add(key);
        Collections.swap(values,index, values.size()-1);
        Collections.swap(keys,index,values.size()-1);
        perlocatefordelete(value);


    }
    
    public E extractMax(){
        T key=keys.get(0);
        E max=values.get(0);
        System.out.println(max);
        System.out.println(key);

        delete(key);
        
        return max;

    }
    

    /*
    public void printHeap(){

    }
    */
    
    public E findvaluegivenkey(T key){
        int count=0;
        for(int i=0;i<keys.size();i++){
            if(keys.get(i)==key){
                count+=i;
            }
        }
        return values.get(count);


    }
    public void updater(T key,E value){
        int index=getindex(values,value);
        Collections.swap(values,index,values.size()-1);
        Collections.swap(keys,index,keys.size()-1);

    }
    public int getindex(ArrayList<E> values,E value){
        int count=0;
        for(int i=0;i<values.size();i++){
            if(values.get(i)==value){
                count+=i;
            }
        }
        return count;
        
    }
    public int getindexk(ArrayList<T> keys,T key){
        int count=0;
        for(int i=0;i<keys.size();i++){
            if(keys.get(i)==key){
                count+=i;
            }
        }
        return count;
    }

    public void swapv(E value,ArrayList<T> keys,ArrayList<E> values){
        boolean ans=values.contains(value);
        int childindex=getindex(values, value);
        int parentindex=((getindex(values, value)-1)/2);
        if(ans){
            if(values.get(childindex).compareTo(values.get((parentindex)))==1){
                Collections.swap(values,parentindex,childindex);
                Collections.swap(keys,parentindex,childindex);
                
            }
            
        }
    }
    public int newswap(E value,ArrayList<T> keys,ArrayList<E> values){
        boolean ans=values.contains(value);
        int index=getindex(values, value);
        System.out.println(index+"nn");
        //int parentindex=((getindex(values, value)-1)/2);
        int leftchildindex=(2*getindex(values,value)+1);
        int rightchildindex=(2*getindex(values,value)+2);
        while(leftchildindex<=values.size() || rightchildindex<=values.size()){
        if(ans){
            if(leftchildindex>values.size() && values.get(index).compareTo(values.get((leftchildindex)))==1){
                System.out.println("bbb");
                break;
            }
            else if(leftchildindex>values.size() && values.get(index).compareTo(values.get((leftchildindex)))==-1){
                Collections.swap(values,leftchildindex,index);
                Collections.swap(keys,leftchildindex,index);
                //System.out.println("ccc");

                break;
            }
            else if(rightchildindex>values.size()){
                break;
            }

            else if(values.get(index).compareTo(values.get((leftchildindex)))==1 && values.get(index).compareTo(values.get((rightchildindex)))==1){
                //System.out.println("ddd");
                break;
            }

            // else if(values.get(index).compareTo(values.get((parentindex)))==1){
            //     Collections.swap(values,parentindex,index);
            //     Collections.swap(keys,parentindex,index);
            //     return parentindex;

            // }
            else{
                if(values.get(index).compareTo(values.get((leftchildindex)))==-1 && values.get(index).compareTo(values.get((rightchildindex)))==1){
                    Collections.swap(values,leftchildindex,index);
                    Collections.swap(keys,leftchildindex,index);
                    return leftchildindex;
                }
                else if(values.get(index).compareTo(values.get((leftchildindex)))==1 && values.get(index).compareTo(values.get((rightchildindex)))==-1){
                    System.out.println("bb");
                    Collections.swap(values,rightchildindex,index);
                    Collections.swap(keys,rightchildindex,index);
                    return rightchildindex;
                }
                else if(values.get(index).compareTo(values.get((leftchildindex)))==-1 && values.get(index).compareTo(values.get((rightchildindex)))==-1){
                    System.out.println("a");
                    if(values.get(rightchildindex).compareTo(values.get((leftchildindex)))==1){
                        System.out.println("last");
                        Collections.swap(values,rightchildindex,index);
                        Collections.swap(keys,rightchildindex,index);
                        return rightchildindex;
                    }
                    else{
                        Collections.swap(values,leftchildindex,index);
                        Collections.swap(keys,leftchildindex,index);
                        return leftchildindex;

                    }
                }
            }
            
        }
    }
        return -4;


    }

    public void perlocatefordelete(E value){
        newswap(value,keys,values);
        int alpha=newswap(value,keys,values);
        if (alpha!=-4){
            perlocatefordelete(values.get(alpha));
        }

    }
    public void perlocate(E value){
        //int childindex=getindex(values, value);
        int parentindex=((getindex(values, value)-1)/2);
        //System.out.println(parentindex);
        if(parentindex>0){
            swapv(value, keys, values);
            perlocate(values.get(parentindex));
        }
        if(parentindex==0){
            swapv(value,keys,values);

        }

    }

    public static void main(String args[])throws EmptyStackException{
        farziheap push1=new farziheap<>();
        push1.insert(1,100);
        push1.insert(2,10);
        push1.insert(3,30);
        push1.insert(4,50);
        push1.insert(5,150);
        push1.insert(6,1);
        push1.insert(7,3);
        push1.delete(1);
        push1.insert(8,500);
        push1.extractMax();
        //push1.update(7,70);
        
        System.out.println(push1.values);
        System.out.println(push1.keys);
        //ArrayList<Integer> beh=new ArrayList<Integer>();
        //beh.add(1);
        //beh.add(2);
        //beh.get(3);
        //System.out.println(beh);
    }
    


}

    /*

    public int getindexk(ArrayList<T> keys,T key){
        int count=0;
        for(int i=0;i<keys.size();i++){
            if(keys.get(i)==key){
                count+=i;
            }
        }
        return count;
        
    }

    
    public void swapk(T key,ArrayList<T> keys,ArrayList<E> values){
        boolean ans=keys.contains(key);
        int childindex=getindexk(keys, key);
        int parentindex=((getindexk(keys, key)-1)/2);
        if(ans){
            if(keys.get(childindex).compareTo(keys.get((parentindex)))==1){
                Collections.swap(keys,parentindex,childindex);
                Collections.swap(keys,parentindex,childindex);
                
            }
            
        }
    }
    public void perlocatek(T key){
        //int childindex=getindexk(values, value);
        int parentindex=((getindexk(keys, key)-1)/2);
        //System.out.println(parentindex);
        if(parentindex>0){
            swapk(key, keys, values);
            perlocatek(keys.get(parentindex));
        }
        if(parentindex==0){
            swapk(key,keys,values);

        }

    }
    */