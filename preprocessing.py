#!/usr/bin/env python

import json
import os
import argparse
import pandas as pd

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--context-length', type=int, default=200)
    parser.add_argument('--instances', type=str, default='i-00fd004630d4fc21a,i-053f0b868dc1f9da6,i-057f758d045603466,i-070b0ff606e234f7d,i-078542929a025d728,i-086cec6ebf9adb1da,i-09943d7fdc4ebc96c,i-0b1daabbde6ba0865,i-0e02c4d67b1f6f3b9,i-0fd3557bd75c356fe')
    args, _ = parser.parse_known_args()

    context_length = args.context_length
    instances = args.instances

    print('Received arguments {}'.format(args))

    # input data
    input_data_path = '/opt/ml/processing/input/'
    # input_data_path = 'local_test/test_dir/processing/input/'
    print('Reading input data from {}'.format(input_data_path))
    print('now_files: ' + str(os.listdir(input_data_path)))

    data = {}
    with open(input_data_path + 'memory.dat') as lines:
        for line in lines:
            result = json.loads(line)['data']['result']
            for item in result:
                instance = item['metric']['ec2_instance_id']
                one = pd.DataFrame(item['values'])
                if instance not in data:
                    data[instance] = one
                else:
                    data[instance] = pd.concat(
                        [data[instance], one], ignore_index=True)

    # processing
    print('Processing data...')
    result = pd.DataFrame()
    for instance in instances.split(','):
        if instance in data:
            one = data[instance]
            one.columns = ['ds', instance]
            if 'ds' not in result:
                result = one
            else:
                result[instance] = one[instance]

    print(result.head())
    result = result.apply(pd.to_numeric, errors="raise")
    result['y'] = result.iloc[:, 1:].mean(axis=1)
    result = result[['ds', 'y']]

    # output data
    print('Output data...')
    output_data_path = '/opt/ml/processing/output/'
    # output_data_path = 'local_test/test_dir/processing/output/'
    train_data_path = output_data_path + 'train'
    if not os.path.exists(train_data_path):
        os.makedirs(train_data_path)
    result.to_csv(train_data_path + '/memory.csv',
                  header=True, index=False)
