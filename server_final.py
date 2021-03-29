import socket
import sys
import time
import os
import struct
import hashlib

print "\nWelcome to the FTP server.\n\nTo get started, connect a client."

# Initialise socket stuff
TCP_IP = "127.0.0.1" # Only a local server
TCP_PORT = 1456 # Just a random choice
BUFFER_SIZE = 1024 # Standard size
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
conn, addr = s.accept()

print "\nConnected to by address: {}".format(addr)
\

def index():
    conn.send("1")
    flag_length = struct.unpack("h", conn.recv(2))[0]
    print flag_length
    flag = conn.recv(BUFFER_SIZE)
    print "\nRecieved instruction: {}".format(flag)
    flag1 = str(flag)
    print flag
    conn.send("1")
    start_time_length = struct.unpack("h", conn.recv(2))[0]
    print start_time_length
    start_time = conn.recv(start_time_length)
    print start_time
    conn.send("1")
    end_time_length = struct.unpack("h", conn.recv(2))[0]
    print end_time_length
    end_time = conn.recv(end_time_length)
    print end_time
#    cmd = "find  -newermt 2020-04-24 -not -newermt 2020-04-26 -ls > ax5.txt "  
    if flag.upper() == "SHRT":
        cmd1 = 'find -newermt ' + start_time + ' -not -newermt ' + end_time + ' -name ' + '\'*.pdf\''+ ' -ls > ax5.txt' 
        cmd2 = 'find -newermt ' + start_time + ' -not -newermt ' + end_time + ' -name ' + '\'*.txt\''+ ' -ls >> ax5.txt' 
        print cmd1
        listing = os.system(cmd1)
        listing = os.system(cmd2)
    else:
        cmd1 = 'ls -alt *.txt > ax5.txt'
        #cmd1 = 'grep programmer *.txt -ls '
        print cmd1
        listing = os.system(cmd1)
        #for i in listing:
        #    cmd2 = 'ls -alt' + i + ' >> ax5.txt'
        #    os.system(cmd2)



    file_name = 'ax5.txt' 
    if os.path.isfile(file_name):
      # then the file exists, and send file size
        conn.send(struct.pack("i", os.path.getsize(file_name)))
    else:
        # Then the file doesn't exist, and send error code
        print "File name not valid"
        conn.send(struct.pack("i", -1))
        return
    # Wait for ok to send file
    print "reached here"
    conn.recv(BUFFER_SIZE)
    # Enter loop to send file
    print "reached here"
    start_time = time.time()
    print "reached here"
    print "Sending file..."

    content = open(file_name, "rb")
    # Again, break into chunks defined by BUFFER_SIZE
    l = content.read(BUFFER_SIZE)
    while l:
        conn.send(l)
        l = content.read(BUFFER_SIZE)
    content.close()
    # Get client go-ahead, then send download details
    conn.recv(BUFFER_SIZE)
    conn.send(struct.pack("f", time.time() - start_time))
    return

def dwld():
    conn.send("1")
    flag_name_length = struct.unpack("h", conn.recv(2))[0]
    print flag_name_length
    flag = conn.recv(flag_name_length)
    print flag
    conn.send("1")
    file_name_length = struct.unpack("h", conn.recv(2))[0]
    print file_name_length
    file_name = conn.recv(file_name_length)
    print file_name
    if os.path.isfile(file_name):
        # Then the file exists, and send file size
        conn.send(struct.pack("i", os.path.getsize(file_name)))
    else:
        # Then the file doesn't exist, and send error code
        print "File name not valid"
        conn.send(struct.pack("i", -1))
        return 
    # Wait for ok to send file
    if flag.upper() == "TCP": 
        conn.recv(BUFFER_SIZE)
        print "waiting for acknowledgement for client for TCP"
    # Enter loop to send file
    start_time = time.time()
    print "Sending file..."
    # Again, break into chunks defined by BUFFER_SIZE
    content = open(file_name, "rb")
    l = content.read(BUFFER_SIZE)
    while l:
        conn.send(l)
        l = content.read(BUFFER_SIZE)
    content.close()
    # Get client go-ahead, then send download details
    conn.recv(BUFFER_SIZE)
    conn.send(struct.pack("f", time.time() - start_time))
    
    cmd1 = 'md5sum ' + file_name + '  > ax4.txt' 
    print cmd1
    listing = os.system(cmd1)
    cmd2 = 'date -r ' + file_name + ' >> ax4.txt' 
    print cmd2
    listing = os.system(cmd2)
    file_name1 = 'ax4.txt'
    conn.send("1")
    file_name_length1 = struct.unpack("h", conn.recv(2))[0]
    print file_name_length1
    file_name1 = conn.recv(file_name_length)
    print file_name1
    if os.path.isfile(file_name1):
        # Then the file exists, and send file size
        conn.send(struct.pack("i", os.path.getsize(file_name1)))
    else:
        # Then the file doesn't exist, and send error code
        print "File name not valid"
        conn.send(struct.pack("i", -1))
        return
    # Wait for ok to send file
    # Wait for ok to send file
    conn.recv(BUFFER_SIZE)
    # Enter loop to send file
    start_time = time.time()
    print "Sending file..."
    content = open(file_name1, "rb")
    # Again, break into chunks defined by BUFFER_SIZE
    l = content.read(BUFFER_SIZE)
    print l
    while l:
        print "reached here server1"
        conn.send(l)
        l = content.read(BUFFER_SIZE)
    content.close()
    print "reached here server1"
    # Get client go-ahead, then send download details
    conn.recv(BUFFER_SIZE)
    conn.send(struct.pack("f", time.time() - start_time))
    return

def FileHash():
    conn.send("1")
    flag_length = struct.unpack("h", conn.recv(2))[0]
    #print  flag_length
    flag = conn.recv(BUFFER_SIZE)
    #print "\nRecieved instruction: {}".format(flag)
    flag1 = str(flag)
    #print flag
    conn.send("1")
    if flag.upper()=="VERI":
        file_name_length = struct.unpack("h", conn.recv(2))[0]
        #print file_name_length
        file_name = conn.recv(file_name_length)
        #print file_nameMonth
        if os.path.isfile(file_name):
      # Then the file exists, and send lastmodified and checksum
            conn.send( last_modified_fileinfo(file_name))
            conn.send( hashlib.md5(file_name).hexdigest())
        else:
        # Then the file doesn't exist, and send error code
        #print "File name not valid"
            conn.send(struct.pack("i", -1))
        return
    if flag.upper()=="CHCK":
        listOfFiles = os.listdir('.')
        conn.send(struct.pack("i", len(listOfFiles)))
        for i in listOfFiles:
            conn.send(struct.pack("i", sys.getsizeof(i)))
            conn.send(i)
            conn.recv(BUFFER_SIZE)
            list1 = last_modified_fileinfo(i)
            conn.send(struct.pack("i", sys.getsizeof(list1)))
            conn.send(list1)
            conn.recv(BUFFER_SIZE)
            list2= hashlib.md5(i).hexdigest()
            conn.send(struct.pack("i", sys.getsizeof(list2)))
            conn.send(list2)
            conn.recv(BUFFER_SIZE)

    return
                
        
        
def last_modified_fileinfo(filepath):
    filestat = os.stat(filepath)

    date = time.localtime((filestat.st_mtime))
    # Extract year, month and day from the date\
    year = date[0]
    month = date[1]
    day = date[2]
    # Extract hour, minute, second
    hour = date[3]
    minute = date[4]
    second = date[5]
    
    # Year
    strYear = str(year)[0:]
    # Month
    if (month <=9):
        strMonth = '0' + str(month)
        
    else:
        strMonth = str(month)

        # Date
    if (day <=9):
        strDay = '0' + str(day)
    else:
        strDay = str(day)
    return (strYear+"-"+strMonth+"-"+strDay+" "+str(hour)+":"+str(minute)+":"+str(second))

def quit():
    # Send quit conformation
    conn.send("1")
    # Close and restart the server
    conn.close()
    s.close()
    os.execl(sys.executable, sys.executable, *sys.argv)

while True:
    # Enter into a while loop to recieve commands from client
    print "\n\nWaiting for instruction"
    data = conn.recv(BUFFER_SIZE)
    print "\nRecieved instruction: {}".format(data)
    # Check the command and respond correctly
    if data == "DWLD":
        dwld()
    elif data == "INDEX":
        index()
    elif data == "HASH":
        FileHash()
    elif data == "QUIT":
        quit()
    # Reset the data to loop
    data = None
