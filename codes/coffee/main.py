"""
@author: Guilherme Esgario
@email: guilherme.esgario@gmail.com
"""

import os
from .classifier import Classifier

import warnings
warnings.filterwarnings("ignore")

def run(in_image_path, out_image_path):
    PATH = os.path.dirname(__file__)
    
    # Parameters
    class Opt():
        pass
    
    options = Opt()
    options.in_image_path = in_image_path
    options.out_image_path = out_image_path
    options.segmentation_weights = os.path.join(PATH, 'net_weights/segmentation.pth')
    options.symptom_weights = os.path.join(PATH, 'net_weights/symptom.pth')
    
    # Classifier
    clf = Classifier(options)
    result = clf.run()
    
    return result