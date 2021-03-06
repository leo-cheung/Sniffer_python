## Port to service 
## Port 80 - HTTP
## Port 21 - FTP
## Port 443 - HTTPS


import socket, sys
from struct import *
 
#Convert a string of 6 characters of ethernet address into a dash separated hex string
def eth_addr (a) :
  b = "%.2x:%.2x:%.2x:%.2x:%.2x:%.2x" % (ord(a[0]) , ord(a[1]) , ord(a[2]), ord(a[3]), ord(a[4]) , ord(a[5]))
  return b
 
# receive a packet
def CheckIPPacket(ip_packet):
    packet = ip_packet

    #parse ethernet header
    eth_length = 14
     
    eth_header = packet[:eth_length]
    eth = unpack('!6s6sH' , eth_header)
    eth_protocol = socket.ntohs(eth[2])
    #print 'Destination MAC : ' + eth_addr(packet[0:6]) + ' Source MAC : ' + eth_addr(packet[6:12]) + ' Protocol : ' + str(eth_protocol)
 
    #Parse IP packets, IP Protocol number = 8
    if eth_protocol == 8 :
        #Parse IP header
        #take first 20 characters for the ip header
        ip_header = packet[eth_length:20+eth_length]
         
        #now unpack them :)
        iph = unpack('!BBHHHBBH4s4s' , ip_header)
 
        version_ihl = iph[0]
        version = version_ihl >> 4
        ihl = version_ihl & 0xF
 
        iph_length = ihl * 4
 
        ttl = iph[5]
        protocol = iph[6]
        s_addr = socket.inet_ntoa(iph[8]);
        d_addr = socket.inet_ntoa(iph[9]);
 
        #print 'Version : ' + str(version) + ' IP Header Length : ' + str(ihl) + ' TTL : ' + str(ttl) + ' Protocol : ' + str(protocol) + ' Source Address : ' + str(s_addr) + ' Destination Address : ' + str(d_addr)
 
        #TCP protocol
        if protocol == 6 :
            print 'TCP protocol'
            t = iph_length + eth_length
            tcp_header = packet[t:t+20]
 
            #now unpack them :)
            tcph = unpack('!HHLLBBHHH' , tcp_header)
             
            source_port = tcph[0]
            dest_port = tcph[1]
            sequence = tcph[2]
            acknowledgement = tcph[3]
            doff_reserved = tcph[4]
            tcph_length = doff_reserved >> 4
            try:
                app_layer_pro = socket.getservbyport(dest_port,'tcp')
                if app_layer_pro =='https':
                    print 'Application Layer Protocol: ' + 'HTTPS'
                    return app_layer_pro
                elif app_layer_pro =='http':
                    print 'Application Layer Protocol: ' + 'HTTP'
                    return app_layer_pro
                elif app_layer_pro =='ftp':
                    print 'Application Layer Protocol: ' + 'FTP'
                    return app_layer_pro
                #print  'Application Layer Protocol: '+ app_layer_pro +'   Port ' + str(dest_port)
            except :
                pass
            #print 'Source Port : ' + str(source_port) + ' Dest Port : ' + str(dest_port)   +' Sequence Number : ' + str(sequence) + ' Acknowledgement : ' + str(acknowledgement) + ' TCP header length : ' + str(tcph_length)
             
            h_size = eth_length + iph_length + tcph_length * 4
            data_size = len(packet) - h_size
             
            #get data from the packet
            data = packet[h_size:]
             
            #print 'Data : ' + data
 
        #ICMP Packets
        elif protocol == 1 :
            print 'ICMP Packets'
            u = iph_length + eth_length
            icmph_length = 4
            icmp_header = packet[u:u+4]
 
            #now unpack them :)
            icmph = unpack('!BBH' , icmp_header)
             
            icmp_type = icmph[0]
            code = icmph[1]
            checksum = icmph[2]
             
            #print 'Type : ' + str(icmp_type) + ' Code : ' + str(code) + ' Checksum : ' + str(checksum)
             
            h_size = eth_length + iph_length + icmph_length
            data_size = len(packet) - h_size
             
            #get data from the packet
            data = packet[h_size:]
             
            #print 'Data : ' + data
 
        #UDP packets
        elif protocol == 17 :

            print 'UDP packets'
            u = iph_length + eth_length
            udph_length = 8
            udp_header = packet[u:u+8]
 
            #now unpack them :)
            udph = unpack('!HHHH' , udp_header)
             
            source_port = udph[0]
            dest_port = udph[1]
            length = udph[2]
            checksum = udph[3]
#            try:
#                app_layer_pro = socket.getservbyport(dest_port,'udp')
#                print  'Application Layer Protocol: '+ app_layer_pro +'   Port: ' + str(dest_port)
#            except :
#                pass

    
            #print 'Source Port : ' + str(source_port) + ' Dest Port : ' + str(dest_port) + ' Length : ' + str(length) + ' Checksum : ' + str(checksum)
             
            h_size = eth_length + iph_length + udph_length
            data_size = len(packet) - h_size
            print data_size
             
            #get data from the packet
            data = packet[h_size:]
            # Distinguish VoIP and other type of UDP by data length

             
            #print 'Data : ' + data
 
        #some other IP packet like IGMP
        else :
            print 'Protocol other than TCP/UDP/ICMP'
             
