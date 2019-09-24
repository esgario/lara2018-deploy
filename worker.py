"""
@author: Guilherme Esgario
@email: guilherme.esgario@gmail.com
    
If you'd like add another script you can call your code at
image_classification method changing the 'algorithm' name.
"""

import sys
sys.stdout.flush()

import asyncio
from mlq.queue import MLQ

# Import Inference Scripts HERE
from codes.coffee import main as clf_coffee


mlq = MLQ('prediction_app', 'redis', 6379, 0)

def image_classification(p_dict, *args):
    print('Start inference:', p_dict)
    
    if p_dict['algorithm'] == 'coffee':
        # exec coffee algorithm
        p_dict['out_file'] = p_dict['file'].split('.')[0]+'_output.png'
        p_dict['result'] = clf_coffee.run('in_images/'+p_dict['file'],
                                          'out_images/'+p_dict['out_file'])
    
    if p_dict['algorithm'] == 'cancer':
        # exec cancer algorithm
        pass
    
    print('Inference completed')
    
    return p_dict

def main():
    async def start_worker():
        mlq.create_listener(image_classification)
        
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_worker())
    
    print("Worker started")

main()
