# DiskVirtualization

Considered 2 arrays A and B as 2 disks of size 200 and 300 blocks each. But the user gets a view of single disk of size 500 blocks. <br />

Designed the followind APIs:
1. CreateDisk(Id, num_blocks)
* To create a smaller disk with a unique id within a larger available disk of 500 blocks.
2. DeleteDisk(Id)
3. readFromDisk(Id, block_no)
4. writeToDisk(Id, block_no, block_info)
5. createCheckpoint(Id)
6. RollBack(Id, state)

Added replication feature to provide reliability. New APIs introduced:

1. write_with_replicate(Id, block_no, block_info)
2. read_with_replicate(Id, block_no)
