from math import sqrt, cos, sin, pi, asin
import networkx as nx
import matplotlib.pyplot as plt

# Make own haversine for dictionary input
def haversine(dict1, dict2):
    r = 6371
    deg = pi/180
    dlat = (dict2["x"] - dict1["x"]) * deg
    dlon = (dict2["y"] - dict1["y"]) * deg
    root = sin(dlat/2)**2 + cos(dict2["x"]*deg) * cos(dict1["x"]*deg) * sin(dlon/2)**2
    return 2*r*asin(sqrt(root))

# Get adjacent list
def adjacent(id, graph):
    adjc = []
    for i, adj in enumerate(graph[id]):
        if adj != 0:
            adjc.append(i)
    return adjc

# Get distance of a path from the text file
def get_distance(path, parsed_text):
    output = []
    node = parsed_text[1]
    adjacency = parsed_text[3]
    distance = 0.0

    for i in range(len(path)-1):
        output.append((node.index(path[i]), node.index(path[i+1])))
    
    for edge in output:
        distance += adjacency[edge[0]][edge[1]]
    
    return distance

# Parse text file
def parse(filename):
    f = open(filename, "r")
    
    lines = f.readlines()  # Read all lines
    node = []              # List for nodes
    coor = []              # List for coordinates
    adj = []               # List for adjacencies
    
    # Remove new line
    for i in range(len(lines)):
        lines[i] = lines[i].replace('\n', '')
    
    # Total nodes (on line 1)
    nodetotal = int(lines[0])

    # Get coordinates
    for i in range(1, nodetotal+1):
        splitted = lines[i].split(',')
        node.append(splitted[0])
        coor.append({'x': float(splitted[1]), 'y': float(splitted[2])})
    
    # Get adjacency matrix
    for i in range(nodetotal+1, len(lines)):
        split = lines[i].split(' ')
        rows = []
        for jarak in split:
            rows.append(int(jarak))
        adj.append(rows)

    listnode = {}

    for i in range(len(node)):
        adjc = {}
        for nodeid in adjacent(i, adj):
            distance = haversine(coor[nodeid], coor[i])
            adjc[node[nodeid]] = distance
            adj[i][nodeid] = distance
        listnode[node[i]] = adjc
    
    f.close()
    return listnode, node, coor, adj

# Create Graph
def create_graph(type, parsed_text, path = None):
    G = nx.Graph()
    colored = False
    node = parsed_text[1]
    coor = parsed_text[2]
    adj = parsed_text[3]

    pos = {}
    edgelabel = {}

    nodecolor = []
    pathcolor = []
    if path is not None:
        colored = True
        for i in range(len(path)-1):
            pathcolor.append((path[i], path[i+1]))
            pathcolor.append((path[i+1], path[i]))
    
    # Assign graph to visualizer
    for i in range(len(adj)):        
        # Assign graph position from input to visualizer
        pos[node[i]] = (coor[i]["x"], coor[i]["y"])
        for j in range(len(adj[i])):
            if (i != j and i < j and adj[i][j] != 0):
                # Assign edge color
                color = None
                if (node[i],node[j]) in pathcolor:
                    color = "red"
                else:
                    color = "black"
                
                # Assign edge to visualizer
                G.add_edge(node[i],node[j],color=color)
                edgelabel[(node[i], node[j])] = '%.2f'%adj[i][j]
    
    for node in G:
        # Node Color
        if colored and node in path:
            nodecolor.append("red")
        else:
            nodecolor.append("white")

    # type = tipe graf
    # -1 = x y (default)
    # 0 = planar
    # 1 = circular
    # 2 = spectral
    # 3 = spring
    # 4 = shell

    options = {
        "with_labels": True,
        "node_color": nodecolor,
        "edge_color": [G[i][j]['color'] for i,j in G.edges()],
        "edgecolors": "black"
    }

    # Different graph layouts for different cases
    if type == -1:
        nx.draw_networkx(G, pos, **options)
    elif type == 0:
        pos = nx.planar_layout(G)
        nx.draw_planar(G, **options)
    elif type == 1:
        pos = nx.circular_layout(G)
        nx.draw_circular(G, **options)
    elif type == 2:
        pos = nx.spectral_layout(G)
        nx.draw_spectral(G, **options)
    elif type == 3:
        pos = nx.spring_layout(G)
        nx.draw_spring(G, **options)
    elif type == 4:
        pos = nx.shell_layout(G)
        nx.draw_shell(G, **options)
                
    nx.draw_networkx_edge_labels(G, pos, edge_labels = edgelabel)
    
    # Set margins for the axes so that nodes aren't clipped
    ax = plt.gca()
    ax.margins(0.20)
    plt.axis("off")
    plt.show()
