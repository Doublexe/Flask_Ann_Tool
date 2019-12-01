import os
import cv2
import base64
import numpy as np
import yaml
import multiprocessing as mp
from att.static.root_path import Config
import re
import shutil

root = Config.extracted_path

record_position = re.compile(r'[\dA-Z]+_[A-Za-z\-]+_[A-Za-z]+_[\d]+_[\d]+')


def store_meta(meta_pth):
    with open(meta_pth, 'r') as f:
        meta = yaml.load(f)
    record_pth = os.path.dirname(meta_pth)
    attribute = find_attribute(record_pth)
    relative_record_pth = os.path.relpath(record_pth, Config.extracted_path)
    annotated_record_pth = os.path.join(Config.annotated_path, relative_record_pth)
    if not os.path.isdir(annotated_record_pth):
        os.makedirs(annotated_record_pth)
    annotation = meta['annotated']
    for camera in os.listdir(annotated_record_pth):
        if camera not in annotation:
            shutil.rmtree(os.path.join(annotated_record_pth, camera))
    for camera in os.listdir(record_pth):
        camera_path = os.path.join(Config.annotated_path, relative_record_pth, camera)
        if not os.path.exists(camera_path):
            os.makedirs(camera_path)
    for camera, imgs in annotation.items():
        ori_imgs = set(os.listdir(camera_path))
        imgs = set([img.split('.')[0]+'_'+attribute+'.'+img.split('.')[1] for img in imgs])
        added = list(imgs - ori_imgs)
        removed = list(ori_imgs - imgs)
        for img in added:
            shutil.copyfile(
                os.path.join(record_pth, camera, img.replace('_'+attribute, '')),
                os.path.join(camera_path, img)
            )
        for img in removed:
            os.remove(os.path.join(camera_path, img))


def modify_record(cameras):
    output = {}
    for camera in cameras.keys():
        output[camera] = [img[:record_position.search(img).end()]+'.'+img.split('.')[-1] for img in cameras[camera]]
    return output

def find_attribute(record_pth):
    day = os.path.dirname(record_pth)
    record = os.path.basename(record_pth).split(r'_')
    num = record[0]
    name = '_'.join(record[1:])
    attribute = os.path.join(day, os.path.basename(day)+'.csv')
    with open(attribute, 'r') as f:
        for line in f.readlines():
            line=line.strip().split(',')
            if line[0]==num and line[1]==name:
                att = line[2]
                return att


def parse_dir_func(temp_ele):
    directory = temp_ele[0]
    camera = temp_ele[1]
    tracklet = temp_ele[2]
    img = sample_tracklet(os.path.join(directory, camera, tracklet))
    return (camera, (tracklet, img))

def parse_dir(directory):
    # a directory is a record

    attribute = find_attribute(directory)

    cameras = os.listdir(directory)        
    cameras = [f for f in cameras if os.path.isdir(os.path.join(directory,f))]
    print(cameras)
    
    ret = {}
    temp = []
    for camera in cameras:
        ret[camera] = []
        tracklets = os.listdir(os.path.join(directory,camera))
        for tracklet in tracklets:
            temp.append((directory, camera, tracklet))

    pool = mp.Pool(64)
    res = pool.map(parse_dir_func, temp)
    pool.close()
    pool.join()
    for camera in cameras:
        ret[camera] = [r[1] for r in res if r[0]==camera and r[1][1] is not None]

    # for camera in cameras:
    #     ret[camera] = []
    #     tracklets = os.listdir(os.path.join(directory,camera))
    #     for tracklet in tracklets:
    #         img = sample_tracklet(os.path.join(directory, camera, tracklet))
    #         if img is not None:
    #             ret[camera].append((tracklet, img))

    return ret, attribute

def clip_normalize(x, low, high):
    """ Clip lower and upper bounds for an array (color values), and then normalize to 0~1

    Parameters
    ----------
    x : ndarray, one-dimension
    low, high : float
        the bounds to clip
    """

    x[x>=high] = high
    x[x<=low] = low
    ma = x.max()
    mi = x.min()

    # If divid by 0, set to 0
    a = (x-mi)
    b = (ma-mi)
    if b == 0:
        x = np.zeros_like(a)
    else:
        x = np.divide(a, b)*255

    return x.astype(np.int32)


def simplestColorBalance(img, satLevel):
    """
    Parameter
    ---------
    img : ndarray, (H, W, C) #RGB
    satLevel : float, 0~1
        satLevel controls the percentage of pixels to clip to white and black (satLevel/2 for both white and black).
    """
    img = np.array(img)
    H, W, C = img.shape
    flat_img = img.reshape([H*W, C])

    lower_bound = satLevel/2
    upper_bound = 1-satLevel/2

    for ch in range(3):
        low = np.quantile(flat_img[:,ch], lower_bound)
        upp = np.quantile(flat_img[:,ch], upper_bound)
        flat_img[:,ch] = clip_normalize(flat_img[:,ch], low, upp)

    return flat_img.reshape([H, W, C])


def sample_tracklet(pth):
    sample = os.path.join(pth)
    img = cv2.imread(sample)
    if img is None:
        return None
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # modify the img
    img = simplestColorBalance(img, satLevel=0.25)

    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    success, a_numpy = cv2.imencode('.jpg', img)
    img = base64.b64encode(a_numpy.tostring()).decode('utf-8')

    return img
