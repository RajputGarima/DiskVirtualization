from common import CreateDisk
from common import DeleteDisk
from common import num_Available_Blocks
from common import disks
from common import available_blocks
from common import readFromDisk
from common import writeToDisk
from common import createCheckpoint
from common import RollBack


while True:
    print("Enter Your Choice from the below options:")
    print("1. create Disk")
    print("2. delete Disk")
    print("3. write to Disk")
    print("4. read from Disk")
    print("5. create checkpoint")
    print("6. roll back")
    print("7. exit")
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
            writeToDisk(id,block_no, block_info)
        except Exception as e:
            print(e)
    elif n == 4:
        try:
            id = str(input("Enter the id of Disk : "))
            block_no = int(input("Enter the block number to read : "))
            readFromDisk(id,block_no)
        except Exception as e:
            print(e)
    elif n == 5:
        try:
            id = str(input("Enter the id of Disk : "))
            print(createCheckpoint(id))
        except Exception as e:
            print(e)
    elif n == 6:
        try:
            id = str(input("Enter the id of Disk : "))
            state = int(input("Enter checkpoint number: "))
            RollBack(id, state)
        except Exception as e:
            print(e)
    elif n == 7:
        break
    else:
        print("Please enter the correct number.")
