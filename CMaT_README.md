# Code Changes #

The checkout of Distributed CellProfiler needs the following changes:

## Change Once ##

### for_cmat/CP_FLEET_us-east-2.json ###

This file defines the fleet.  This is should stay as is unless we change it CMaT wide.


## Change if pipeline changes, or CMaT's AWS configuration changes. ##

### Config.py Changes ###
APP_NAME
AWS_REGION (for CMaT, us-east-2)
AWS_BUCKET (for CMaT Thrust1, cmat-thrust1)
SSH_KEY_NAME (change to ssh-rsa-aws.pem).  this key needs to be uploaded in AWS.

The following should be tuned based on the job configuration.  If it's expected to have multithread call, then TASKS_PER_MACHINE should be set lower.
CLUSTER_MACHINES
TASKS_PER_MACHINE  (number of docker containers per machine)
DOCKER_CORES  (number of CellProfiler processes per docker.  Recommend 1.)

The following depends on the 
SECONDS_TO_START (delays before starting the next job.  should be the most memory intensive phase's time)

SQS_MESSAGE_VISIBILITY (how soon before a task is made available again.  this should be the average time of a run.  Too short, then the same job will spawn multiple times.)

SQS_DEAD_LETTER_QUEUE (leave as arn:aws:sqs:us-east-2:621508296309:DeadLetterQueue)

## Pipeline Changes ##

Need to change to using LoadData in order to read from the images.csv file.

Also need to add image groups in order to have Distributed CellProfiler partition the data and spawn tasks.


## Change for each dataset / run / update to pipeline ##

### for_cmat/microgliaJob.json ###

This is a description of the job, for the specific data.  For each new dataset/run/pipeline, a new file should be created.

### s3_helper/make_imagelistscsv.py ###

This reads a data directory on AWS s3, and creates a images.csv file for use with the Job.json file.  The output file will be local, and will need to be uploaded to AWS S3

