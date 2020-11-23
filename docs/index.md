# Freeze Tag Robots - RIT CSCI-716: Computational Geometry - Final Project 
## Group Members
- John Tran (jxt5551@rit.edu)
- Brian Musliner (bcm7897@rit.edu)
- Brendan Mutton (bxm8164@rit.edu)

## Chosen Category
Category 2: Work on Open Problems in the Field

## Description
    A specific description of the problem that you are trying to solve, in two sentences or less. This may be an answer to a question like: What does your application do? What is your visualization trying to show? What open problem were you trying to address?

Different algorithms for the "Freeze-Tag Problem: How to Wake Up a Swarm of Robots" and a visualizer to demonstrate the different algorithms.

## Background Information

    Background information about the problem. What is the current best known algorithm? What are the proven theoretical bounds on the problem?

## Application Domain

    If you have an application domain problem:

    Background information about the problem.

    What are your specific inputs and outputs (show a visualization, if possible).

    What are the needs for the problem domain -- is it important that you find the optimal solution? why or why not?

    Are there related projects by others that tackle the same problem. How?

    Describe your algorithm and show example results.

    Give a complexity analysis of your algorithm, and also show measured running time for different sizes of inputs 

## Approaches

    What approaches have you tried? Can you visualize the results? Show sketches of where proof attempts have failed, or example point sets where your (mostly good) algorithm has a bad case?

### Jarvis March Convex Subhulls
A solution we propose is called Jarvis March Convex Subhulls. This solution uses the Jarvis March algorithm to compute all the subhulls of a set of points. 
To do this the convex hull of the set of points is computed. Then all points that were part of the convex hull are removed from the set. Then the next convex hull is computed.
This process is repeated until there are only 6 points left. Each subhull is saved to a list. This list of subhulls serves as a work order list. 
In the sequential version a single robot moves through the list of subhulls, waking up every robot along the way. 
The following GIF is the sequential version

![Sequential Jarvis March Freeze Tag Robots](JarvisMarchSequential.gif)

In the parallel version when a robot is woken up, it checks the list of subhulls. If there is a subhull available, the robot will remove the subhull from the list and begin waking up all the robots in that subhull.
This process continues until all the robots are awoken.

![Parallel Jarvis March Freeze Tag Robots](JarvisMarchParallel.gif)

### KMeans Clustered Awakening
Another solution we propose is called KMeans Clustered Awakening. This solution uses the KMeans clustering algorithm to cluster all the points in the set.
Once the clusters have been determined the sequential version utilizes a single robot to move through every cluster and wake up every robot. 
The path the robot takes within the cluster is random based on the input order of the points. The following give shows the sequential version

![Sequential KMeans Freeze Tag Robots](KMeansSequential.gif)

The parallel version, similar to Jarvis March Convex Subhulls, uses the list of clusters as work orders. A robot that is awoken will check to see if there are any available clusters.
If there are it will move to wake up that cluster. The following GIF visualizes KMeans Clustered Awakening Parallel

![Parallel KMeans Freeze Tag Robots](KMeansParallel.gif)

## Results

## Conclusion

## Challenges

## Future Work

## References
Arkin, E., Bender, M., Fekete, S. et al. The Freeze-Tag Problem: How to Wake Up a Swarm of 
Robots. Algorithmica 46, 193–221 (2006). 

Arkin, E., Bender, M., & Ge, D. (2003). Improved Approximation Algorithms for the Freeze-Tag 
Problem. In Proceedings of the Fifteenth Annual ACM Symposium on Parallel 
Algorithms and Architectures (pp. 295–303). Association for Computing Machinery.

Problem 35: Freeze-Tag: Optimal Strategies for Awakening a Swarm of Robots. (n.d.). Retrieved 
September 07, 2020, from http://cs.smith.edu/~jorourke/TOPP/P35.html

Arkin, E., Bender, M., Fekete, S., Mitchell, J., & Skutella, M. (2002). The Freeze-Tag
Problem: How to Wake up a Swarm of Robots. In Proceedings of the Thirteenth Annual
ACM-SIAM Symposium on Discrete Algorithms (pp. 568–577). Society for Industrial
and Applied Mathematics.
