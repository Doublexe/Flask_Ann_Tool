import os
class Config(object):
    root_path = '/Users/linshan/Library/Group Containers/G69SCX94XU.duck/Library/Application Support/duck/Volumes/Server1LS2/home/lins/dsta/NTU_ReID_Outdoor'
    
    extracted_path = os.path.join(root_path,'ExtractedImages')
    
    annotated_path = os.path.join(root_path,'AnnotatedImages')
    