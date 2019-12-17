BLOCK_SIZE = 100
A = [""] * 200
B = [""] * 300
empty = [1] * 500
stacks = {}

def read(block_no):
    block_no = block_no - 1
    if(block_no < 0 or block_no > 499):
        raise ValueError("Block index out of bound")
    if(empty[block_no] == 1):
        raise Exception("Empty block")
    if(block_no > 199):
        text = B[block_no - 200]
    else:
        text = A[block_no]
    return text

def write(block_no, block_info):
    block_no = block_no - 1
    if(block_no < 0 or block_no > 499):
        raise ValueError("Block index out of bound")
    if(len(block_info) > BLOCK_SIZE):
        raise Exception("Block size limit exceeded")
    if(block_no > 199):
        B[block_no - 200] = block_info
    else:
        A[block_no] = block_info 
    empty[block_no] = 0

disks ={}
available_blocks = [(0,499)]
num_Available_Blocks = 500


def CreateDisk(id, num_blocks):
    global num_Available_Blocks
    if num_blocks > num_Available_Blocks:
        print("Space Availabe : " + str(num_Available_Blocks))
        raise Exception("Disk Space Exhausted")
    if id in disks.keys():
        raise Exception("Disk : " + str(id) + " already exists")
    disks[id] = (num_blocks,[])
    while(num_blocks>0):
        size_interval = available_blocks[0][1] - available_blocks[0][0] + 1
        if size_interval == num_blocks:
            disks[id][1].append(available_blocks[0])
            available_blocks.pop(0)
            num_Available_Blocks -= num_blocks
            num_blocks = 0
        elif size_interval > num_blocks:
            disks[id][1].append((available_blocks[0][0],available_blocks[0][0]+num_blocks-1))
            num_Available_Blocks -= num_blocks
            available_blocks[0] = (available_blocks[0][0]+num_blocks,available_blocks[0][1])
            num_blocks = 0
        else:
            disks[id][1].append(available_blocks[0])
            num_Available_Blocks -= size_interval
            num_blocks -= size_interval
            available_blocks.pop(0)
    print("Space Available is : " + str(num_Available_Blocks))
    print("Disks Details : " , disks)
    print("available blocks", available_blocks)

def DeleteDisk(id):
    global num_Available_Blocks
    global available_blocks
    if id not in disks.keys():
        raise Exception("Disk : " + id + " does not exist.")
    size_disk = disks[id][0]
    fragments = disks[id][1]
    print(size_disk, fragments)
    num_Available_Blocks += size_disk

    # merging the alloted disk to available_Disk
    available_blocks = available_blocks + fragments
    available_blocks.sort()

    i = 0
    while(True):
        if(i == len(available_blocks)-1):
            break
        if(available_blocks[i][1] == available_blocks[i+1][0] - 1):
            first = available_blocks.pop(i)
            second = available_blocks.pop(i)
            available_blocks.insert(i,(first[0],second[1]))
        else:
            i = i+1
    for j in fragments:
        for block_no in range(j[0],j[1]+1):
            if(block_no > 199):
                B[block_no - 200] = ""
            else:
                A[block_no] = ""
            if(empty[block_no] == 0):
                empty[block_no] = 1
    del disks[id]
    if id in stacks.keys():
        del stacks[id]
    print("Space Available is : " + str(num_Available_Blocks))
    print("Disks Details : " , disks)
    print("available blocks", available_blocks)

def writeToDisk(id, block_no , block_info):
    if id not in disks.keys():
        raise Exception("Disk " + id + " does not exist")
    if(block_no <= 0):
        raise Exception("Invalid block number")
    disk  = disks[id]
    disk_size = disk[0]
    fragments = disk[1]
    if block_no > disk_size:
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
    print(blockn)
    write(blockn + 1,block_info)
    return

def readFromDisk(id, block_no):
    if id not in disks.keys():
        raise Exception("Disk " + id + " does not exist")
    if(block_no <= 0):
        raise Exception("Invalid block number")
    disk  = disks[id]
    disk_size = disk[0]
    fragments = disk[1]
    if block_no > disk_size:
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
    text = read(blockn + 1)
    print(blockn)
    print(text)
    return text


class State:
    def __init__(self, fragments):
        self.diskData = []
        self.empty = []
        for interval in fragments:
            for j in range(interval[0],interval[1]+1):
                try:
                    data = read(j+1)
                except:
                    data = ""
                self.diskData.append(data)
                self.empty.append(empty[j])


def createCheckpoint(id):
    if(id not in disks.keys()):
        raise Exception("Disk id "+ str(id) + " doesn't exist")
    if(id not in stacks.keys()):
        stacks[id] = []
    fragments = disks[id][1]
    snapshot = State(fragments)
    stacks[id].append(snapshot)
    print("data" , stacks[id][-1].diskData)
    print("empty",stacks[id][-1].empty)
    return len(stacks[id])


def RollBack(id, checkpoint_no):
    if id not in disks.keys():
        raise Exception("Disk id " + str(id) + " doesn't exist")
    if id not in stacks.keys():
        raise Exception("No Checkpoint available for the disk " + str(id))
    if(checkpoint_no > len(stacks[id])):
        raise Exception("Disk checkpoint number doesn't exist")
    init_len = len(stacks[id])
    checkpoint_no = init_len - checkpoint_no + 1
    while(checkpoint_no != 0):
        state_obj = stacks[id].pop()
        checkpoint_no -= 1
    fragments = disks[id][1]
    i = 0
    for interval in fragments:
        for j in range(interval[0],interval[1]+1):
            empty[j] = state_obj.empty[i]
            if(j > 199):
                B[j - 200] = state_obj.diskData[i]
            else:
                A[j] = state_obj.diskData[i]
            i += 1

