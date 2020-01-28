import argparse
import logging
import os
import os.path
import subprocess


pull_cmd = ['git', 'pull']


def pull(path):
    logging.info('pulling {}'.format(path))
    original_path = os.getcwd()
    os.chdir(path)
    try:
        subprocess.run(args=pull_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        logging.info('pull {} completely'.format(path))
    except subprocess.CalledProcessError as e:
        logging.error('error in pulling {}'.format(path))
    finally:
        os.chdir(original_path)


def pull_repos(path):
    path = os.path.abspath(path)
    for p in os.listdir(path):
        if os.path.isdir(p):
            pull(os.path.join(path, p))


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--path", help="path, default to current directory")

    args = parser.parse_args()
    if args.path is None:
        args.path = os.getcwd()
    pull_repos(args.path)
