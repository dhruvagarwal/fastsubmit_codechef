import java.io.*;
import java.util.*;
 
public class Main {
 
	public static void main(String args[]) {
 
		try {
 
			BufferedReader input = new BufferedReader(new InputStreamReader(System.in));
			int t;
			List<Integer> myList;
 
			while(true) {
				int move = 0;
				int sum = 0;
				myList = new ArrayList<Integer>();
				t = Integer.parseInt(input.readLine());
				if(t==-1)
					break;
				//String arr[] = new String[t];
				int[] arr = new int[t];
				for(int i=0;i<t;i++) {
					arr[i] = Integer.parseInt(input.readLine());
					sum += arr[i];
				}
				if(sum%t !=0) {
					move = -1;
				}
				else {
					int eq = sum/t;
					Arrays.sort(arr);
					for(int i=t-1; i>=0 ; i--) 
						if((arr[i]<eq)) {
							move+=eq-arr[i];
							
						}
				}
					System.out.println(move);
			}		
 
		}
 
		catch (Exception e) {}
	}
}
 

