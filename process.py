def CO2(graph, parent):  
    #calculates the amount of CO2 emissions
    totaldistance = timings(graph) 
    #gets the sum of the total time

    message = ""
    sum = distance('SO21 1HA', parent['postcode']) 
    #add the distance from school to the house

    for child in parent['collecting']:
        sum += distance('SO21 1HA' , child['postcode']) 
        #add the individual distances from school to each house

    saved = totaldistance[1] – sum 
    #get the total time saved
    
    emission = round((saved/2) * 0.164) 
    #converts it to amount of CO2 emissions in kilograms

    trees = round((emission / 21.77) * 5)  
    #calculates the amount of work done a tree would have to do to reduce the amount of CO2 in the earth’s atmosphere. 
    
    message += "You have saved " + str(emission) + " kg of CO2 today.\nThis is about the work of " + str(trees) + " trees this week."
  
    return message

def prims(graph): 
    #finds the minimum spanning tree using prims’ algorithm
    visit = set()
    tree = []
  
    start = list(graph.keys())[0] 
    #gets the start node which is always the first node in the graph
    visit.add(start)
  
    while len(visit) < len(graph): 
        #checks if the number of nodes visited is less than the number of nodes in the graph

        edge = None
        for node in visit:
            for neighbor, weight in graph[node]:
                if neighbor not in visit and (edge is None or weight < edge[2]): 
                    #checks which edge is the shortest
                    edge = (node, neighbor, weight) 
  
        if edge is not None:
            tree.append(edge) 
            #adds node and node’s neighbor with shortest edge between them to tree
            visit.add(edge[1]) 
            #moves to next node
          
    return(tree)

def mst_to_graph(grapht): 
    #converts the list of node and edges gotten from prims’ algorithm back into a graph
    mst_edges = prims(grapht)
    mst_graph = {}

    for start, dest, weight in mst_edges:
        if start not in mst_graph:
            mst_graph[start] = []
        
        if dest not in mst_graph:
            mst_graph[dest] = []
        
        mst_graph[src].append([dest, weight])
        mst_graph[dest].append([src, weight])
    
    return(mst_graph)

def search(mgraph, visited_node): 
    #checks if every node in in the list
    
    for key in list(mgraph.keys()):
        if key not in visited_node:
            return False

    return True

def dfs(grapht): 
    #does depth first
    graph = mst_to_graph(grapht)
    start_node = list(graph.keys())[0] 
    #adds first node 
    
    visited = [start_node]
    stack = []
    graph = graph
    current = start_node

    while not search(graph, visited):
        decision = True 
        #determines if one can transverse further down
        for neighbour in graph[current]:
            if neighbour[0] not in visited:
                stack.append(current)
                current = neighbour[0]
                visited.append(current)
                decision = False
                break

        if decision and not search(graph, visited):
            current = stack.pop() 
            #removes nodes from the stack
      
    return visited

def schedule(graph): 
    #creates the schedule the parent should take
    new_graph = prims(graph)
    depth_first = dfs(graph)
    route = []
    neigbour = None
    
    for x in range(len(depth_first)):
        for y in range(len(new_graph)):
            if depth_first[x] == new_graph[y][0] and depth_first[x+1] == new_graph[y][1]: 
                #goes through the list for depth first and minimum spanning tree and check if the nodes following it is connected
                route.append(depth_first[x]) 
                #if it is connected, add it to the route
                break
        
        else:
            #if it not connected reverses backwards and add the nodes to the route until it gets to a node that the current node is connected to
            #add the node it is connected to and the node itself to the route
            current = depth_first[x]
            
            for z in range(len(new_graph)): 
                if current == new_graph[z][1]:
                    neigbour = new_graph[z][0]
            
            while neigbour != depth_first[x-1]:
                route.append(depth_first[x-1])
                x = x - 1
            
            route.append(depth_first[x-1])
            route.append(current)
      
    return(route)

def timings(graph): 
    #uses the route made to determine how long it will take
    route = schedule(graph)
    path  = [route[0]]
    time = []
    last_node = list(graph.keys())[-1]
    sum = distance('SO21 1HA', last_node)
    
    for i in range(len(route)-1):
        for key in graph:
            if route[i] == key:
                for x in range(len(graph[key])):
                    if route[i+1] == graph[key][x][0]:
                        sum = sum+graph[key][x][1] + 1
                        path.append(graph[key][x][0])
                        time.append(graph[key][x][1])

    return path, sum, time

def message(parent, graph): 
    #creates message about the route to take and the timing of everything
    time = timings(graph)
    emissions = CO2(graph, parent) 
    message = "The route is: \n"
    middle = time[1] 
    start = datetime.fromtimestamp(time[1]*60) 
    #converts the integer to time format
    
    end = datetime.strptime("1970:01:01:8:00" , "%Y:%m:%d:%H:%M") 
    #end time is the latest time one should arrive but still not be late thus 8:00
    
    difference = end – start 
    #get the lastest time the parent should leave their house
    
    for x in range(len(time[0])):
        message = message + time[0][x] + " is the postcode"
        message = message + " and the suggested leave time is " + str(difference) + "\n"
            
        try: 
            middle -= time[2][x]
            difference = end - datetime.fromtimestamp(middle*60) 
            #increases time but the time taken to get to each house
        
        except:
            pass
      
        try:
            message = message + "The address is " + parent['collecting'][x]['address'] + " "  
            #adds the address of each house
        
        except:
            pass
      
    message = message + "\n" + emissions  
  
    return(message)

def sendmailtodrop(parent, graph): 
    #creates email for parents who are picking up children
    messagetosend = message(parent, graph)
    additionalmessage = "Dear " + parent['name'] + ", \n\nThis is the list of addresses of the children you are picking. The list has the child's address, postcode as well as suggested time to leave in order to get to school on time. \n\n"
    
    sender = 'schoolrunexpress@gmail.com' 
    #sender email
    
    password = 'etviqzudvdvrocnr'
    reciever = parent['email']
    server = smtplib.SMTP('smtp.gmail.com', 587) 
    #587 is the port number used to send the email
    
    server.starttls()
    server.login(sender, password) 
    #logins into the gmail account
    
    server.sendmail(sender, reciever, 'Subject: School Run Express\n\n' + additionalmessage  +  messagetosend + "\n\nThank you for using School Run Express")
    server.quit()

def sendmaintopick(email, parenttopickname, parentname, childname, grapht, parent, parentemail, parentnumber): 
    #creates email for parents who want their child to be picked up
    messagetosend = message(parent, grapht)
    additionalmessage = "Dear " + parentname + ",\n\nThe person picking up your child " + childname + " is " + parenttopickname + ".\n\nTheir phone number is"  + parentnumber + " and their email is " + parentemail + ". \n\nPlease contact them if there are any changes." 
    #adds the customized part of the email
    
    sender = 'schoolrunexpress@gmail.com'
    password = 'etviqzudvdvrocnr'
    reciever = email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, password)
    server.sendmail(sender, reciever, 'Subject: School Run Express\n\n' + additionalmessage + messagetosend + "\n\nThank you for using School Run Express")
    server.quit()
  

def distance(code1, code2): 
    #calaculates the distance to each house using the postcodes
    dist = pgeocode.GeoDistance('GB')
    length =  dist.query_postal_code(code1, code2)
    
    if length == 0.0: 
        #sometimes the length are to small thus it is assume it will take about 2 minutes to drive there
        length = 2
        return(length)

    else:
        return round(length*2) 
        #converts it to time taken to get to the house using the average speed in Winchester

def assigning(): 
    #determines which student goes in which car
    for child in children:
        for parent in parents:
            distance_there = distance(parent["postcode"], child["postcode"])
            child["distancetoparent"].append([distance_there, parent]) 
            #gets all the distances from each child to a potential parent
      
    for child in children:
        child["distancetoparent"] = sorted(child["distancetoparent"], key=lambda x: x[0]) 
        #orders the times from shortest to longest

        while len(child["distancetoparent"]) > 0:
            minparent = child["distancetoparent"][0] 
            #gets the parent who is closest thus the first one
            parent = minparent[1] 

            if parent["avaiableseats"] >= child["noofchildren"]: 
                #check there are enough seats for the number of children the parent has
                parent["collecting"].append(child)
                parent["avaiableseats"] -= child["noofchildren"]
                break

            else:
                child["distancetoparent"].remove(minparent) 
                #if there is not enough seats, removes that parent from the list of potential parents
    
    return parents

def creategraph(parent): 
    #create graph with postcodes and timings
    #the graph is in the form of an adjacency list
    assigning()
    graph = {}
    graph[parent['postcode']] = []

    for child in parent['collecting']: 
        #adds the connection for all the children to the adjacency list for the parent 
        weight = distance(parent['postcode'], child['postcode'])
        graph[parent['postcode']].append([child['postcode'], weight])
    
    for childs in parent['collecting']:   
        #repeats the same for all the children
        graph[childs['postcode']] = []
        weight = distance(parent['postcode'], childs['postcode'])
        graph[childs['postcode']].append([parent['postcode'], weight])
        
        for child in parent['collecting']:
            if childs['postcode'] != child['postcode']:
                weight = distance(childs['postcode'], child['postcode'])
                graph[childs['postcode']].append([child['postcode'], weight])
    
    return graph
 

children = getchildren() 
#stores the dictionary of all the children being picked up in a global variable

parents = getparents() 
#stores the dictionary of all the parents picking up children in a global variable

currentframe = None 
#sets the current frame on the window to none

main() 
#starts the Tkinter to collect all the information

for parent in parents: 
    #starts the processing and sending of data to parents
    grapht = creategraph(parent) 
    #passes the dictionary of parents to create the graph
    sendmailtodrop(parent, grapht) 

    for children in parent['collecting']:
        email = children['email']
        parenttopickname = parent['name']
        parentname = children['parentname']
        childname = children['childrennames']
        parentemail = parent['email']
        number = parent['phonenumber']
        sendmaintopick(email, parenttopickname, parentname, childname, grapht, parent, parentemail, number)



