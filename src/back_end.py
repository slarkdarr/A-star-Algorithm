import os
from astar import heuristic_distance, search
from utility import haversine, get_distance, parse, create_graph

parsed_text = None
type = 0

def initialization(filename = None):
    if filename is None:
        cwd = os.getcwd()
        test_path = cwd + '\\..\\test'
        list_files = [f for f in os.listdir(test_path) if os.path.isfile(os.path.join(test_path, f))]
        filename = str(input("Insert file name with extension (e.g.: file1.txt) :\n"))
        found = False
        while True:
            for i in range(len(list_files)):
                if (filename == list_files[i]):
                    found = True
            if (found):
                break
            else:
                filename = str(input("Invalid file name, please input again (e.g.: file1.txt) :\n"))

        filepath = test_path + '\\' + filename
    
    global parsed_text
    parsed_text = parse(filepath)

    print()
    print("Graph Visualization (weight in kilometer)")
    create_graph(type, parsed_text)

def search_path(initial_node = None, target_node = None):
    if initial_node is None or target_node is None:
        initial_node = input("Initial Node : ")
        target_node = input("Target Node : ")
    
    heuristic = heuristic_distance(parsed_text, target_node)
    searchPath = search(parsed_text, heuristic, initial_node, target_node)

    if searchPath is not None:
        print()
        print("Result")
        distance = get_distance(searchPath, parsed_text)
        print("The shortest distance between", initial_node, "and", target_node, "is", '%.3f'%distance, "km")
        create_graph(type, parsed_text, searchPath)
    else:
        print("No path found")

def graph_type(tipe):
    if tipe == -1 or tipe == 0 or tipe == 1 or tipe == 2 or tipe == 3 or tipe == 4:
        # -1 = using x, y (default)
        # 0 = planar
        # 1 = circular
        # 2 = spectral
        # 3 = spring
        # 4 = shell
        name = ["default", "planar", "circular", "spectral", "spring", "shell"]
        global type
        type = tipe
        print("Graph type : ", name[tipe+1])
    else:
        raise Exception("Wrong type")
