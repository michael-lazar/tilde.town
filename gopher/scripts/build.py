#!/usr/bin/env python3
"""
Build script for gopher://tilde.town/~mozz
"""

import os
import shutil


def info(text):
    return f'i{text}\t\tnull.host\t1'


def dir(text, selector):
    return f'1{text}\t/~mozz/{selector}\ttilde.town\t70'


def file(text, selector):
    return f'0{text}\t/~mozz/{selector}\ttilde.town\t70'


width = 60
max_section_lines = 100
build_target = os.path.abspath('../public')
title = 'All You Love Will Be Carried Away'
book_file = 'all_you_love_will_be_carried_away.txt'
author = 'By Steven King'

# Use `par` to format the story because it does full-width
# justification better than python's textwrap
cmd = os.popen(f'par -j1 -w{width} < {book_file}')
fulltext = cmd.read().strip()

# Use `wc` to get the word count
cmd = os.popen(f'wc -w < {book_file}')
word_count = cmd.read().strip()

# Split the story into sections based on length
sections = []
for paragraph in fulltext.split('\n\n'):
    lines = paragraph.strip().splitlines()
    if sections and len(lines) + len(sections[-1]) + 1 < max_section_lines:
        sections[-1].extend([''] + lines)
    else:
        sections.append(lines)

# Write each section to a separate file + gophermap
for i, section in enumerate(sections, start=1):

    header = [
        '', title.center(width), f'{author}'.center(width), '',
        f'(part {i} of {len(sections)})'.center(width), '']

    lines = [dir('Information (tilde.town/~mozz/index)', 'index')]
    lines.extend(map(info, header))
    lines.extend(map(info, section))
    if i < len(sections):
        lines.extend([
            info(''),
            dir(f'{title} (Part {i+1} of {len(sections)})', f'p{i+1}'),
            info('(next page)')])

    # Write the gophermap to /p{i}/gophermap
    path = os.path.join(build_target, f'p{i}')
    os.makedirs(path, exist_ok=True)
    filename = os.path.join(path, 'gophermap')
    print(f'Writing {filename}')
    with open(filename, 'w') as fp:
        fp.write('\r\n'.join(lines))

    # Write the plaintext file to /files/p{i}.txt
    path = os.path.join(build_target, 'files')
    os.makedirs(path, exist_ok=True)
    filename = os.path.join(path, f'p{i}.txt')
    print(f'Writing {filename}')
    with open(filename, 'w') as fp:
        fp.write('\r\n'.join(header) + '\r\n')
        fp.write('\r\n'.join(section))

# Build the gophermap for the index page
lines = (
    [
        dir('Information (tilde.town/~mozz/index)', 'index'),
        info('A tiny literature service'),
        info(''),
        info(title),
        info(f'{author}'),
        info(f'({word_count} words)'),
        info(''),
        info('[Directory]')
    ] + [
        dir(f'{title} (Part {i} of {len(sections)})', f'p{i}')
        for i, _ in enumerate(sections, start=1)
    ] + [
        info(''),
        info('[Text Files]'),
    ] + [
        file(f'{title} (Part {i} of {len(sections)})', f'files/p{i}.txt')
        for i, _ in enumerate(sections, start=1)
    ] + [
        info(''),
        info('[Source]'),
        file(f'{book_file}', f'files/{book_file}'),
        info(''),
        info('Have a nice day.'),
    ]
)
path = os.path.join(build_target, 'index')
os.makedirs(path, exist_ok=True)
filename = os.path.join(path, 'gophermap')
print(f'Writing {filename}')
with open(filename, 'w') as fp:
    fp.write('\r\n'.join(lines))

# Copy the first page to the root of the gopherhole
src = os.path.join(build_target, 'p1', 'gophermap')
dst = os.path.join(build_target, 'gophermap')
print(f'Writing {dst}')
shutil.copy(src, dst)

# Copy the book file to the static files directory
src = book_file
dst = os.path.join(build_target, 'files', book_file)
print(f'Writing {dst}')
shutil.copy(src, dst)

print('finished!')
