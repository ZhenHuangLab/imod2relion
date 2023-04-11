from imod2relion._utils import *
import argparse

def main():
    parser = argparse.ArgumentParser(
        prog='imod2relion', 
        description='''A tool reading IMOD points, obtaining particles' info and generating .star file for RELION''',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
        More details in README.md.
        https://github.com/ZhenHuangLab/imod2relion
        Feel free to contact me if you have any other questions.
        --------------------------
        Copyright: Zhen Huang. 
        Email: hzvictor@zju.edu.cn
        --------------------------
        '''
        )

    parser.add_argument('--input', 
                        '-i', 
                        type=str, 
                        required=True,
                        help='Dictionary containing all txt files. The txt filenames must match the tomogram names.'
                        )
    parser.add_argument('--binning', 
                        '-b', 
                        type=int, 
                        default=1,
                        help='Binning of the tomogram when using IMOD to pick particles. Default is 1.')
    parser.add_argument('--output', 
                        '-o', 
                        type=str, 
                        default='IMODpoints.star',
                        help='''Name of relion star file. 
                        Do not forget the file suffix .star. 
                        Default is IMODpoints.star''')
    args = parser.parse_args()

    path = args.input
    binning = args.binning
    starfilename = args.output

    txt_files_list = get_txt_files_list(path)
    print(f'Reading txt files from {txt_files_list}')
    dfs_dict = read_txt_to_df(path)
    star_data = pd.DataFrame()
    star_data_temp = {}
    for txt_name in txt_files_list:
        df = dfs_dict[txt_name]
        print(f'Reading {txt_name}')
        tomoname = txt_name.split('.')[0]
        print(f'Recognize tomogram {tomoname}')
        # print(df)
        # print(df.shape[0])
        star_data_temp['rlnTomoName'] = [f'{tomoname}'] * (df.shape[0] // 2)
        star_data_temp['rlnTomoParticleId'] = [' '] * (df.shape[0] // 2)
        star_data_temp['rlnTomoManifoldIndex'] = ['1'] * (df.shape[0] // 2)
        posi_df = cal_posi(df, binning)
        for axis in ('X', 'Y', 'Z'):
            star_data_temp[f'rlnCoordinate{axis}'] = posi_df[f'rlnCoordinate{axis}']
        for axis in ('X', 'Y', 'Z'):
            star_data_temp[f'rlnOrigin{axis}Angst'] = ['0'] * (df.shape[0] // 2)
        angle_df = cal_eulerange(df)
        for angle in ('Rot', 'Tilt', 'Psi'):
            star_data_temp[f'rlnAngle{angle}'] = angle_df[f'rlnAngle{angle}']
        star_data_temp['rlnClassNumber'] = ['1'] * (df.shape[0] // 2)
        star_data_temp['rlnRandomSubset'] = np.random.choice([1, 2], size=len(star_data_temp['rlnClassNumber']), p=[0.5, 0.5])
        # print(pd.DataFrame(star_data_temp))
        star_data = pd.concat([star_data, pd.DataFrame(star_data_temp)], ignore_index=True)
        star_data['rlnTomoParticleId'] = range(1, star_data.shape[0]+1)
    print(star_data)

    save_dynamo_star(star_data, starfilename, filepath=path)