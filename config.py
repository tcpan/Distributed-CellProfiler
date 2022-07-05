# Constants (User configurable)

APP_NAME = 'Marklein_Microglia'                # Used to generate derivative names unique to the application.

# DOCKER REGISTRY INFORMATION:
DOCKERHUB_TAG = 'cellprofiler/distributed-cellprofiler:2.0.0_4.1.3'

# AWS GENERAL SETTINGS:
AWS_REGION = 'us-east-2'
AWS_PROFILE = 'default'                 # The same profile used by your AWS CLI installation
SSH_KEY_NAME = 'ssh-rsa-aws.pem'      # Expected to be in ~/.ssh
AWS_BUCKET = 'cmat-thrust1'

# EC2 AND ECS INFORMATION:
ECS_CLUSTER = 'default'
CLUSTER_MACHINES = 4
#TASKS_PER_MACHINE = 8
#MACHINE_TYPE = ['m4.xlarge']    # this has 4GB per core, 4 cores.
#MACHINE_TYPE = ['c6i.2xlarge']  # this has 2GB per core, 8 cores.
MACHINE_TYPE = ['r6i.xlarge']     # this has 8GB per core, 4 cores.
machine_cores = 4       # cores - please look up on AWS website based on machine type
machine_mem = 32        # in GB - please look up on AWS website based on machine type
docker_max_mem = 14     # container MAX mem in GB. default microglia pipeline uses about 12GB.  this is the limiting factor.
counts_by_mem = machine_mem // docker_max_mem
# prefer 1 core per container.
TASKS_PER_MACHINE = min(machine_cores, counts_by_mem)

MACHINE_PRICE = 0.10
EBS_VOL_SIZE = 30                       # In GB.  Minimum allowed is 22.
DOWNLOAD_FILES = 'False'

# DOCKER INSTANCE RUNNING ENVIRONMENT:
#DOCKER_CORES = 1                        # Number of CellProfiler processes to run inside a docker container
DOCKER_CORES = machine_cores // TASKS_PER_MACHINE    # Number of CellProfiler processes to run inside a docker container
CPU_SHARES = DOCKER_CORES * 1024        # ECS computing units assigned to each docker container (1024 units = 1 core)
#MEMORY = 15000                           # Memory assigned to the docker container in MB
MEMORY = docker_max_mem * 1000
SECONDS_TO_START = 30                 # Wait before the next CP process is initiated to avoid memory collisions

# SQS QUEUE INFORMATION:
SQS_QUEUE_NAME = APP_NAME + 'Queue'
SQS_MESSAGE_VISIBILITY = 20*60           # Timeout (secs) for messages in flight (average time to be processed)
SQS_DEAD_LETTER_QUEUE = 'arn:aws:sqs:us-east-2:621508296309:DeadLetterQueue'

# LOG GROUP INFORMATION:
LOG_GROUP_NAME = APP_NAME 

# REDUNDANCY CHECKS
CHECK_IF_DONE_BOOL = 'True'  #True or False- should it check if there are a certain number of non-empty files and delete the job if yes?
EXPECTED_NUMBER_FILES = 5    #What is the number of files that trigger skipping a job?
MIN_FILE_SIZE_BYTES = 1      #What is the minimal number of bytes an object should be to "count"?
NECESSARY_STRING = 'csv'        #Is there any string that should be in the file name to "count"?

# PLUGINS
USE_PLUGINS = 'False'
