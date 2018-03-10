#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse, hashlib, os
import pyperclip

def int_to_list(n, base=94): # ascii code: 33~126
    ans = []
    while n > 0:
        ans.append(n % base)
        n //= base
    return ans

def list_to_str(a_list, code_map):
    ans = ''
    for i in a_list:
        ans += code_map[i]
    return ans

def generate_passwd_for_given_url(infile, url, max_length, use_hex, exclude):
    infile = os.path.expanduser(infile)
    with open(infile, 'rb') as f:
        passwd = f.read()
    passwd += bytes(url, 'utf-8')
    passwd = hashlib.sha512(passwd).hexdigest()

    if not use_hex:
        code_map = []
        for i in range(33, 127):
            c = chr(i)
            if c not in exclude:
                code_map.append(c)
        passwd = list_to_str(int_to_list(int(passwd, 16), len(code_map)), code_map)
    else:
        new_passwd = ''
        lower = True
        for c in passwd:
            if c.isalpha():
                if lower:
                    new_passwd += c.upper()
                else:
                    new_passwd += c.lower()
                lower = not lower
            else:
                new_passwd += c
        passwd = new_passwd

    if max_length > 0:
        passwd = passwd[:max_length]
    return passwd

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--infile', default='~/.DrEvil')
    parser.add_argument('-l', '--max_length', type=int, default=32)
    parser.add_argument('--hex', action='store_true')
    parser.add_argument('--print', action='store_true')
    parser.add_argument('--exclude', default='')
    parser.add_argument('URL')
    args = parser.parse_args()
    passwd = generate_passwd_for_given_url(args.infile, args.URL, args.max_length, args.hex, args.exclude)
    if not args.print:
        pyperclip.copy(passwd)
    else:
        print(passwd)

if __name__ == '__main__':
    main()
