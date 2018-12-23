# CCBias

CCbias is a tool to help observational researchers understand how selection bias plays a role in their data. 
Suppose it is desired to observe some kind of event that occurs in nature. Maybe it's supernovae, or perhaps volcanic eruptions. For each event, there is some observable data associated with it, and there exists a set that contains all the information about all the events that have ever occured up to some time. Since the contents of that set are dependent on time, let us call it T(t_1,t_2) : R^2 -> E, (where E is a space of sets of events) a function of time that returns all events that occured after t_1 and before t_2.
Of course, as observers we never have unrestricted access to T(t_1,t_2). There is another function O(T) : E -> E such that O(T(t_1,t_2)) is all the events in T(t_1,t_2) that were actually observed.
As observers, we try to reconstruct the statistical properties of T(t_1,t_2) from O(T(t_1,t_2)). The motivating questions of CCBias number two: 
1: Human choices (e.g. what days to observe, how much money is available) affect O(T). Of the choices that can be easily changed, given a definition of optimal, what set of choices produces the optimal result-data O(T(t_1,t_2))?
2: Given a set of observed events O' and some information about O(T), under what conditions can we solve the inverse-problem of finding the properties of T?