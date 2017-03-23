#!/usr/bin/env python2.7

import yaml


def get_blocked_domain_string(blocked_domains):
    return '|'.join([x.replace('.', '\.') + '@' for x in blocked_domains])


def get_name(name):
    return name.replace('.', '\.')


def get_virtual_line(name, blocked_domains, recipient):
    return "/^(?!{blocked_domains}).*@{name}$/  {recipient}".format(
        blocked_domains=get_blocked_domain_string(blocked_domains),
        name=get_name(name),
        recipient=recipient)

POSTFIX_VIRTUAL_FILENAME = '/etc/postfix/virtual'

try:
    with open('build_postfix_virtual.yaml') as f:
        conf = yaml.load(f)
except IOError:
    print("Missing build_postfix_virtual.yaml file")
    exit(1)

new_content = []

with open(POSTFIX_VIRTUAL_FILENAME) as infile:
    content = infile.readlines()

addresses_found = []

file_updated = False
for line in content:
    line_updated = False
    for address in conf['addresses']:
        if line.strip().endswith('@{name}$/  {recipient}'.format(
                name=get_name(address['name']),
                recipient=address['recipient'])):
            addresses_found.append(address['name'])
            virtual_line = get_virtual_line(address['name'],
                                            address['blocked_domains'],
                                            address['recipient'])
            if line.strip() == virtual_line:
                print('No change detected in {name}.'.format(
                    name=address['name']))
            else:
                print('Updating line for {name}'.format(
                    name=address['name']))
                new_content.append(virtual_line + "\n")
                line_updated = True
                file_updated = True
    if not line_updated:
        new_content.append(line)

for address in [x for x in conf['addresses']
                if x['name'] not in addresses_found]:
    print('Adding line for {name}'.format(
        name=address['name']))
    virtual_line = get_virtual_line(address['name'],
                                    address['blocked_domains'],
                                    address['recipient'])
    new_content.append(virtual_line + "\n")
    file_updated = True

if file_updated:
    print('Updating file')
    with open(POSTFIX_VIRTUAL_FILENAME, 'w') as outfile:
        for line in new_content:
            outfile.write(line)
else:
    print('No changes, file unmodified.')
