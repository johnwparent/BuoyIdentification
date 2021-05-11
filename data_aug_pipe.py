import sys, os, distutils
import argparse
import cv2
import glob
import random

def perform_transform(ims, transform):
    ret_ims = ims
    for im in ims:
        t_im = im.copy()
        new_ims = transform(im)
        if type(new_ims) == list:
            ret_ims.extend(new_ims)
        else:
            ret_ims.append(new_ims)
    return ret_ims

def mult(im, val = 0):
    ims = []
    for x in range(50):
        ims.append(im.copy())
    return ims

# Code inspired by openCV rotate documentation
def rotate(im, val):
    rotate_range = [-50,45]
    val = random.randrange(rotate_range[0],rotate_range[1])
    (h, w) = im.shape[:2]
    (centerX, centerY) = (w // 2, h // 2)
    RotMat = cv2.getRotationMatrix2D((centerX, centerY), val, 1.0)
    rotated = cv2.warpAffine(im, RotMat, (w, h))
    return rotated

def bright(im):
    bright_range = ["-50","100"]
    val = random.randrange(bright_range[0],bright_range[1])
    sat_im = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    cv2.add(sat_im[:,:,2], val, sat_im[:,:,2])
    return cv2.cvtColor(sat_im, cv2.COLOR_HSV2BGR)

def crop(im):
    width_height_range = [90,70]
    rand_range_x = random.randrange(width_height_range[0],width_height_range[1])
    rand_range_y = random.randrange(width_height_range[0],width_height_range[1])
    return im[0:rand_range_x,0:rand_range_y]

def flip(im):
    flip_direction = "vertical"
    return cv2.flip(im, 0)

im_types = [".jpg", ".png"]

def read_ims_in(direc, recursive=False):
    jpg_files = glob.glob(direc+"*"+im_types[0])
    png_files = glob.glob(direc+"*"+im_types[1])
    ims = []
    for pth in jpg_files:
        ims.append(cv2.imread(pth))
    for pth in png_files:
        ims.append(cv2.imread(pth))
    return ims

def write_ims_out(direc, ims):
    for im in ims:
        pth, ext = os.path.splitext(direc)
        cv2.imwrite(pth+hash(im)+ext,im)

def main():
    args = argparse.ArgumentParser()
    args.add(
        "--include-dir",
        "-I",
        dest="I",
        action="store",
        default=os.getcwd(),
        required=False,
    )
    args.add_argument(
        "--aug",
        "-a",
        dest="aug_type",
        action="append",
        default=["mult"],
        type=list,
        required=False,
        choices=["mult","bright","crop","rotate","flip"]
    )
    args.add_argument(
        "--output-dir",
        "-o",
        dest="output_dir",
        action="store",
        required=False,
        default=os.getcwd(),
    )
    args.add_argument(
        "--recursive",
        "-R",
        dest="recursive",
        action="store",
        required=False,
        default=False,
        type=lambda x: bool(distutils.util.strtobool(x))
    )
    opts = args.parse_args(sys.argv[1:])
    initial_ims = read_ims_in(opts.I, recursive=opts.recursive)
    tot_ims = [].extend(initial_ims)
    for mut in sorted(opts.arg_type):
        tot_ims.extend(perform_transform(initial_ims,mut))

if __name__ == '__main__':
    main()