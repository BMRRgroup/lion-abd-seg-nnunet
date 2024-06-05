import os


def get_subdirs(main_dir):
    subdir_list = list()

    for root, subdir, files in os.walk(main_dir):
        # if 'Subject' in subdir:
        subdir_list.append(subdir)

    return subdir_list[0]


def get_subject_list(root_dir):
    out_list = list()
    parent_subj_list = get_subdirs(root_dir)
    for parent_subj in parent_subj_list:
        path_to_parent = os.path.join(root_dir, parent_subj)
        for fname in os.listdir(path_to_parent):
            if os.path.isdir(os.path.join(path_to_parent, fname)):
                out_list.append(f'{parent_subj}/{fname}')
            elif os.path.isfile(os.path.join(path_to_parent, fname)):
                out_list.append(parent_subj)
                break
            else:
                raise ValueError(f'Path: {os.path.join(path_to_parent, fname)} is not a file or folder')
    return out_list


def make_data_dict(in_dir, args):

    subj_list = get_subject_list(in_dir)
    out_dict = dict()

    for subj_path_name in subj_list:
        # Subject list can be like XXX_YYYY/XXX_YYYY_V1 or just XXX_YYYY_V1
        if '/' in subj_path_name:
            subj_name = subj_path_name.split('/')[1]
        else:
            subj_name = subj_path_name

        out_dict[subj_name] = dict()

        subj_dir = os.path.join(in_dir, subj_path_name)

        fat_filename = [f for f in os.listdir(subj_dir) if os.path.isfile(os.path.join(subj_dir, f)) and
                        (args.fat_keyword in f and 'nii.gz' in f)][0]
        print(f'\nFat: {fat_filename}')
        water_filename = [f for f in os.listdir(subj_dir) if os.path.isfile(os.path.join(subj_dir, f)) and
                          (args.water_keyword in f and 'nii.gz' in f)][0]
        print(f'Water: {water_filename}')
        t2star_filename = [f for f in os.listdir(subj_dir) if os.path.isfile(os.path.join(subj_dir, f)) and
                           (args.t2star_keyword in f and 'nii.gz' in f)][0]
        print(f'T2Star: {t2star_filename}')
        # Additional conditions for PDFF name checking
        # pdff_regex = re.compile('..._LION_......')
        pdff_filename = [f for f in os.listdir(subj_dir) if os.path.isfile(os.path.join(subj_dir, f)) and
                         ((args.pdff_keyword in f and 'nii.gz' in f) and (('11.nii.gz' in f or '213.nii.gz' in f) or
                                                      ('01_FF' in f or '15.nii.gz' in f)))][0]
        # print(f'PDFF: {pdff_filename}\n')

        fat_path = os.path.join(subj_dir, fat_filename)
        water_path = os.path.join(subj_dir, water_filename)
        t2star_path = os.path.join(subj_dir, t2star_filename)
        pdff_path = os.path.join(subj_dir, pdff_filename)

        out_dict[subj_name]['fat'] = fat_path
        out_dict[subj_name]['water'] = water_path
        out_dict[subj_name]['t2star'] = t2star_path
        out_dict[subj_name]['pdff'] = pdff_path
        out_dict[subj_name]['dir_path'] = subj_dir

    return out_dict


