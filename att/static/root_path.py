import os
import re
import numpy as np

class Config(object):
    # root_path = '/Users/linshan/Library/Group Containers/G69SCX94XU.duck/Library/Application Support/duck/Volumes/Server1LS2/home/lins/dsta/NTU_ReID_Outdoor'
    # root_path = '/Users/linshan/Pictures/WebAnnotationTesting/'
    root_path = '/home/tangyingtian/dsta/NTU_ReID_Outdoor/'

    ori_extracted_path = os.path.join(root_path,'ExtractedImages')
    ori_annotated_path = os.path.join(root_path,'AnnotatedImages')

    extracted_path = os.path.abspath('ConstrainedExtractedImages')
    annotated_path = os.path.abspath('AnnotatedImages')

    ADMIN_ID = 0

    record_pattern = re.compile(r'^[\dA-Z]+_[A-Za-z\-]+_[A-Za-z]+$')
    dirname_pattern = re.compile(r'^[\d]{2}-[\d]{2}-[\dA-Z]+$')
    camera_pattern = re.compile(r'^[A-Z\d]+-[A-Z]+$')

    annotate_targets = np.genfromtxt('att/static/outdoor_annotations.csv', delimiter=',',dtype=str)[:, -3].tolist()

    REL_TARGETS = list(map(lambda pth: os.path.relpath(pth, r'/home/rahulahuja/dsta/NTU_ReID_Outdoor/AnnotatedImages/'), annotate_targets))
