
# coding: utf-8

# In[3]:

import csv
import os.path


# In[72]:

class Firewall(object):
    def __init__(self, csv_file):
        self.type_hash = {}
        if not os.path.isfile(csv_file):
            raise Exception("File not existed")
            
        with open(csv_file) as csvf:
            csv_reader = csv.reader(csvf, delimiter=',')
            for row in csv_reader:
                # get data by columns
                direction = row[0]
                ctype = row[1]
                port_range = row[2]
                ip_range = row[3]

                # if is multiple ports
                multiple_port = False
                if "-" in port_range:
                    multiple_port = True

                if multiple_port:
                    start_port, end_port = port_range.split("-")
                else:
                    start_port = port_range
                    end_port = port_range
                
                # iterate ip to create unique hashmap (direction, connection type, port)
                start_port = int(start_port)
                end_port = int(end_port)
                
                # if is multiple ips
                multiple_ip = False
                if "-" in ip_range:
                    multiple_ip = True
                if multiple_ip:
                    start_ip, end_ip = ip_range.split("-")
                else:
                    start_ip = ip_range
                    end_ip = ip_range
                    
                for port in range(start_port, end_port+1):
                    if self.type_hash.get((direction, ctype, port), None) is None:
                        self.type_hash[(direction, ctype, port)] = [(start_ip, end_ip)]
                    else:
                        self.merge((direction, ctype, port), (start_ip, end_ip))
        
    # compare string ip
    def compare(self, ip1, ip2):
        if ip1 == ip2:
            return 0
        ip1_list = list(map(lambda x : int(x), ip1.split(".")))
        ip2_list = list(map(lambda x : int(x), ip2.split(".")))
        size = len(ip1_list)
        for i in range(0, size):
            if ip1_list[i] < ip2_list[i]:
                return -1
            elif ip1_list[i] > ip2_list[i]:
                return 1        
        return 0

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
    
    def accept_packet(self, direction, connection_type, port, ip):
        if self.type_hash.get((direction, connection_type, port), None) is None:
            return False
        if self.search((direction, connection_type, port), ip):
            return True
        return False
    
    # binary search to see if the ip is in a certain interval
    def search(self, mkey, ip):
        ip_ranges = self.type_hash[mkey]
        l = 0
        r = len(ip_ranges) - 1
        while l <= r:
            mid = int(l + (r-l)/2)
            cur_start = ip_ranges[mid][0]
            cur_end = ip_ranges[mid][1]
            # in range
            if self.compare(ip, cur_start) >= 0 and self.compare(ip, cur_end) <= 0:
                return True
            elif self.compare(ip, cur_start) < 0:
                r = mid - 1
            else:
                l = mid + 1
        
        return False
        


# In[84]:

# For unit test cases
class TestCase(object):
    def __init__(self):
        self.fw1 = Firewall("testcase.csv")
        self.fw2 = Firewall("testcase2.csv")
    
    def test1(self):
        # base case in IP range
        assert self.fw1.accept_packet('inbound', 'tcp', 22, "155.155.155.160") == True
        # IP not in range but rest of the info are matched
        assert self.fw1.accept_packet('inbound', 'tcp', 22, "155.155.155.161") == False
        assert self.fw1.accept_packet('inbound', 'tcp', 22, "155.155.155.149") == False
#         # connection type is wrong
        assert self.fw1.accept_packet('inbound', 'udp', 22, "155.155.155.155") == False
#         # direction is wrong
        assert self.fw1.accept_packet('outbound', 'udp', 22, "155.155.155.155") == False
    
    # more complicated csv file
    def test2(self):
         # base case in IP range
        assert self.fw2.accept_packet('inbound', 'tcp', 22, "155.155.155.145") == True
        # IP not in range but rest of the info are matched
        assert self.fw2.accept_packet('inbound', 'tcp', 22, "155.155.155.130") == False
        assert self.fw2.accept_packet('inbound', 'tcp', 22, "155.155.155.171") == False
#         # connection type is wrong
        assert self.fw2.accept_packet('inbound', 'udp', 22, "155.155.155.155") == False
#         # direction is wrong
        assert self.fw2.accept_packet('outbound', 'tcp', 22, "155.155.155.155") == False


# In[85]:

test = TestCase()
test.test1()
test.test2()


# In[ ]:



