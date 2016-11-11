# Table of Contents

1. [Challenge Summary] (README.md#challenge-summary)
2. [Runtime Environment] (README.md#runtime-environment)
3. [Details of Implementation] (README.md#details-of-implementation)

##Challenge Summary

PayMo is a company that allows users to easily request and make payments to other PayMo users. The team at PayMo has decided they want to implement features to prevent fraudulent payment requests from untrusted users. When users make a payment, they'll be notified when the other user is outside of their "nth-degree network". The tasks of this project is to 

*Process the historical data to create an intial network structure.
*Process the simulated transaction data to identify the unverified transactions and update the network.
 
The challenge of this taks includes:

*The size of the data could be very large, despite there are 3 million recorders each in batch data and stream data. As PayMo and the number of the members grow, the scalability of the process is challenged.
*The processing time should be short enough, so the member would not have to wait for approval.  

##Runtime Environment

[Back to Table of Contents] (README.md#table-of-contents)

The program is writen and tested in Python 3.5 under Linux Ubuntu 14.04. The memory usage should not over 8 GB. No extra library is used.

##Details of implementation

[Back to Table of Contents] (README.md#table-of-contents)

A 'dictionary' is used to store the network for the fairly fast search time during reading. Each appeared member holds an item in the dictionary, and the key is the member's id. The member's first degree friends's ids are store as value of the item in 'set', because 'set' automatically removes duplicates. This data structure saves time when searching friends and saves memory usage. Since the ids are all integter, an 'array' was considered to replace the 'dictionary'. Due lack of flexibility and the complexity of using, it would tried out after this challenge.

The program processes the input data line by line. One line in batch data will trigger an update of the network, if two sides of the transaction are not the first degree friends before. For example, the network before a line of data comes is:

    {1:{2,3},2:{1},3,{1}}

*4,1 arrives. 4 is added to 1's set, and a new item is added for 4

    {1:{2,3,4},2:{1},3,{1},4:{1}}

*2,3 arrives. Only 2 and 3's set is updated, and no item is added

    {1:{2,3,4},2:{1,3},3,{1,2},4:{1}}   

*1,2 arrives. Since they are the first degree firends, so no change

The program processes the stream data also line by line. It will read one line of the input, check for friendship, write one line of output, and update the network. This program checks the 1st, 2nd, and 4th degree friendship at same time, which is not suitable for the production. For the faster processing, the program should only hanld one case, and network update should be also handled separately.

 


