###### Example 4: Airlines Network using Edge List ##################
library("igraph") 
dir()

airports <- read.csv("airports.dat", header=FALSE) ## source: http://openflights.org/data.html
colnames(airports) <- c("Airport ID","Name","City","Country","IATA_FAA","ICAO","Latitude","Longitude","Altitude","Timezone","DST","Tz database timezone")
head(airports[airports$IATA_FAA=='DXB',])


airline_routes <- read.csv("routes.dat", header=FALSE) ## source: http://openflights.org/data.html
colnames(airline_routes) <- c("Airline", "Airline ID", "Source Airport","Source Airport ID","Destination Airport","Destination Airport ID","Codeshare","Stops","Equipment")
head(airline_routes)

#creating a directed Network Graph
#Directed graph definition. A directed graph is graph, i.e., a set of objects (called vertices or nodes)
#that are connected together, where all the edges are directed from 
#one vertex to another. A directed graph is sometimes called a digraph or a directed network.
AirlineNW <- graph.edgelist(as.matrix(airline_routes[,c(3,5)]), directed=TRUE)
plot(AirlineNW)

#Degree
#first and conceptually simplest is degree centrality, which is defined as the number of links incident upon a node 
#(i.e., the number of ties that a node has). The degree can be interpreted in terms of the immediate risk of a node 
#for catching whatever is flowing through the network (such as a virus, or some information). In the case of
#a directed network (where ties have direction), we usually define two separate measures of degree centrality, 
#namely indegree and outdegree. Accordingly, indegree is a count of the number of ties directed to the node and
#outdegree is the number of ties that the node directs to others. When ties are associated to some positive aspects
#such as friendship or collaboration, indegree is often interpreted as a form of popularity, 
#and outdegree as gregariousness

#Closeness
#In a connected graph, the normalized closeness centrality (or closeness) of a node is the average
#length of the shortest path between the node and all other nodes in the graph.
#Thus the more central a node is, the closer it is to all other nodes.

#Betweenness is a centrality measure of a vertex within a graph (there is also edge betweenness,
#which is not discussed here). Betweenness centrality quantifies the number of times a node acts as a 
#bridge along the shortest path between two other nodes

#Eigenvector centrality (also called eigencentrality) is a measure of the influence of a node in a network. It assigns relative scores to all nodes in the network based on the concept that connections to high-scoring nodes contribute more to 
#the score of the node in question than equal connections to low-scoring nodes.
UndirectedAirlineNW <- graph.edgelist(as.matrix(airline_routes[,c(3,5)]),directed=FALSE)
A <- leading.eigenvector.community(UndirectedAirlineNW)

#Number of unique airports present in the dataset
length(unique(names(membership(A))))

#Maximum number  
max(membership(A))

#Community 
closeness_in <- closeness(AirlineNW, mode="in",normalized = TRUE)
btwn <- betweenness(AirlineNW,normalized = TRUE)
indegree <- degree(AirlineNW,mode="in")
outdegree<-degree(AirlineNW,mode='out')
Centralities <- cbind(indegree, outdegree, closeness_in, btwn)
colnames(Centralities) <- c("inDegree","outDegree","closenessIn","betweenness")
head(Centralities)

#Kmeans clustering on degrees centralities

set.seed(20)
AirportCluster <- kmeans(Centralities, 25)

#Difference
sum(AirportCluster$cluster==membership(A))

#Lets take three airports 
#ATL - Hartsfield Jackson Atlanta International Airport
#LAX - Los_Angeles Airport
#FRA - Frankfurt am Main International Airport
airports[airports$IATA_FAA=="ATL",]
airports[airports$IATA_FAA=="LAX",]
airports[airports$IATA_FAA=="FRA",]

#Atlanta is the busiest international airport in the world, hence indegree and outdegree is maximum
max(indegree)
index1 <- which(indegree == max(indegree))
indegree[index1]

max(outdegree)
index2 <- which(outdegree == max(outdegree))
outdegree[index2]

# We know that Frankurt airport location is located in Europe in the center , Europe itself in a central continent
# and hence promoting to more closeness between different continents and airports , The data shows more closeness as well
max(closeness_in)
index3 <- which(closeness_in == max(closeness_in))
closeness_in[index3]

#LAX connects nonstop to 101 domestic and 85 international destinations in
#North America, Latin America, Europe, the Middle East, Africa, Asia, and Oceania and hence it acts as a junction
#resulting in high junctionness
index4 <- which(btwn == max(btwn))
btwn[index4]

airports[airports$IATA_FAA=="ATL",]
airports[airports$IATA_FAA=="LAX",]
airports[airports$IATA_FAA=="FRA",]
