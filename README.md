# Load-Balancer

Simple job load balancer distribute fairly between master node and slave node. It has a GUI interface showing the statistics of each node and messages.

## Usage
Put ip address of master and slave node in `config.json` file

1. Launch master node with `python gui.py M`
2. Launch slave node with `python gui.py S`
3. Click start button in slave window
4. Click start button in master window


## Implementation

#### Step 1:​Bootstrap Phase
4. The transfer manager is responsible of performing a load transfer upon request of the
