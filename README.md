# Illumio OA

### Coding Environment
- Python3
- Jupyter
 

If you want to run in Jupyter, you can open illumio.ipynb in Jupyter environment.
Otherwise, just run illumio.py. illumio.py already included the test cases in a class.

### Algorithm Design
In the implementation, I use a hashmap which consists of the keys with tuple (direction, connection_type, port) and the values are the array to store the range of the ip.
When inserting a record to the fire wall, we first check the whether the tuple (direction, connection_type, port) matches the keys in the hashmap. Since the fire wall supports multiple ports (22-30), it implies the system should do the forloop to insert the keys. The reason why I plan to do so is the maximum number of the keys is 65536(total ports)*2(inbound, outbound)*2(tcp, udp) which is around 250k. On the other hand, if I choose the ip as a part of the key, the number of the keys increases dramatically (256^4).

#### Merge intervals
Now, after solving the problem of the hashmap design, next challenge in this design is how to manage the range of the ips. Every time inserting a range of ips, the algorithm just goes through the interval list til the interval[i].end >= insertedInterval.start. this means this is the time to consider merging intervals. Next, we use another while loop to check interval[i].start <= insertedInterval.end. This is the intervals we are interested in merging.
The last operation is to push the rest of intervals in the original intervals.
```
    ### Code Snippet
    # insert ip range into a sorted ip range list
    def merge(self, mkey, ip_range):
        newIntervals = []
        size = len(self.type_hash[mkey])
        
        range_start = ip_range[0]
        range_end = ip_range[1]
        i = 0
        while i < size and self.compare(self.type_hash[mkey][i][1], range_start) == -1:
            newIntervals.append(self.type_hash[mkey][i])
            i += 1
        
        merge_start = range_start
        merge_end = range_end
        
        while i < size and self.compare(self.type_hash[mkey][i][0], range_end) <= 0:
            if self.compare(self.type_hash[mkey][i][0], merge_start) == -1:
                merge_start = self.type_hash[mkey][i][0]
            if self.compare(self.type_hash[mkey][i][1], merge_end) == 1:
                merge_end = self.type_hash[mkey][i][1]
            i += 1
        
        newIntervals.append((merge_start, merge_end))
        
        while i < size:
            newIntervals.append(self.type_hash[mkey][i])
            i += 1
        
        self.type_hash[mkey] = newIntervals
```
The time complexity of this merge operation ***takes O(n)***.
n is the # of the elements in the original interval list.

#### Get proper interval
This operation is used in core API ***accept_packet***
Try to find a certain record can pass the firewall is using the following steps:
1. Check tuple (direction, connection_type, port) is in the hashmap or not. If it is go to step 2, otherwise, return false.
2. Use binary search to search the sorted intervals in order to find whether there is a interval includes the ip.

The time complexity of this search is ***O(log n)***.
n is the # of the elements in the original interval list.

### Test Cases
The testcases separate into 2 parts a basic one (test1) and an advanced one (test2).

test1 verifies the following:
- correct matching
- only direction is wrong
- only connection type is wrong
- only port number is wrong
- only ip is not in the ranges

test2 does the same thing, but the only difference between test1 and test2 is the input.
The test2 uses an input csv that verifies the operation of the merging intervals and separating port ranges into several identical keys.

***Example***
```
# with different port ranges and overlapped ip ranges
inbound	tcp	19-22	155.155.155.155-155.155.155.157
inbound	tcp	22	155.155.155.150-155.155.155.160
```

