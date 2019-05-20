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


width = 60
max_section_lines = 100
build_target = os.path.abspath('../public')
title = 'All You Love Will Be Carried Away'
author = 'By Steven King'

# Use `par` to format the story because it does full-width
# justification better than python's textwrap
cmd = os.popen(f'par -j1 -w{width} < fulltext.txt')
fulltext = cmd.read()

# Use `wc` to get the word count
cmd = os.popen('wc -w < fulltext.txt')
word_count = cmd.read().strip()

# Split the story into sections based on length
sections = [[]]
for paragraph in fulltext.split('\n\n'):
    lines = paragraph.strip().splitlines()
    if len(lines) + len(sections[-1]) + 1 < max_section_lines:
        sections[-1].extend([''] + lines)
    else:
        sections.append(lines)

# Build the gophermaps for the story sections
for i, section in enumerate(sections, start=1):
    lines = [
        dir('tilde.town/~mozz (information)', 'index'),
        info(''),
        info(title.center(width)),
        info(author.center(width)),
        info(f'(Part {i} of {len(sections)})'.center(width)),
        info('')]

    lines.extend(map(info, section))

    if i < len(sections):
        lines.extend([
            info(''),
            dir(f'{title} (Part {i+1} of {len(sections)})', f'p{i+1}'),
            info('(next page)')])

    path = os.path.join(build_target, f'p{i}')
    os.makedirs(path, exist_ok=True)
    filename = os.path.join(path, 'gophermap')
    print(f'Writing {filename}')
    with open(filename, 'w') as fp:
        fp.write('\r\n'.join(lines))

# Build the gophermap for the index page
lines = [
    dir('tilde.town/~mozz', 'index'),
    info('"An itty-bitty literature portal"'),
    info(''),
    info(title),
    info(author),
    info(f'({word_count} words)'),
    info(''),
    info('[index]')]
lines.extend([
    dir(f'{title} (Part {i} of {len(sections)})', f'p{i}')
    for i, _ in enumerate(sections, start=1)])
lines.extend([
    info(''),
    '1visit my other gopherhole at mozz.us\t/\tmozz.us\t70'])

path = os.path.join(build_target, 'index')
os.makedirs(path, exist_ok=True)
filename = os.path.join(path, 'gophermap')
print(f'Writing {filename}')
with open(filename, 'w') as fp:
    fp.write('\r\n'.join(lines))

# Copy the first page to the root of the gopherhole
src = os.path.join(build_target, 'p1', 'gophermap')
dst = os.path.join(build_target, 'gophermap')
shutil.copy(src, dst)

print('finished!')
