import os
import starfile
import pandas as pd
import numpy as np


def get_txt_files_list(path):
    files = os.listdir(path)
    txt_files = [file for file in files if file.endswith('.txt')]
    return txt_files

def read_txt_to_df(path):
    dfs_dict = {}
    txt_files = get_txt_files_list(path)
    for file in txt_files:
        file_path = os.path.join(path, file)
        file_path_new = os.path.join(path, file+'_processed')
        print(f'''Please ignore the {file}.txt_processed files and you can just delete them after generating the star file''')
        with open(file_path, 'r') as f:
            lines = f.readlines()
            new_lines = ['\t'.join(line.strip().split()) for line in lines]
        with open(file_path_new, 'w') as f:
            f.writelines('\n'.join(new_lines))
        temp_df = pd.read_csv(file_path_new, sep='\t', header=None, names=['X', 'Y', 'Z'])
        dfs_dict[file] = temp_df
    return dfs_dict

def cal_posi(df, binning):
    cal_posi_df = pd.concat([pd.DataFrame({'rlnCoordinateX': [(df['X'].iloc[i] + df['X'].iloc[i+1]) / 2 * binning],
                                   'rlnCoordinateY': [(df['Y'].iloc[i] + df['Y'].iloc[i+1]) / 2 * binning],
                                   'rlnCoordinateZ': [(df['Z'].iloc[i] + df['Z'].iloc[i+1]) / 2 * binning]}) 
                    for i in range(0, df.shape[0], 2)], ignore_index=True)
    return cal_posi_df

def eulerangle(x1,x2,y1,y2,z1,z2):
    x = x2 - x1
    y = y2 - y1
    z = z2 - z1
    if x == 0:
        phi = np.pi / 2
    else:
        phi = np.arctan2(y, x)
    if z == 0:
        theta = np.pi / 2
    else:
        theta = np.arctan2(np.sqrt(x ** 2 + y ** 2), z)
    psi = 0
    phi = np.rad2deg(phi)
    theta = np.rad2deg(theta)
    psi = np.rad2deg(psi)
    return phi, theta, psi

def cal_eulerange(df):
    cal_eulerange_df = pd.DataFrame(columns=['rlnAngleRot', 'rlnAngleTilt', 'rlnAnglePsi'])
    for i in range(0, df.shape[0], 2):
        phi, theta, psi = eulerangle(x1=df['X'].iloc[i], x2=df['X'].iloc[i+1], y1=df['Y'].iloc[i], y2=df['Y'].iloc[i+1], z1=df['Z'].iloc[i], z2=df['Z'].iloc[i+1])
        angle_temp = pd.DataFrame({'rlnAngleRot': [phi],
                                   'rlnAngleTilt': [theta],
                                   'rlnAnglePsi': [psi]})
        cal_eulerange_df = pd.concat([cal_eulerange_df, angle_temp], ignore_index=True)
    return cal_eulerange_df

def save_dynamo_star(dataframe, filename, filepath):
    filename_n = filename if filename else 'AllCoords.star'
    filepath_n = str(filepath) + '/' if filepath else str(os.path.abspath('.')) + '/'
    filenamepath = os.path.join(filepath_n, filename_n)
    starfile.write(dataframe, filenamepath, overwrite=True)
    print(f'Saved relion .star file {filename_n} to {filepath_n}.')
