# DiskVirtualization

Considered 2 arrays A and B as 2 disks of size 200 and 300 blocks each. But the user gets a view of single disk of size 500 blocks. <br />

Designed the followind APIs:
1. CreateDisk(Id, num_blocks)
> to create a smaller disk of size *num_blocks* with a unique *Id* within a larger available disk of 500 blocks.
2. DeleteDisk(Id)
> to delete a disk of given id. This would create a hole in larger disk, leading to fragmentation. **Fragmentation** has been handled using merging and splitting of blocks.
3. readFromDisk(Id, block_no)
> read from a disk *Id* and its block *block_no.*
4. writeToDisk(Id, block_no, block_info)
> write to disk *Id* on block *block_no* and content is *block_info.*
5. createCheckpoint(Id)
> to save the current state of disk *Id* and return a state number. The disk *Id* can be later rolled back to this state using the returned state number.
6. RollBack(Id, state)
> to roll back *Id* to *state.*

Added replication feature to provide reliability. New APIs introduced:

1. write_with_replicate(Id, block_no, block_info)
2. read_with_replicate(Id, block_no)
