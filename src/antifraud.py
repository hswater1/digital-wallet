# -*- coding: utf-8 -*-


#store network
def add_trans(id_1,id_2, network):
    '''generate netowrk'''
    temp1=network.get(id_1,set())
    temp2=network.get(id_2,set())
    temp1.add(id_2)
    temp2.add(id_1)
    network[id_1]=temp1
    network[id_2]=temp2
    return network


#check connection within n degrees
def find_trustees(id_1,id_2,network,depth):
    '''check whether two ids are connect in maximum (depth)th degree.'''
    #check for new member. If an id has no friend yet, it return False
    temp1=network.get(id_1,False)
    if not temp1:
        return False
    temp2=network.get(id_2,False)
    if not temp2:
        return False
        
    #check direct friends
    if len(temp1)<=len(temp2):
        if id_2 in temp1:
            return True
        #this variable store current and previous level friends
        prev1=temp1.union(set([id_1]))
        id_1=temp1
        id_2=set([id_2])
        prev2=id_2
    else:
        if id_1 in temp2:
            return True
        prev2=temp2.union(set([id_2]))     
        id_1=set([id_1])
        id_2=temp2
        prev1=id_1

    #check for 2+ degree friends
    for i in range(2,depth+1):
        #choose the side with less friends
        if len(id_1)<=len(id_2):
            #get next level friends
            temp=set()
            for mem in id_1:
                temp.update(network.get(mem,set()))
            #if found connection then returns True
            if bool(id_2.intersection(temp)):
                return True
            #remove current and previous level friend
            temp=temp-prev1
            #If no new friends found return False
            if not(temp):
                return False
            #move to next level
            id_1=temp
            prev1.update(temp)

        else:
            temp=set()
            for mem in id_2:
                temp.update(network.get(mem,set()))
            if bool(id_1.intersection(temp)):
                return True
            temp=temp-prev2
            if not(temp):
                return False
            id_2=temp
            prev2.update(temp)
            
    return False 
    
    
#process batch data to generant network
    
def proc_batch(network, batch_path):
    
    total=0
    batch_file=open(batch_path,"r")   
    batch_file.readline()
    
    while 1:
        line=batch_file.readline().strip()
        if line=='':
            break
        try:
            arr = line.split(",")
            id_1=int(arr[1])
            id_2=int(arr[2])
            if id_1!=id_2:
                network=add_trans(id_1,id_2,network)
        except:
            continue
        
        total+=1
        if total%1000000==0:
            print(total)
    batch_file.close()
    
    return network

    
#start processing stream data to get output
def proc_stream(network,  stream_path, output_path1, output_path2, output_path3):
    total=0
    stream_file=open(stream_path,"r")
    out_file1=open(output_path1,"w")
    out_file2=open(output_path2,"w")
    out_file3=open(output_path3,"w")
    stream_file.readline()
    while 1:
        line=stream_file.readline().strip()
        if line=='':
            break
       
        try:
            arr = line.split(",")
            if len(arr)<2:
                continue
            id_1=int(arr[1])
            id_2=int(arr[2])
            if id_1==id_2:
                out_file1.write("trusted\n")
                out_file2.write("trusted\n")
                out_file3.write("trusted\n")
            else:
                
                if find_trustees(id_1,id_2,network,1):
                    out_file1.write("trusted\n")
                else:
                    out_file1.write("unverified\n")
                    
                if find_trustees(id_1,id_2,network,2):
                    out_file2.write("trusted\n")
                else:
                    out_file2.write("unverified\n")
                    
                if find_trustees(id_1,id_2,network,4):
                    out_file3.write("trusted\n")
                else:
                    out_file3.write("unverified\n")
                network=add_trans(id_1,id_2,network)
        except Exception as e:
            continue
        
        total+=1
        if total%1000000==0:
            print(total)
        
    stream_file.close()
    out_file1.close()
    out_file2.close()
    out_file3.close()
    
    return network
    
    
import time
import sys
args=sys.argv
if len(args) > 1:
    batch_path=args[1] 
    stream_path=args[2]
    output_path1=args[3]
    output_path2=args[4]
    output_path3=args[5]
else:
    
    #assign paths as defualt. 
    batch_path="../paymo_input/batch_payment.txt"
    stream_path="../paymo_input/stream_payment.txt"
    output_path1="../paymo_output/output1.txt"
    output_path2="../paymo_output/output2.txt"
    output_path3="../paymo_output/output3.txt"


start_time = time.time()
start_time=time.time()    
network=proc_batch(dict(), batch_path)
print("--- %s minutes to process batch data---" % round(((time.time() - start_time)/60),2))
start_time = time.time()
network=proc_stream(network, stream_path, output_path1, output_path2, output_path3)
print("--- %s minutes to process stream data---" % round(((time.time() - start_time)/60),2))
