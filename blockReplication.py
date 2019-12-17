from common import CreateDisk
from common import DeleteDisk
from common import writeToDisk
from common import readFromDisk
from common import A
from common import B
from common import empty
import random
from common import disks

Backup = [""] * 500
empty_bck = [1] * 500
replicated = {}
bad_block = {}


def read_with_replicate(id, block_no1):
    if id not in disks.keys():
        raise Exception("Disk " + id + " does not exist")
    block_no = block_no1
    random_num = random.randrange(1, 20)
    disk  = disks[id]
    disk_size = disk[0]
    fragments = disk[1]
    if block_no > disk_size and block_no <= 0:
        raise Exception("Block no is outside the disk")
    blockn = fragments[0][0]
    i = 0
    while block_no > 0:
        size_of_fragment = fragments[i][1] - fragments[i][0] + 1
        if size_of_fragment >= block_no:
            blockn = fragments[i][0] + block_no - 1
            block_no = 0
        else:
            block_no -= size_of_fragment
        i += 1
    if(random_num < 10):
        print("A bad block")
        empty[blockn] = 2
        copy = replicated[blockn]
        print("Reading from " + str(copy) + " in backup")
        text = Backup[copy]
        
        for i in range(500):
            if(empty_bck[i] == 1):
                print("Replicating this block at " + str(i))
                bad_block[blockn] = i
                Backup[i] = text
                empty_bck[i] = 0
                break
        print(text)
    else:
        if(empty[blockn] != 2):
            text = readFromDisk(id, block_no1)
        else:

            text = Backup[bad_block[blockn]]
    print(replicated)
    print(bad_block)
    return text


def write_with_replicate(id, block_no1, block_info):
    if id not in disks.keys():
        raise Exception("Disk " + id + " does not exist")
    block_no = block_no1
    disk  = disks[id]
    disk_size = disk[0]
    fragments = disk[1]
    if block_no > disk_size and block_no <= 0:
        raise Exception("Block no is outside the disk")
    blockn = fragments[0][0]
    i = 0
    while block_no > 0:
        size_of_fragment = fragments[i][1] - fragments[i][0] + 1
        if size_of_fragment >= block_no:
            blockn = fragments[i][0] + block_no - 1
            block_no = 0
        else:
            block_no -= size_of_fragment
        i += 1
    if(empty[blockn] != 2):
        print("Not a bad block")
        writeToDisk(id, block_no1, block_info)
        if(blockn in replicated.keys()):
            print("Already replicated")
            Backup[replicated[blockn]] = block_info
        else:
            for i in range(500):
                if(empty_bck[i] == 1):
                    replicated[blockn] = i
                    Backup[i] = block_info
                    print("Creating replication at " + str(i) + " in backup")
                    empty_bck[i] = 0
                    break
    else:
        Backup[replicated[blockn]] = block_info
        Backup[bad_block[blockn]] = block_info
    print(replicated)
    print(bad_block)
                

while True:
    print("Enter Your Choice from the below options:")
    print("1. create Disk")
    print("2. delete Disk")
    print("3. write to Disk")
    print("4. read from Disk")
    print("5. exit")
    n = int(input())
    if n == 1:
        try:
            id = str(input("Enter the id for creating a new Disk : "))
            num_blocks = int(input("Enter the number of blocks to allocate : "))
            CreateDisk(id, num_blocks)
        except Exception as e:
            print(e)
    elif n == 2:
        try:
            id = str(input("Enter the Disk Id to delete : "))
            DeleteDisk(id)
        except Exception as e:
            print(e)
    elif n == 3:
        try:
            id = str(input("Enter the id of Disk : "))
            block_no = int(input("Enter the block number to write : "))
            block_info = str(input("Enter the block info : "))
            write_with_replicate(id,block_no, block_info)
        except Exception as e:
            print(e)
    elif n == 4:
        try:
            id = str(input("Enter the id of Disk : "))
            block_no = int(input("Enter the block number to read : "))
            read_with_replicate(id,block_no)
        except Exception as e:
            print(e)
    elif n == 5:
        break
    else:
        print("Please enter the correct number.")
