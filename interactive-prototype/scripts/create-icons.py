import numpy as np
import cv2

import os
import sys
import argparse


def get_parser():
    parser = argparse.ArgumentParser(description="create ubuntu icons")
    parser.add_argument("--input_image", dest="input_image", help="original image used for icon production")
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    input_image = str(args.input_image)
    
    if "" == input_image or not os.path.exists(input_image):
        parser.print_help()
        return -1

    image = cv2.imread(input_image)
    rootdir = "hicolor"
    if not os.path.exists(rootdir):
        os.makedirs(rootdir)

    for imgsize in (16, 22, 24, 32, 48, 64, 128, 256):
        destdir = os.path.join(rootdir, "{0}x{0}/apps".format(imgsize))
        if not os.path.exists(destdir):
            os.makedirs(destdir)
        imagename = input_image.strip().split(".")[0]
        icon = cv2.resize(image, (imgsize,imgsize), 0, 0, cv2.INTER_LINEAR)
        cv2.imwrite(os.path.join(destdir, imagename+".png"), icon)

    return 0


if __name__ == "__main__":
    sys.exit(main())

