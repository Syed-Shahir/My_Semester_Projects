#include <iostream>
#include <unordered_map>
#include <vector>

using namespace std;

// This class represents a directed graph using adjacency list representation
class Graph {
  int V; // Number of vertices
  unordered_map<int, vector<int>> adj; // Adjacency list

 public:
  Graph(int V) {
    this->V = V;
  }

  void addEdge(int v, int w) {
    adj[v].push_back(w); // Add w to v's list
  }

  void printGraph() {
    // Iterate through all the vertices
    for (int v = 1; v <=V; v++) {
      cout << v << ": ";

      // Iterate through all adjacent vertices of v
      for (int i : adj[v]) {
        cout << i << " ";
      }

      cout << endl;
    }
  }
};

int main() {
    int n,m,c;
    cout<<"enter number of nodes =";
    cin>>n;
  Graph g(n);
  cout<<"enter number of edges =";
  cin>>m;
  cout<<"enter 1 for directed and 0 for undirected =";
  cin>>c;
  if(c==0)
    m=2*n;
  for(int i=0;i<m;i++)
	{
		int u,v;
		cout<<"link between :";
		cin>>u;
		cout<<" & ";
		cin>>v;
		//cin>>u>>v;
		//creating an undirected graph
		g.addEdge(u,v);
	}
g.printGraph();

  return 0;
}

