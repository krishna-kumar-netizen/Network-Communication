import socket
import sys
import os
import struct
import dircache
import time

# Initialise socket stuff
TCP_IP = "127.0.0.1" # Only a local server
TCP_PORT = 1456 # Just a random choice
BUFFER_SIZE = 1024 # Standard chioce
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def conn():
    # Connect to the server
    print "Sending server request..."
    try:
        s.connect((TCP_IP, TCP_PORT))
        print "Connection sucessful"
    except:
        print "Connection unsucessful. Make sure the server is online."

def upld(file_name):
    # Upload a file
    print "\nUploading file: {}...".format(file_name)
    try:
        # Check the file exists
        content = open(file_name, "rb")
    except:
        print "Couldn't open file. Make sure the file name was entered correctly."
        return
    try:
        # Make upload request
        s.send("UPLD")
    except:
        print "Couldn't make server request. Make sure a connection has bene established."
        return
    try:
        # Wait for server acknowledgement then send file details
        # Wait for server ok
        s.recv(BUFFER_SIZE)
        # Send file name size and file name
        s.send(struct.pack("h", sys.getsizeof(file_name)))
        s.send(file_name)
        # Wait for server ok then send file size
        s.recv(BUFFER_SIZE)
        s.send(struct.pack("i", os.path.getsize(file_name)))
    except:
        print "Error sending file details"
    try:
        # Send the file in chunks defined by BUFFER_SIZE
        # Doing it this way allows for unlimited potential file sizes to be sent
        l = content.read(BUFFER_SIZE)
        print "\nSending..."
        while l:
            s.send(l)
            l = content.read(BUFFER_SIZE)
        content.close()
        # Get upload performance details
        upload_time = struct.unpack("f", s.recv(4))[0]
        upload_size = struct.unpack("i", s.recv(4))[0]
        print "\nSent file: {}\nTime elapsed: {}s\nFile size: {}b".format(file_name, upload_time, upload_size)
    except:
        print "Error sending file"
        return
    return


def Index_get(flag,arg1,arg2):

    print arg1
    print arg2
    # List the files avaliable on the file server
    # Called list_files(), not list() (as in the format of the others) to avoid the standard python function list()
    print "Requesting files...\n"
    try: 
        # Send list request
        s.send("INDEX")
    except:
        print "Couldn't make server request. Make sure a connection has bene established."
        return
    try:
        # First get the number of files in the directory
        s.recv(BUFFER_SIZE)
        s.send(struct.pack("h", sys.getsizeof(flag)))
        s.send(flag)
        s.recv(BUFFER_SIZE)
        s.send(struct.pack("h", sys.getsizeof(arg1)))
        s.send(arg1)
        s.recv(BUFFER_SIZE)
        s.send(struct.pack("h", sys.getsizeof(arg2)))
        s.send(arg2)
        #if flag == 0:
        #    s.send(struct.pack("h", sys.getsizeof(arg1)))
        #    s.send(arg1)
        #    s.send(struct.pack("h", sys.getsizeof(arg2)))
        #    s.send(arg2)
        #    s.send(struct.pack("h", sys.getsizeof(arg3)))
        #    s.send(arg3)
        #number_of_files = struct.unpack("i", s.recv(4))[0]
        # Then enter into a loop to recieve details of each, one by one
    except:
        print "Couldn't retrieve listing"
        return
    print "reached here"
    file_name = 'ax2.txt'
    try:
        # Send ok to recieve file content
        s.recv(BUFFER_SIZE)
        #s.send("1")
        # Enter loop to recieve file
        output_file = open(file_name, "wb")
        bytes_recieved = 0
        print "\nDownloading..."
        while bytes_recieved < file_size:
            # Again, file broken into chunks defined by the BUFFER_SIZE variable
            l = s.recv(BUFFER_SIZE)
            output_file.write(l)
            bytes_recieved += BUFFER_SIZE
        output_file.close()
        print "Successfully downloaded {}".format(file_name)
        # Tell the server that the client is ready to recieve the download performance details
        # Get performance details
        time_elapsed = struct.unpack("f", s.recv(4))[0]
        print "Time elapsed: {}s\nFile size: {}b".format(time_elapsed, file_size)
    except:
        print "could not download"
        return
    try:
        # Final check
        s.send("1")
        return
    except:
        print "Couldn't get final server confirmation"
        return

def index1(flag,start_time,end_time):
    print flag
    print start_time
    print end_time
    # Download given file
    #print "Downloading file: {}".format(file_name)
    try:
        # Send server request
        s.send("INDEX")
    except:
        print "Couldn't make server request. Make sure a connection has bene established."
        return
    try:
        # Wait for server ok, then make sure file exists
        s.recv(BUFFER_SIZE)
        s.send(struct.pack("h", sys.getsizeof(flag)))
        s.send(flag)
        s.recv(BUFFER_SIZE)
        # Send file name length, then name
        s.send(struct.pack("h", sys.getsizeof(start_time)))
        s.send(start_time)
        s.recv(BUFFER_SIZE)
        s.send(struct.pack("h", sys.getsizeof(end_time)))
        s.send(end_time)
        # Get file size (if exists)
        file_size = struct.unpack("i", s.recv(4))[0]
        #if file_size == -1:
            # If file size is -1, the file does not exist
        #    print "File does not exist. Make sure the name was entered correctly"
        #    return
    except:
        print "Error checking file"
    try:
        # Send ok to recieve file content
        s.send("1")
        # Enter loop to recieve file
        file_name = 'result.txt'
        output_file = open(file_name, "wb")
        bytes_recieved = 0
        print "\nDownloading..."
        while bytes_recieved < file_size:
            # Again, file broken into chunks defined by the BUFFER_SIZE variable
            l = s.recv(BUFFER_SIZE)
            output_file.write(l)
            bytes_recieved += BUFFER_SIZE
        output_file.close()
        print "Successfully downloaded {}".format(file_name)
        # Tell the server that the client is ready to recieve the download performance details
        s.send("1")
        # Get performance details
        time_elapsed = struct.unpack("f", s.recv(4))[0]
        print "Time elapsed: {}s\nFile size: {}b".format(time_elapsed, file_size)
    except:
        print "Error downloading file"
        return
    cmd2 = 'cat ' + file_name
    list1= os.system(cmd2)
    print list1
    return

def dwld(flag,file_name):
    # Download given file
    
    print "Downloading file: {}".format(file_name)
    try:
        # Send server request
        s.send("DWLD")
    except:
        print "Couldn't make server request. Make sure a connection has bene established."
        return
    try:
        # Wait for server ok, then make sure file exists
        s.recv(BUFFER_SIZE)
        # Send file name length, then name
        s.send(struct.pack("h", sys.getsizeof(flag)))
        s.send(flag)
        # Wait for server ok, then make suree file exists
        s.recv(BUFFER_SIZE)
        # Send file name length, then name
        s.send(struct.pack("h", sys.getsizeof(file_name)))
        s.send(file_name)
        # Get file size (if exists)
        file_size = struct.unpack("i", s.recv(4))[0]
        if file_size == -1:
            # If file size is -1, the file does not exist
            print "File does not exist. Make sure the name was entered correctly"
            return
    except: 
        print "Error checking file"
    try:
        # Send ok to recieve file content
        if flag.upper() == "TCP":
            s.send("1")
            print "send ok to receive  server in case of TCP"

        # Enter loop to recieve file
        print "\nDownloading.\.."
        output_file = open(file_name, "wb")
        print "\nDownloading.\.."
        cached_file = open('./cache/' + file_name, 'wb')
        print "\nDownloading.\.."
        bytes_recieved = 0
        print "\nDownloading.\.."
        while bytes_recieved < file_size:
            # Again, file broken into chunks defined by the BUFFER_SIZE variable
            l = s.recv(BUFFER_SIZE)
            output_file.write(l)
            cached_file.write(l)
            bytes_recieved += BUFFER_SIZE
        output_file.close()
        print "Successfully downloaded {}".format(file_name)
        # Tell the server that the client is ready to recieve the download performance details
        s.send("1")
        # Get performance details
        time_elapsed = struct.unpack("f", s.recv(4))[0]
        print "Time elapsed: {}s\nFile size: {}b".format(time_elapsed, file_size)
    except:
        print "Error downloading file"
        return

    file_name1 = 'ax4.txt'
    try:
        # Wait for server ok, then make sure file exists
        s.recv(BUFFER_SIZE)
        # Send file name length, then name
        s.send(struct.pack("h", sys.getsizeof(file_name1)))
        s.send(file_name1)
        # Get file size (if exists)
        file_size1 = struct.unpack("i", s.recv(4))[0]
        if file_size == -1:
            # If file size is -1, the file does not exist

            print "File does not exist. Make sure the name was entered correctly"
            return
    except:
        print "Error checking file"
    try:
        # Send ok to recieve file content
        s.send("1")
        # Enter loop to recieve file
        output_file = open(file_name1, "wb")
        print file_name1
        bytes_recieved = 0
        print "\nDownloading..."
        while bytes_recieved < file_size1:
            # Again, file broken into chunks defined by the BUFFER_SIZE variable
            l = s.recv(BUFFER_SIZE)
            output_file.write(l)
            bytes_recieved += BUFFER_SIZE
        output_file.close()
        print "Successfully downloaded {}".format(file_name1)
        # Tell the servrier that the client is ready to recieve the download performance details
        s.send("1")
        # Get performance details
        time_elapsed = struct.unpack("f", s.recv(4))[0]
        print "Time elapsed: {}s\nFile size: {}b".format(time_elapsed, file_size)
    except:
        print "Error downloading file"
        return
    cmd2 = 'cat ' + file_name1
    list1= os.system(cmd2)
    print list1
    print file_size
    cmds = 'du -s '
    listOfFiles = os.listdir('./cache')
    preventry = file_name
    filestat1 = os.stat(file_name)
    prev = time.localtime((filestat1.st_mtime))
    #print prev
    total_size = 0
    for i in listOfFiles:
        filestat = os.stat(i)
        date = time.localtime((filestat.st_mtime))
        total_size+= sys.getsizeof(i)
    #    print date
        if date < prev:
            print date
            prev = date
            preventry = i
           # prev = i 
    print preventry
    cmddir = 'cd ./cache'
    os.system(cmddir)
    size1 = os.system(cmds)
    print total_size
    if total_size > 200:
        cmd1 = 'rm ./cache/' + preventry
        print "delete"
        os.system(cmd1)

    return


def verify(file_name):
    try:
    # Check if we have this file locally
        content= open('./cache/' + file_name)
        output_file = open(file_name, "wb")
        l = content.read()
        output_file.write(l)
        #content = fin.read()
        #fin.close()
        # If we have it, let's send it
        print "found in cache"
        print "downlading from  cache"
    except IOError:
        print "not in cache, reading from server"
        dwld("TCP",file_name)
 
    return
def show():
    print "show"
    dir = './cache'
    list1 = os.listdir(dir)
    print list1

    return

def FileHash(flag,filename):
    #print flag
   # print filename
    try:
        s.send("HASH")
    except:
        print "Couldn't make server request. Make sure a connection has bene established."
        return
    try:
        s.recv(BUFFER_SIZE)
        s.send(struct.pack("h", sys.getsizeof(flag)))
        s.send(flag)
        s.recv(BUFFER_SIZE)
        if flag.upper()=="VERI":
            print "reached VERI"
            s.send(struct.pack("h", sys.getsizeof(filename)))
            s.send(filename)
            print s.recv(BUFFER_SIZE)
            print s.recv(BUFFER_SIZE)
        if flag.upper()=="CHCK":
             number_of_files = struct.unpack("i", s.recv(4))[0]
             for i in range(int(number_of_files)):
                file_name_size = struct.unpack("i", s.recv(4))[0]
                file_name = s.recv(file_name_size)
                print file_name
                s.send("1")
                date_size = struct.unpack("i", s.recv(4))[0]
                date_mod = s.recv(date_size)
                print date_mod
                s.send("1")
                check_sum_size = struct.unpack("i", s.recv(4))[0]
                check_sum = s.recv(check_sum_size)
                print check_sum
                print "\n"
                s.send("1")
            #while s.recv(BUFFER_SIZE)!="done":
	#	print  s.recv(BUFFER_SIZE)
        #        print "\n"
            #conn.send(las
        #        print  s.recv(BUFFER_SIZE)
        #        print "\n"
    except:
        print "Error getting the details"
        return
    return

def quit():
    s.send("QUIT")
    # Wait for server go-ahead
    s.recv(BUFFER_SIZE)
    s.close()
    print "Server connection ended"  
    return

print "\n\nWelcome to the IIIT FTP client.\n\nCall one of the following functions:\nCONN           : Connect to server\nDWLD file_name : Download file\nINDE           : file_path : INDEX short or long with time stamps file\n CACH        : to verify and cache contents \n HASH        : to verify last modificationkrishna@krishna-Surface-Pro \nQUIT           : Exit"

while True:
    # Listen for a command
    prompt = raw_input("\nEnter a command: ")
    if prompt[:4].upper() == "CONN":
        conn()
    elif prompt[:4].upper() == "INDE":
        if prompt[5:9].upper() == "SHRT":
            index1(prompt[5:9],prompt[10:20],prompt[21:])
        else:
            index1(prompt[5:9],'NULL','NULL')

    elif prompt[:4].upper() == "DWLD":
        dwld(prompt[5:8],prompt[9:])
    elif prompt[:4].upper() == "HASH":
        if prompt[5:9].upper() == "VERI":
            FileHash(prompt[5:9],prompt[10:])
        else:
            FileHash(prompt[5:9],'NULL')
    elif prompt[:4].upper() == "CACH":
        print prompt[5:9].upper()
        if prompt[5:9].upper() == "VERI":
            verify(prompt[10:])
        else:
            show()
    elif prompt[:4].upper() == "QUIT":
        quit()
        break
    else:
        print "Command not recognised; please try again"

