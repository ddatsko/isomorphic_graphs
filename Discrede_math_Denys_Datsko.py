import os
import random


def next_permutation(perm):
    """
    (lst) -> lst

    Precondition: all the elements must be different
    Generates the next permutation by the given one
    Return None if the permutation is the last

    >>> next_permutation([1, 2, 5, 4, 3])
    [1, 3, 2, 4, 5]

    >>> next_permutation([3, 2, 1])
    None
    """
    n = len(perm)
    j = n - 2
    while perm[j] > perm[j + 1]:
        j -= 1
    k = n - 1
    while perm[j] > perm[k]:
        k -= 1
    perm[j], perm[k] = perm[k], perm[j]
    r = n - 1
    s = j + 1
    while r > s:
        perm[r], perm[s] = perm[s], perm[r]
        r -= 1
        s += 1
    if sorted(perm) == perm:
        return None
    return perm


def show_graph(graph, number):
    """
    (dict, str) -> None

    @param number - photo number that will be addad to the name of file
    Shows the graphs using igraph library in default image viewer
    and creates .png file of it
    """
    try:
        from igraph import Graph, plot

        # get the lists of unique edges and vertices
        edges = set()
        for key in graph:
            for i in graph[key]:
                edges.add(tuple(sorted([key, i])))
        vertices = list(graph.keys())

        # create graph from the given one
        g = Graph()
        g.add_vertices(vertices)
        g.add_edges(list(edges))

        # make formating for our graph (size of vertex depends on its
        # degree, colors are random)
        g.vs["label"] = vertices
        colors = ["#66FF66", "#B2FF66", "#66B2FF", "#9999FF", "#FF6666",
                  "#FFB266", "#FFFF99", "#E0E0E0", "#A9B9DA"]
        for i in g.vs:
            i["size"] = len(graph[i["name"]]) * 4 + 15
            i["color"] = random.choice(colors)
        formating = {
            "vertex_label_dist": 1.5,
            "vertex_label_size": 20,
            "margin": 40,
            "vertex_label_angle": 1.57,
            "edge_color": "#888888"
        }

        # choose the layout and file for the graph
        if len(graph) <= 10:
            layout = g.layout_circle()
        else:
            layout = g.layout_lgl()
        file = "graph" + number + ".png"

        # show and print graph to file
        plot(g, layout=layout, **formating)
        plot(g, file, layout=layout, **formating)
    except ImportError:
        print("Sorry, you should install module igraph")
    except:
        print("Ouch... Something went wrong")


def line_to_dict(line):
    """
    (str) -> dict

    Convert the line of format "[(v1, v2), (v3, v4)]" to dictionary
    """
    try:
        line = line.strip().replace("]", "").replace(
            "[", "").replace("(", "").replace(")", "").replace(" ", "")
        vertices = line.split(",")
        dct_vertices = {}
        for vertex in range(0, len(vertices), 2):
            if vertices[vertex] in dct_vertices:
                dct_vertices[vertices[vertex]].append(vertices[vertex + 1])
            else:
                dct_vertices[vertices[vertex]] = [vertices[vertex + 1]]
            if vertices[vertex + 1] in dct_vertices:
                dct_vertices[vertices[vertex + 1]].append(vertices[vertex])
            else:
                dct_vertices[vertices[vertex + 1]] = [vertices[vertex]]
        return dct_vertices
    except:
        print("So sad... your data is of the wrong format")
        exit()


def read_graphs(file):
    """
    (str) -> dict, dict

    Reads the info of graph and returns the graph
    """
    try:
        if file:
            f = open(file, "r")
            line = f.readline()
        else:
            line = input().strip()
        dct_vertices1 = line_to_dict(line)
        if file:
            line = f.readline()
        else:
            line = input().strip()
        dct_vertices2 = line_to_dict(line)
        if file:
            f.close()
        return dct_vertices1, dct_vertices2
    except IOError:
        print("Sorry, I can`t find this file...")
        exit()


def get_graphs():
    """
    None -> tuple(list(tuple), list(tuple))

    Gets two graphs from user
    """
    from_file = input(
        "Do you want to get graph from file [y] or enter it here [n]? [y/n] ")
    while not from_file.strip() or from_file not in "YyNn":
        from_file = input("Enter either 'y' or 'n': ")
    if from_file.lower() == 'y':
        file = input("Enter the file name please: ")
        graphs = read_graphs(file=file)
    else:
        graphs = read_graphs(file="")
    try:
        os.system("clear")
    except:
        pass
    want = input(
        "Do you want to be shown the visualisation of the 1-st graph [y/N]: ")
    if want and want in "yY":
        show_graph(graphs[0], "1")
    try:
        os.system("clear")
    except:
        pass
    want = input(
        "Do you want to be shown the visualisation of the 2-nd graph [y/N]: ")
    if want and want in "yY":
        show_graph(graphs[1], "2")
    try:
        os.system("clear")
    except:
        pass
    return graphs


def check_isomorphism(graph1, graph2):
    """
    (dict, dict) -> bool

    Check if 2 graphs are isomorphic
    """
    # Check if they are not isomorphic by simple signs(number of edges,
    # number of vertices, degrees of all the vertices
    if len(graph1) != len(graph2):
        return False
    degrees = [0] * len(graph1) * 2
    for i in graph1:
        degrees[len(graph1[i])] += 1
    for i in graph2:
        degrees[len(graph2[i])] -= 1
    for vertice in degrees:
        if vertice != 0:
            return False

    # check by considering all the possible permutations of vertices
    perm = sorted(list(graph2.keys()))
    while perm:
        bad = -1
        change = dict(zip(graph1.keys(), perm))
        for key in graph1:
            if len(graph1[key]) != len(graph2[change[key]]):
                bad = change[key]
                break
            for vertex in graph1[key]:
                if change[vertex] not in graph2[change[key]]:
                    break
            else:
                continue
            break
        else:
            return change
        if bad != -1 and perm.index(bad) != len(perm)-1:
            perm[perm.index(
                bad)+1:] = sorted(perm[perm.index(bad)+1:], reverse=True)
        perm = next_permutation(perm)
    return False


def print_isomorphism(res):
    """
    (dict) -> None

    Print the result
    """
    try:
        os.system("clear")
    except:
        pass
    if not res:
        print("So sad((( These graphs are not isomorphic\n\
Maybe next time you will be luckier")
    else:
        print("Hooray!!! Your graphs are isomorphic. Here`s one of possible \
correspondences:")
        for i in res:
            print(i, "-->", res[i])


def print_intro():
    mes = """This program checks whether 2 graphs are isomorphic
You can input data from file or terminal but in both cases
it should be in the format [(v1, v2), (v3, v4), (v5, v6)] or
v1, v2, v3, v4, understanding that it means that there is an edge between
v1 and v3, v2 and v4 ... (while reading all the symbols except "," are deleted)
You can use any names for vertices.

If you choose to visualize a graph - it will be shown to you via 
default image viewer and there will be created an image (.png) of it.

NOTE
The program can work very long you enter graphs with more than 10 vertices).
    """
    print(mes)


def main():
    """
    The main function of the program for checkig
    graphs for isomorphism
    """
    # clear the screen
    try:
        os.system("clear")
    except:
        pass

    # proceed functions
    print_intro()
    graphs = get_graphs()
    print("Checking graphs...")
    isomorphism = check_isomorphism(graphs[0], graphs[1])
    print_isomorphism(isomorphism)

    more = input('Do you want to check more graphs? [y/N]: ')
    if more and more in "yY":
        main()


if __name__ == "__main__":
    main()
