import os
import datetime
store_dir="BIN/"

#Move current BIN files to BIN_OUT
if len([file for file in os.listdir(store_dir)])!=0:
    folder_name=f"../../BIN_OUT/{int(datetime.datetime.now().timestamp())}/"
    os.makedirs(folder_name)
    for file in os.listdir(store_dir):
        os.rename(store_dir+file,folder_name+file)