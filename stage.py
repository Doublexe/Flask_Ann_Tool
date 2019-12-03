from att.static.root_path import Config
import yaml
from tqdm import tqdm
import os
import datetime

def parse_annotated(annotated_path):
    annotated = {}
    dirs = [d for d in os.listdir(annotated_path) if Config.dirname_pattern.search(d) is not None]
    for dr in tqdm(dirs, desc="Parsing directories"):
        records = [r for r in os.listdir(os.path.join(annotated_path, dr)) if Config.record_pattern.search(r) is not None]
        for record in records:
            cameras = [c for c in os.listdir(os.path.join(annotated_path, dr, record)) if Config.camera_pattern.search(c) is not None]
            for camera in cameras:
                imgs = os.listdir(os.path.join(annotated_path, dr, record, camera))
                annotated.setdefault(dr, {}).setdefault(record, {})[camera]=imgs

    return annotated


if __name__ == '__main__':
    annotated=parse_annotated(Config.annotated_path)
    with open('./original'+str(datetime.datetime.now().date())+'.yaml', 'w') as f:
        yaml.dump(annotated, f)  # this is a backup
    with open('./original.yaml', 'w') as f:
        yaml.dump(annotated, f)
