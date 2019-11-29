import os
import re

class Config(object):
    # root_path = '/Users/linshan/Library/Group Containers/G69SCX94XU.duck/Library/Application Support/duck/Volumes/Server1LS2/home/lins/dsta/NTU_ReID_Outdoor'
    # root_path = '/Users/linshan/Pictures/WebAnnotationTesting/'
    root_path = '/home/tangyingtian/dsta/WebAnnotationTesting/'

    extracted_path = os.path.join(root_path,'ExtractedImages')

    annotated_path = os.path.join(root_path,'AnnotatedImages')

    ADMIN_ID = 0

    # annotated_path = '/home/tangyingtian/dsta/NTU_ReID_Outdoor/AnnotatedImages/'

    record_pattern = re.compile(r'^[\dA-Z]+_[A-Za-z\-]+_[A-Za-z]+$')
    dirname_pattern = re.compile(r'^[\d]{2}-[\d]{2}-[\dA-Z]+$')
    camera_pattern = re.compile(r'^[A-Z\d]+-[A-Z]+$')
