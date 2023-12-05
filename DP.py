# Python3 implementation for the above approach


def addEdge(adj, x, y):
	adj[x].append(y)
	adj[y].append(x)


def dfs(adj, dp, src, par):
	for child in adj[src]:
		if child != par:
			dfs(adj, dp, child, src)

	for child in adj[src]:
		if child != par:
			# not including source in the vertex cover
			dp[src][0] = dp[child][1] + dp[src][0]

			# including source in the vertex cover
			dp[src][1] = dp[src][1] + min(dp[child][1], dp[child][0])


def minSizeVertexCover(adj, N):
	dp = [[0 for j in range(2)] for i in range(N+1)]
	for i in range(1, N+1):
		# 0 denotes not included in vertex cover
		dp[i][0] = 0

		# 1 denotes included in vertex cover
		dp[i][1] = 1

	dfs(adj, dp, 1, -1)

	# printing minimum size vertex cover
	print(min(dp[1][0], dp[1][1]))


# Driver Code
"""
		1
		/ \
	2	 7
	/ \
	3 6
/|\ 
4 8 5
"""
# number of nodes in the tree
N = 8

# adjacency list representation of the tree
adj = [[] for i in range(N+1)]
addEdge(adj, 1, 2)
addEdge(adj, 1, 7)
addEdge(adj, 2, 3)
addEdge(adj, 2, 6)
addEdge(adj, 3, 4)
addEdge(adj, 3, 8)
addEdge(adj, 3, 5)

minSizeVertexCover(adj, N)
