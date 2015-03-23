#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Will Brennan'

# built-in modules
import logging
# Standard modules
import cv2
import numpy
# Custom modules
import scripts

logger = logging.getLogger('main')


def evaluate(img_col, args):
    assert isinstance(img_col, numpy.ndarray), ''
    assert img_col.ndim in [2, 3], ''
    img_gry = cv2.cvtColor(img_col, cv2.COLOR_RGB2GRAY)
    rows, cols = img_gry.shape
    crow, ccol = rows/2, cols/2
    f = numpy.fft.fft2(img_gry)
    fshift = numpy.fft.fftshift(f)
    fshift[crow-30:crow+30, ccol-30:ccol+30] = 0
    f_ishift = numpy.fft.ifftshift(fshift)
    img_fft = numpy.fft.ifft2(f_ishift)
    img_fft = numpy.abs(img_fft)
    if args.display and not args.testing:
        cv2.destroyAllWindows()
        cv2.imshow('img_fft', img_fft)
        cv2.imshow('img_col', img_col)
        cv2.waitKey(0)
    result = (640.0*480.0/img_fft.size)*numpy.mean(img_fft)
    return result, result < args.thresh


if __name__ == '__main__':
    args = scripts.get_args()
    logger = scripts.get_logger(quite=args.quite, debug=args.debug)
    x_points, y_points = [], []
    for path in args.image_paths:
        for img_path in scripts.find_images(path):
            logger.debug('evaluating {0}'.format(img_path))
            img = cv2.imread(img_path)
            if isinstance(img, numpy.ndarray):
                if args.testing:
                    x_axis = [1, 3, 5, 7, 9]
                    for x in x_axis:
                        img_mod = cv2.GaussianBlur(img, (x, x), 0)
                        x_points.append(x)
                        y_points.append(evaluate(img_mod, args=args)[0])
                else:
                    result, val = evaluate(img, args=args)
                    logger.info('fft average of {0}'.format(result))
    if args.display:
        import matplotlib.pyplot as plt
        plt.scatter(x_points, y_points)
        plt.grid(True)
        plt.show()
