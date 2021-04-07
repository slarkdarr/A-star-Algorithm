from utility import haversine

def heuristic_distance(parsed_text, target_node):
    for i in range(len(parsed_text[1])):
        # The index of target
        if parsed_text[1][i] == target_node:
            target = i
    # Make a dict.
    # Key = Node
    # Value = Eucledian Distance from current node to target node
    target_dist = []
    heuristic = {}
    for i in range(len(parsed_text[1])):
        target_dist.append(haversine(parsed_text[2][target], parsed_text[2][i]))
        heuristic[parsed_text[1][i]] = target_dist[i]
    return heuristic

def search(parsed_text, heuristic, initial_node, target_node): 
    
    # Initialization two list of nodes
    can_visit = []          # Can be visited
    to_visit = []           # To be visited

    # Parent Dict
    # Key = Node
    # Value = Parent Node
    parent = {}
    for i in parsed_text[1]:
      parent[i] = None

    # F Value
    dict_f= {}
    dict_f[initial_node] = heuristic[initial_node]

    # G Value
    dict_g = {}
    dict_g[initial_node] = 0

    can_visit.append(initial_node)
    
    # Loop until can_visit list is empty
    while len(can_visit) > 0:
        # Take node f with the lowest value
        temp_dict = {}
        for node in can_visit:
            if dict_f.get(node, "Not Available") != "Not Available":
                temp_dict[node] = dict_f[node]
        temp_dict = dict(sorted(temp_dict.items(), key=lambda item: item[1]))
        for i in temp_dict.keys():
            can_visit.append(i)
        current_node = can_visit.pop(0)
        to_visit.append(current_node)

        # If we already arrive on target
        if current_node == target_node:
            path = []
            while current_node != initial_node:
                path.append(current_node)
                current_node = parent[current_node]
            path.append(initial_node)
            return path[::-1]

        neighbors = parsed_text[0][current_node]  

        for neighbor in neighbors.keys():
            if(neighbor in to_visit):
                continue
            parent[neighbor] = current_node

            # Update g value dan f value if the new f value is minimum
            if(dict_g[current_node] + neighbors[neighbor] + heuristic[neighbor] < dict_f.get(neighbor, 99999999)):
                dict_g[neighbor] = dict_g[current_node] + neighbors[neighbor] 
                dict_f[neighbor] = dict_g[neighbor] + heuristic[neighbor]
                can_visit.append(neighbor)
    # Return None if there's no path available
    return None
