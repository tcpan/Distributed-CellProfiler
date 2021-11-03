# import.
# %%
import boto3

import os
import glob

import pandas

import argparse

import re

# %%
# get commandline params
# - directory
# - extension
# - output file


parser = argparse.ArgumentParser(description='Make CellProfiler Image list')
parser.add_argument('-p', '--path', nargs="?", help='Directory, S3 URI or local path')
parser.add_argument('-x', '--ext', nargs="?", help='Image extension')
parser.add_argument('-o', '--output', nargs="?",
                    help='output filename (csv format)')

args = parser.parse_args()
img_path = args.path.rstrip('/')
img_ext = args.ext
imgs_csv = args.output

# %%
# check if s3.  if yes, split.
if (img_path.startswith("s3://")):
    p = img_path[len("s3://"):]
    bucket = p.split('/')[0]
    img_dir = p[(len(bucket) + 1):]
    plate = p.split('/')[-1]
    print("process S3 bucket " + bucket + ", folder " + img_dir + ", plate " + plate)
    s3 = boto3.resource('s3')
    my_bucket = s3.Bucket(bucket)

    files = []
    for object_summary in my_bucket.objects.filter(Prefix=img_dir):
        if object_summary.key.endswith("." + img_ext): 
            files.append( object_summary.key[(len(img_dir)+1):] ) 
    # may have non-matching ones.
else:
    plate = img_path.split('/')[-1]
    img_dir = img_path
    print("process local file system, folder " + img_path + ", plate " + plate)
    files = [ f[(len(img_path)+1):] for f in glob.glob(os.path.join(img_path, "*." + img_ext)) ]


# %%  

# compile regex.
# H4_-3_1_1_Stitched[Read 1_GFP 469,525]_001.tif
prog = re.compile("^(([A-Z])([0-9]{1,2}))_(-[0-9]+)_([0-9])_([0-9]+)_Stitched\[Read ([0-9])_(.*) ([0-9]{3}),([0-9]{3})\]_([0-9]{3})\." + img_ext + "$")
# keeping 2, 3, and 8
# 1 is combination of 2 and 3.

# %%
# first get unique count of images and total number of channels..
pos_list = []
chan_list = []
for f in files:
    result = prog.match(f)
    pos_list.append(result.group(1))
    chan_list.append(result.group(8).replace(" ", ""))
    
unique_pos = list(set(pos_list))
unique_pos.sort()
unique_chan = list(set(chan_list))
unique_chan.sort()

# create empty pandas dataframe of the right size.  (because we have multiple channels per position in separate files.)
col_names = ['Metadata_Plate', 'Metadata_WellRow', 'Metadata_WellColumn']
for chan in unique_chan:
    col_names.append('PathName_' + chan)
    col_names.append('FileName_' + chan)

print(col_names)

# %%
out = pandas.DataFrame(index=unique_pos, columns=col_names)
out['Metadata_Plate'] = plate

# now fill the table's path columns
abs_p = '/home/ubuntu/bucket/' + img_dir
for chan in unique_chan:
    out['PathName_' + chan] = abs_p

# %%
# then fill the rest of the table.
for f in files:
    result = prog.match(f)
    out.loc[result.group(1), 'FileName_' + result.group(8).replace(" ", "")] = f
    out.loc[result.group(1), 'Metadata_WellRow'] = result.group(2)
    out.loc[result.group(1), 'Metadata_WellColumn'] = result.group(3)
    

# %%
# output as file.

out.to_csv(imgs_csv, index=False)
