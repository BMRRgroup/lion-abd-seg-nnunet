from Utils.lib_preprocess import Preprocess
from Utils.lib_utils import make_data_dict
import argparse
import os
import time
from tqdm import tqdm


def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)


parser = argparse.ArgumentParser()
required_named = parser.add_argument_group('required named arguments')
required_named.add_argument('-i', '--in_dir', type=dir_path,
                            default='', help='Path to Dataset', required=True)
# required_named.add_argument('-o', '--out_dir', type=dir_path,
#                             default='', help='Path to Output Directory', required=True)
# parser.add_argument('--is_pre_interpol', action="store_true",
#                     help='Whether input is already pre-interpolated to (256, 224, 72)')

parser.add_argument('--fat_keyword', type=str, default='Fat_fused', help='Keyword in image name for Fat')
parser.add_argument('--water_keyword', type=str, default='Water_fused', help='Keyword in image name for Water')
parser.add_argument('--t2star_keyword', type=str, default='T2star_fused', help='Keyword in image name for Water')
parser.add_argument('--pdff_keyword', type=str, default='FF_fused', help='Keyword in image name for Water')
# ---------------------------------------------------
args = parser.parse_args()
in_dir = args.in_dir
# out_dir = args.out_dir

# ----------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    start_time = time.time()

    subject_dict = make_data_dict(in_dir, args)

    t2star_pp = Preprocess()

    loop = tqdm(subject_dict.keys())

    for subj_name in loop:
        loop.set_description(subj_name)

        check_flag = t2star_pp.preprocess_image_pipeline(subject_dict[subj_name])

        if not check_flag:
            print(f'\nSkipped {subj_name}: Noise_Removed T2* Already Exists or One or more of Fat, Water, or T2Star missing')


