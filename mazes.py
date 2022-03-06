from Maze import Maze
from time import time
import argparse

## TODO try left-hand rule (ensure no pre-processing)
## TODO implement Fibonacci Heap, increased Dijkstra/A* speed

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--maze', help="Maze file name", type=str, default="normal")
    parser.add_argument('-a', '--algorithm', help="Algorithm type", type=str, default="ASTAR")
    parser.add_argument('-p', '--pre_processing', help="'True' | 'False'", type=str, default="False")
    parser.add_argument('-c', '--cull', help="cull graph?", type=str, default="True")
    parser.add_argument('-t', '--track', help="Track nodes the algorithm searched", type=str, default="True")


    args = parser.parse_args()
    pre_proc = args.pre_processing == 'True'
    track = args.track == 'True'
    cull = args.cull == 'True'
    print("Creating Graph...")
    startTime = time()


    maze = Maze(args.maze, PREPROCESSING=pre_proc, CULLING=cull)

    print("Graph Created!", len(maze.G.vertices))

    #Solve the maze

    num_nodes = maze.Solve(args.algorithm.upper(), MARK = track)

    print("Solved! Path is", maze.G.end.distance, "nodes long. \nTime to solve in seconds: ", time() - startTime)
    print("Nodes explored:", num_nodes)

    ##Now draw on image!!
    maze.ColorImage()#out=r"Output/out.png")

    #Display the image
    maze.img.show()