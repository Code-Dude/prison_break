import sys
from graph import Graph, Vertex

def create_graph(filename):
    # read the lines in the specified file
    # to create a Graph object. Returns 3 values:
    #
    #     prison_graph, prisoner_vertex, exit_vertex

    first_line = True

    with open(filename) as f:
        rows, columns = 0, 0
        camera_locations = []
        graph_as_nested_list = []
        graph = Graph()

        for line in f:
            if line != '\n':
                if first_line:
                    row_str, column_str = line.split(' ')
                    rows, columns = int(row_str), int(column_str)
                    first_line = False
                else:
                    camera_row_str, camera_column_str = line.split(' ')
                    camera_row, camera_column = int(camera_row_str), int(camera_column_str)
                    camera_locations.append((camera_row, camera_column))

        for row in range(rows):
            graph_as_nested_list.append(list())
            for column in range(columns):
                node_contains_camera = False

                if (row, column) in camera_locations:
                    node_contains_camera = True

                new_vertex = Vertex((row, column), node_contains_camera)
                if new_vertex not in graph_as_nested_list[row]:
                    graph_as_nested_list[row].append(new_vertex)
                    graph.add_vertex(graph_as_nested_list[row][column])

        for row in range(rows):
            for column in range(columns):
                    if row - 1 >= 0:
                        graph.add_undirected_edge(graph_as_nested_list[row][column],
                                                 graph_as_nested_list[row -1][column])

                    if row + 1 < rows:
                        graph.add_undirected_edge(graph_as_nested_list[row][column],
                                                 graph_as_nested_list[row + 1][column])

                    if column - 1 >= 0:
                        graph.add_undirected_edge(graph_as_nested_list[row][column],
                                                 graph_as_nested_list[row][column - 1])

                    if column + 1 < columns:
                        graph.add_undirected_edge(graph_as_nested_list[row][column],
                                                 graph_as_nested_list[row][column + 1])

    return graph, graph_as_nested_list[0][0], graph_as_nested_list[rows - 1][columns - 1]

def count_exit_paths(g, start_vertex, exit_vertex, current_path, count):
    # Use depth-first-search to count how many distinct
    # paths exist from the given start vertex to the given
    # exit vertex.

    current_path.append(start_vertex)

    if start_vertex.label == exit_vertex.label:
        return 1
    else:
        num_complete_sub_paths = 0
        for vertex in g.adjacency_list[start_vertex]:
            if (vertex not in current_path) and (not vertex.has_camera):
                next_path = list(current_path)
                num_complete_sub_paths += count_exit_paths(g, vertex, exit_vertex, next_path, count)

        count += num_complete_sub_paths

    return count

if __name__ == "__main__":
    prison_filename = sys.argv[1]
    prison_graph, prisoner_vertex, exit_vertex = create_graph(prison_filename)
    path = []
    count = 0
    num_paths = count_exit_paths(prison_graph, prisoner_vertex, exit_vertex, path, count)
    print(num_paths)
