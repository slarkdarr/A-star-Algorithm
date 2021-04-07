from back_end import initialization, search_path, graph_type

# -1 = use x y position
# 0 = planar (default)
# 1 = circular
# 2 = spectral
# 3 = spring
# 4 = shell

tipe = 0

graph_type(tipe)
initialization()
search_path()
