# Nurse-Scheduling-problem
A solution to the nurse scheduling problem written in Python using simulated annealing and artificial bee colony

Given n number of nurses over x days, as well as multiple hard restrictions (events that must not occur) and soft restrictions (events that should be prevented if possible), I created the best possible schedule for the hospital, considering multiple possibilities depending on which algorithm I used, and going forward with the best one. 

# Hard restrictions
- A nurse can't take multiple shifts in a single day
- A nurse may not take a night shift followed by a morning shift

# Soft restrictions
- A nurse shouldn't work for more than 7 days in a row

Simulated annealing is a metaheuristic I used to approximate the global optimal solution (schedule).

Artificial Bee Colony (ABC for short from here on) is a population based algorithm that makes use of bees with different roles performing various tasks like scouting, observing or working. In the scope of this project, this means recreating this process by clearly delimiting the problem into a process with multiple steps, each as if it were done by a different group of bees.

Using simulated annealing yields a better result predominantly when the number of nurses is low, while ABC outperforms when dealing with a large number of nurses. They're about equally effective if the number of nurses is equal to around 40 based on the tests I ran.

Example of Test results:
-	Number of nurses: 50
-	Number of days: 20
-	Number of iterations for simulation annealing: 20
-	Number of iterations for ABC: 10

Simulated annealing results:  [440 502 395 196 393 393 318 470 376 284] <br/>
Average of Simulated annealing results:  376.7
Std Deviation of Simulated annealing results:  86.00587189256323
ABC results:  [104  91 127 112 113 152 118 135  99 142]
Average of ABC results:  119.3
Std Deviation of ABC results:  18.52592777703724

