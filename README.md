# Load-Balancer

Simple job load balancer distribute fairly between master node and slave node. It has a GUI interface showing the statistics of each node and messages.

## Usage
Put ip address of master and slave node in `config.json` file

1. Launch master node with `python gui.py M`
2. Launch slave node with `python gui.py S`
3. Click start button in slave window
4. Click start button in master window


## Implementation

#### Step 1:​Bootstrap Phaseg09 (1​72.22.156.12)​node is chosen as master node, and g09­s (1​72.22.156.72)​as slave node. In bootstrap phase, the local node will transfer half of the workload to the remote node.#### Step 2:​Processing Phase1. After initialization step is finished, several threads are initialized: worker_thread, hardware_monitor, state_manager, transfer_manager, adaptor.2. The worker thread executes the computation job (increment each element of vector) on aseparate thread. Worker thread keeps working until both nodes finish all the jobs in theirqueues. While processing each job, the worker thread will limit its utilization to the throttling value setby user. e.g. a throttling value of 0.7 means that during each 100ms, the worker thread mustbe sleeping for 30ms and process the job for 70ms.time.sleep((​100​​-​​self​.throttling) ​/​​1000.0​)3. The hardware monitor is responsible for collecting information about the hardware. It monitorsCPU utilization information (p​sutil.cpu_percent())​and user throttling value. 
4. The transfer manager is responsible of performing a load transfer upon request of theadaptor. We implement two thread function, one is to move jobs from the job queue and sendthem to another node: s​end_job​(​self​,​job​);​one is to receive any jobs from another node andplace them in the job queue: r​eceive_job​(​self​).Here we use UDP to transfer jobs.5. The state manager is responsible of sending and receiving state from another node. Similar to transfer manager, we implement two thread function, one is to send local state information to remote node: s​end_state​(​self​),​one is to receive remote state information: r​eceive_state​(​self​).​ We update the state information every 30s.6. The adaptor is responsible for applying the transfer and selection policies. Transfer policy is set as a comparison between the local and remote nodes. When the size of the remaining job queue for each node differs in size by more than a threshold value, say 30 jobs, that differential will be transferred to the node with fewer jobs. We use a sender initiated transfer, which has less overhead but is less responsive than a receiver or symmetrically initiated transfer.#### Step 3:​Aggregation PhaseAfter all jobs are successfully processed, our system aggregate the result into remote node and display the result. We accomplish this by sending finished jobs from the remote node to the local node and requeueing completed jobs in the master node. In this way, all completed jobs will be stored in the original master node job queue. 

