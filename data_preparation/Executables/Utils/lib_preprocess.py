import os
import SimpleITK as sitk


k_means_filter = sitk.ScalarImageKmeansImageFilter()
label_merger = sitk.LabelVotingImageFilter()
mask_filter = sitk.MaskImageFilter()
fill_hole_filter = sitk.BinaryFillholeImageFilter()
smooth_filter = sitk.SmoothingRecursiveGaussianImageFilter()


class Preprocess:
    def __init__(self):
        self.fat_image = None
        self.water_image = None
        self.t2star_image = None

        self.t2star_name = None
        self.subj_dict = None
        self.out_path = None

    def preprocess_image_pipeline(self, subj_dict):
        self.subj_dict = subj_dict
        check_flag = self.read_images()
        if not check_flag:
            return False

        self.t2star_preprocess_and_write()

        return True

    def read_images(self):
        if (not os.path.isfile(self.subj_dict['fat'])) or (
                (not os.path.isfile(self.subj_dict['water'])) or (not os.path.isfile(self.subj_dict['t2star']))):
            return False

        self.t2star_name = os.path.basename(self.subj_dict['t2star'])
        name = self.t2star_name.split('.')[0]
        self.out_path = os.path.join(self.subj_dict["dir_path"], f'{name}_Noise_Removed.nii.gz')

        if os.path.isfile(self.out_path):
            return False

        self.fat_image = sitk.ReadImage(self.subj_dict['fat'])
        self.water_image = sitk.ReadImage(self.subj_dict['water'])
        self.t2star_image = sitk.ReadImage(self.subj_dict['t2star'])

        # Adding a check to equalize origins
        if self.fat_image.GetOrigin() != self.t2star_image.GetOrigin():
            self.fat_image.CopyInformation(self.t2star_image)
        if self.water_image.GetOrigin() != self.t2star_image.GetOrigin():
            self.water_image.CopyInformation(self.t2star_image)

        return True

    def t2star_preprocess_and_write(self):
        self.remove_t2star_bg()
        self.write_t2star()
        # self.smooth_t2star()
        # self.write_t2star(out_dir, 'No_Bg_Smoothed')

    def remove_t2star_bg(self):
        k_means_mask = self.get_wf_k_means_mask()
        self.t2star_image = mask_filter.Execute(self.t2star_image, k_means_mask)

    def write_t2star(self):
        sitk.WriteImage(self.t2star_image, self.out_path)

    def smooth_t2star(self):
        self.t2star_image = smooth_filter.Execute(self.t2star_image)

    def get_wf_k_means_mask(self):
        water_mask = k_means_filter.Execute(self.water_image)
        fat_mask = k_means_filter.Execute(self.fat_image)
        water_and_fat_mask = label_merger.Execute(water_mask, fat_mask)
        water_and_fat_mask = fill_hole_filter.Execute(water_and_fat_mask)
        return water_and_fat_mask

