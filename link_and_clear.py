from att.static.root_path import Config
import os
import shutil

# This will clear the temp storage (all meta.yaml) and create symlink to the folders that we want to reannotate

if os.path.exists(Config.extracted_path) and os.access(Config.extracted_path, os.W_OK):
    shutil.rmtree(Config.extracted_path)

for rel_pth in Config.REL_TARGETS:
    camera_pths = [[os.path.join(os.path.dirname(os.path.join(Config.extracted_path, rel_pth)),d), os.path.relpath(os.path.join(os.path.dirname(os.path.join(Config.extracted_path, rel_pth)),d), Config.extracted_path)] for d in os.listdir(os.path.dirname(os.path.join(Config.ori_extracted_path, rel_pth)))]
    for target_pth, rrel_pth in camera_pths:
        target_dir_pth = os.path.dirname(os.path.dirname(target_pth))
        if not os.path.exists(target_dir_pth):
            os.makedirs(target_dir_pth)
            csv = os.path.basename(target_dir_pth)+'.csv'
            source_dir_pth = os.path.dirname(os.path.dirname(os.path.join(Config.ori_extracted_path, rrel_pth)))
            source_csv_pth = os.path.join(source_dir_pth, csv)
            if not os.path.exists(source_csv_pth):
                raise OSError(f"{source_csv_pth} not exists.")
            os.symlink(source_csv_pth, os.path.join(target_dir_pth, csv))
        if not os.path.exists(target_pth):
            source_pth = os.path.join(Config.ori_extracted_path, rrel_pth)
            if not os.path.exists(source_pth):
                source_pth = os.path.join(Config.ori_extracted_path, rrel_pth+' ')
                if not os.path.exists(source_pth):
                    raise OSError(f"{source_pth} not exists.")
            os.makedirs(os.path.dirname(target_pth), exist_ok=True)
            os.symlink(source_pth, target_pth)
