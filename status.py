import argparse
import fileinput
import fnmatch
import os
import os.path


_files = []


def glob_filter(path, pattern):
    return fnmatch.fnmatch(path, pattern)


def walk(path, callback, glob):
    for root, dirs, files in os.walk(path):
        for file in files:
            if not glob_filter(file, glob):
                continue
            callback(root, file, path)


def _status(root, file, relpath):
    absfile = os.path.join(root, file)
    _files.append((os.path.relpath(os.path.join(root, file), relpath), line_num(absfile)))


def line_num(file):
    num = 0
    with fileinput.input(files=(file,), mode='rb') as f:
        for line in f:
            num += 1
    return num


def status(path, glob):
    walk(path, _status, glob)


def output(sort:str, limit:int) -> str:

    files = _files
    # prepare files by sort and limit options.
    reverse = True
    if sort is not None:
        if sort == 'decrease':
            pass
        elif sort == 'increase':
            reverse = False
        else:
            raise ValueError('value of sort can only be decrease or increase')
        files = sorted(_files, key=lambda v: v[1], reverse=reverse)

    if sort is None and limit is not None:
        files = sorted(_files, key=lambda v: v[1], reverse=reverse)


    # buf is the output buffer, max_width is the max width of output and total_lines
    # represents the total lines number of files in output.
    buf = ''
    max_width = 0
    total_lines = 0

    # dump status result in buf.
    for index, v in enumerate(files):
        if limit is not None and index >= limit:
            break
        total_lines += v[1]
        current = '%5d %s\n' % (v[1], v[0])
        if len(current) > max_width:
            max_width = len(current)
        buf += current

    # a simple summary of the status result.
    summary = 'total files: {}\ntotal lines: {}'.format(len(files), total_lines)

    return render(buf.rstrip('\n'), max_width, summary)


def render(output, max_width, summary):
    return '{}\n{}\n{}\n{}\n{}'.format(
        '=' * max_width,
        output,
        '-' * max_width,
        summary,
        '=' * max_width
    )


def dump(output, file):
    with open(file, 'w') as f:
        f.write(output)


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--path", help="path to detect, can be name of file or directory, default to current directory")
    parser.add_argument("--limit", type=int, help="limit the lines of output, this would implicily sort the output files by line number in decrease order")
    parser.add_argument("--sort", choices=['increase', 'decrease'], help="sort files by line number of it")
    parser.add_argument("--output", type=str, help="redirect output to file")
    parser.add_argument("--glob", type=str, default='*', help="glob filter apply to files")
    
    args = parser.parse_args()
    if args.path is None:
        args.path = os.getcwd()
    else:
        args.path = os.path.abspath(args.path)
    status(args.path, args.glob)
    stat = output(args.sort, args.limit)
    if args.output is not None:
        dump(stat, args.output)
    else:
        print(stat)
    
