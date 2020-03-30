# include<iostream>
using namespace std;

// heap sort 
void max_heapify(int arr[],int n,int i)
{
   // index in the arr[] is the size of the heap or heapsize = n
   int largest = i;
   int l = 2*i+1;
   int r = 2*i+2;

   if (l < n and arr[l] > arr[largest])
      largest = l;
   if (r < n and arr[r] > arr[largest])
      largest = r;
   if (largest != i)
   {
      swap(arr[i],arr[largest]);
      max_heapify(arr,n,largest);
   }
}

void heapsort(int arr[],int n)
{
   // n heapsize 
   // building max heap array
   for (int i = n/2-1;i>=0;i--)
      max_heapify(arr,n, i);

   for(int i = n-1;i>=0;i--)
   {
      swap(arr[0],arr[i]);
      max_heapify(arr,i,0);
   }
}

void printArray(int arr[], int n) 
{ 
    for (int i=0; i<n; ++i) 
        cout << arr[i] << " "; 
    cout << "\n"; 
} 
  
int main() 
{ 
   int arr[] = {12, 11, 13, 5, 6, 7}; 
   int n = sizeof(arr)/sizeof(arr[0]); 
   heapsort(arr,n); 
   printArray(arr, n);     
}