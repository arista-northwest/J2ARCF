#!/usr/bin/env python3

import re, sys, os, argparse

READ_FILE = '/Users/paulc/Desktop/Demo/J2A.txt'

###############################################################################
##### J2A-RCF TOOL ############################################################
##### msft-team@arista.com ####################################################
# VERSION 1.0 - paulc   - Initial config conversion concept
# VERSION 1.1 - paulc   - Additional RCF features, parser arg, operator logic, regex function, clean up

###############################################################################
# ARGUMENTS TO PASS INTO THE TOOL
###############################################################################

parser = argparse.ArgumentParser(description = 'Define what additional translations you want to append to the converted policy')
parser.add_argument('--jshow', help='Append a build for the JUNOS policy after every RCF policy created')
parser.add_argument('--ipv4', help='Append a build for the IPv4 prefix-lists found in the JUNOS policy')
parser.add_argument('--ipv6', help='Append a build for the IPv6 prefix-lists found in the JUNOS policy')
parser.add_argument('--com', help='Append a build for the community lists found in the JUNOS policy')
parser.add_argument('--extcom', help='Append a build for the extended community lists found in the JUNOS policy')
parser.add_argument('--aspath', help='Append a build for the as path lists found in the JUNOS policy')
args = parser.parse_args()

###############################################################################
# PARSE POLICY FUNCTION
###############################################################################
def parsepolicy ():
    global v, ta, v4list, v6list, v6f, ost, osf

    pv = ['protocol bgp', 'as-path', 'color', 'route-filter', 'protocol direct', 'from interface', 'prefix-list', 'community',
    'protocol static', 'tag', 'from policy', 'protocol aggregate', 'inet6', 'route-type external', 'aggregate-contributor']

    if re.search(pv[0], row):
        v0 = row.split()
        v = row.replace(row, 'source_protocol is bgp')
        print (opers + v + opere)
    elif re.search(pv[1], row):
        v0 = row.split()
        v = row.replace(row, 'as-path match as_path_list ' + v0[-1])
        ta = 'ip as-path access-list ' + v0[-1] + ' permit 10 any'
        asp.add(ta)
        print (opers + v + opere)
    elif re.search(pv[2], row):
        v0 = row.split()
        v = row.replace(row, 'ext_community match ext_community_list COLOR_' + v0[-1])
        ta = 'ip extcommunity-list COLOR_' + v0[-1] + ' color ' + v0[-1]
        ecml.add(ta)
        print (opers + v + opere)
    elif re.search(pv[3], row):
        v0 = row[row.find(pv[3]) + len(pv[3]):]
        if re.search(IPV4ADDR, v0) and v4list == True:
            print (opers + 'prefix match prefix_list_v4 ' + term + ' {')
            v4list = False
        if re.search(IPV6ADDR, v0) and v6list == True:
            print (opers + 'prefix match prefix_list_v6 ' + term + ' {')
            v6list = False
        if re.search('orlonger', v0) and re.search(IPV4ADDR, v0):
            ta = ('ip prefix-list ' + term +  ' ' + v0.split()[-2] + ' ge ' + v0[v0.index('/') + 1:v0.index('/') + 3])
            ipv4.add(ta)
        if re.search('orlonger', v0) and re.search(IPV6ADDR, v0):
            ta = ('ipv6 prefix-list ' + term +  ' ' + v0.split()[-2] + ' ge ' + v0[v0.index('/') + 1:v0.index('/') + 3])
            ipv6.add(ta)
        if re.search('exact', v0) and re.search(IPV4ADDR, v0):
            ta = ('ip prefix-list ' + term +  ' ' + v0.split()[-2])
            ipv4.add(ta)
        if re.search('exact', v0) and re.search(IPV6ADDR, v0):
            ta = ('ipv6 prefix-list ' + term +  ' ' + v0.split()[-2])
            ipv6.add(ta)
        if re.search('upto', v0) and re.search(IPV4ADDR, v0):
            ta = ('ip prefix-list ' + term +  ' ' + v0.split()[-3] + ' le ' + v0.split()[-1] )
            ipv4.add(ta)
        if re.search('upto', v0) and re.search(IPV6ADDR, v0):
            ta = ('ipv6 prefix-list ' + term +  ' ' + v0.split()[-3] + ' le ' + v0.split()[-1] )
            ipv6.add(ta)
        if re.search('prefix-length-range', v0) and re.search(IPV4ADDR, v0):
            ta = ('ip prefix-list ' + term +  ' ' + v0.split()[-3] + ' ge ' + v0.split()[-1].replace('-', ' le ') )
            ipv4.add(ta)
        if re.search('prefix-length-range', v0) and re.search(IPV6ADDR, v0):
            ta = ('ipv6 prefix-list ' + term +  ' ' + v0.split()[-3] + ' ge '+ v0.split()[-1].replace('-', ' le ') )
            ipv6.add(ta)
    elif re.search(pv[4], row):
        v0 = row.split()
        v = row.replace(row, 'source_protocol is CONNECTED')
        print (opers + v + opere)
    elif re.search(pv[5], row):
        v0 = row.split()
        v = row.replace(row, 'connected.interface is Loopback0')
        print (opers + v + opere)
    elif re.search(pv[6], row):
        v0 = row.split()
        if v0[-1].find('v6'):
            print (opers + 'prefix match prefix_list_v6 ' + v0[-1] + ' {')
        else:
            print (opers + 'prefix match prefix_list_v4 ' + v0[-1] + ' {')
    elif re.search(pv[7], row):
        v0 = row.split()
        v = row.replace(row, 'community match community_list ' + v0[-1])
        ta = 'ip community-list ' + v0[-1] + ' permit 10 any'
        cml.add(ta)
        print (opers + v + opere)
    elif re.search(pv[8], row):
        v0 = row.split()
        v = row.replace(row, 'source_protocol is STATIC')
        print (opers + v + opere)
    elif re.search(pv[9], row):
        v0 = row.split()
        v = row.replace(row, 'igp.tag is ' + v0[-1])
        print (opers + v + opere)
    elif re.search(pv[10], row):
        v6f = True
    elif re.search(pv[11], row):
        if v6f == True:
            v = row.replace(row, '### BGP AGGREGATE WORKAROUND ###\n' + opers + 'prefix match prefix_list_v6 AGGREGATES-V6')
        else:
            v = row.replace(row, '### BGP AGGREGATE WORKAROUND ###\n' + opers + 'prefix match prefix_list_v4 AGGREGATES-V4')
        print (v + opere)
    elif re.search(pv[12], row):
        v6f = True
        if cp == []:
            osf = True
        else:
            ost = True
    elif re.search(pv[13], row):
        v0 = row.split()
        v = row.replace(row, '### ROUTE TYPE EXTERNAL NEW FEATURE ###\n' + opers + '# route-type is EXTERNAL')
        print (v + opere)
    elif re.search(pv[14], row):
        if v6f == True:
            v = row.replace(row, '### BGP AGGREGATE CONTRIBUTOR WORKAROUND ###\n' + opers + 'prefix match prefix_list_v6 AGGREGATES-V6')
        else:
            v = row.replace(row, '### BGP AGGREGATE CONTRIBUTOR WORKAROUND ###\n' + opers + 'prefix match prefix_list_v4 AGGREGATES-V4')
        print (v + opere)
    else:
        print('UNDEFINED FROM STATEMENT')

###############################################################################
# SET VALUES FUNCTION
###############################################################################
def setvalue ():
    global v, ta

    sv = ['local-preference', 'then accept', 'apply-groups', 'next term', 'as-path-prepend', 'then reject', 'metric', 'community add',
    'next policy', 'tag', 'community set', 'community delete all' , 'color ', 'next-hop self', 'community delete', 'next-hop']

    if re.search(sv[0], row):
        v0 = row.split()
        v = row.replace(row, 'local-preference = ' + v0[-1] + ';')
        print (v)
    elif re.search(sv[1], row) or re.search('action accept', row):
        v0 = row.split()
        v = row.replace(row, 'return true' + ';')
        print (v)
    elif re.search(sv[2], row):
        v0 = row.split()
        v = row.replace(row, '# APPLY-GROUPS N/A')
        print (v)
    elif re.search(sv[3], row):
        pass
    elif re.search(sv[4], row):
        v0 = row[row.find(sv[4]) + len(sv[4]):-1]
        v = ('as_path prepend' + v0.replace('"', '') + ';')
        print (v)
    elif re.search(sv[5], row):
        v0 = row.split()
        v = row.replace(row, opert + 'return false;')
        print (v)
    elif re.search(sv[6], row):
        v0 = row.split()
        v = row.replace(row, 'med = ' + v0[-1] + ';')
        print (v)
    elif re.search(sv[7], row):
        v0 = row.split()
        v = row.replace(row, 'community add community_list ' + v0[-1] + ';')
        ta = ('ip community-list ' + v0[-1] + 'permit 10')
        cml.add(ta)
        print (v)
    elif re.search(sv[8], row):
        pass
    elif re.search(sv[9], row):
        v0 = row.split()
        v = row.replace(row, 'igp.tag = ' + v0[-1] + ';')
        print (v)
    elif re.search(sv[10], row):
        v0 = row.split()
        v = row.replace(row, 'community = community_list ' + v0[-1] + ';')
        ta = ('ip community-list ' + v0[-1] + 'permit 10')
        cml.add(ta)
        print (v)
    elif re.search(sv[11], row):
        v0 = row.split()
        v = row.replace(row, '### COMMUNITY DELETE ALL NEW FEATURE ###')
        print (v)
    elif re.search(sv[12], row):
        v0 = row.split()
        v = row.replace(row, 'ext_community add ext_community_list COLOR_' + v0[-1] + ';')
        ta = 'ip extcommunity-list COLOR_' + v0[-1] + ' color ' + v0[-1]
        ecml.add(ta)
        print (v)
    elif re.search(sv[13], row):
        v0 = row.split()
        v = row.replace(row, '### NEXT-HOP SELF NEW FEATURE ###\n# next-hop = self;')
        print (v)
    elif re.search(sv[14], row):
        v0 = row.split()
        v = row.replace(row, 'community remove ' + v0[-1] + ';')
        print (v)
    elif re.search(sv[15], row):
        v0 = row.split()
        v = row.replace(row, '### NEXT-HOP IP NEW FEATURE ###\n# next-hop = ' + v0[-1] + ';')
        print (v)
    else:
        print('UNDEFINED TO STATEMENT')

###############################################################################
# OPERATOR FUNCTION(s)
###############################################################################
def operatorpv ():
    global osf, ost, opers, opere, opert

    oper    = open(READ_FILE)
    lines   = oper.readlines()

    try:
        line    = lines[li]
        if re.search('protocol ', line) or re.search('interface', line):
            opere = ' or'
        elif re.search('policy ', line):
            opere = ' {'
        elif re.search('from ', line):
            opere = ' and'
        elif re.search('then ', line):
            opere = ' {'
    except:
        variable = 'pass'

    if osf == True:
        opers = 'if '
        osf = False
        ost = False
    elif ost == True:
        opers = '} else if '
        ost = False
    else:
        opers = ''


def operatorsv ():
    global opert

    oper    = open(READ_FILE)
    lines   = oper.readlines()

    try:
        line    = lines[li]
        if re.search('then ', line) and re.search('reject', line):
            opert = '} else {\n'
        elif term == 'NO TERM FOUND':
            opert = '} else {\n'
        else:
            opert =''
    except:
        variable = 'pass'

###############################################################################
# APPEND JUNOS POLICY FUNCTION
###############################################################################
def appj ():
    global cp

    if nf != 'NEW FUNC':
        print ('  }\n}\n\n')

    if nf != func and cp != []:
        if args.jshow:
            jpolicy = '# '.join([str(item) for item in cp])
            print(fmt4 + ' CONVERTED JUNOS POLICY ' + fmt4 + '\n# ' + jpolicy +'\n')
            cp = []

    # USE TO DEBUG
    #if nf != func and cp != []:
    #    jpolicy = '# '.join([str(item) for item in cp])
    #    print(fmt4 + ' CONVERTED JUNOS POLICY ' + fmt4 + '\n# ' + jpolicy +'\n')
    #    cp = []

###############################################################################
# APPEND ADDITIONAL
###############################################################################
def append ():
    global ipv4v, ipv6v, ecmlv, cmlv, aspv, cp

    print ('  }\n}\n\n')

    print (fmt4 + '## END OF CONVERSION ###' + fmt4 + '\n\n')

    if args.jshow:
        jpolicy = '# '.join([str(item) for item in cp])
        print(fmt4 + ' CONVERTED JUNOS POLICY ' + fmt4 + '\n# ' + jpolicy +'\n')
        cp = []

    if args.ipv4:
        ipv4v = '\n'.join(ipv4)
        print (fmt5 + '### IPv4 PREFIX-LIST ####' + fmt5 + '\n' + ipv4v)

    if args.ipv6:
        ipv6v = '\n'.join(ipv6)
        print (fmt5 + '### IPv6 PREFIX-LIST ####' + fmt5 + '\n' + ipv6v)

    if args.extcom:
        ecmlv = '\n'.join(ecml)
        print (fmt5 + '### EXT-COMM LIST ##' + fmt5 + '\n' + ecmlv)

    if args.com:
        cmlv = '\n'.join(cml)
        print (fmt5 + '##### COM LIST #####' + fmt5 + '\n' + cmlv)

    if args.aspath:
        aspv = '\n'.join(asp)
        print (fmt5 + '### AS-PATH LIST ###' + fmt5 + '\n' + aspv)


with open(READ_FILE) as r:
###############################################################################
# VARIABLES
###############################################################################
    li      = 0
    nf      = 'NEW FUNC'
    nt      = 'NEW TERM'
    v4list  = False
    v6list  = False
    v6f     = False
    cp      = [] # JUNOS POLICY LIST
    ipv4    = set([]) # IPv4 PREFIX LIST
    ipv6    = set([]) # IPv6 PREFIX LIST
    asp     = set([]) # AS-PATH LIST
    cml     = set([]) # COMMUNITY LIST
    ecml    = set([]) # EXTENDED COMMUNITY LIST
###############################################################################
# REGEX CHECKER
###############################################################################
    regipv4 = ("(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\\.){3}([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])")
    IPV4SEG  = r'(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])'
    IPV4ADDR = r'(?:(?:' + IPV4SEG + r'\.){3,3}' + IPV4SEG + r')'
    IPV6SEG  = r'(?:(?:[0-9a-fA-F]){1,4})'
    IPV6GROUPS = (
        r'(?:' + IPV6SEG + r':){7,7}' + IPV6SEG,                  # 1:2:3:4:5:6:7:8
        r'(?:' + IPV6SEG + r':){1,7}:',                           # 1::                                 1:2:3:4:5:6:7::
        r'(?:' + IPV6SEG + r':){1,6}:' + IPV6SEG,                 # 1::8               1:2:3:4:5:6::8   1:2:3:4:5:6::8
        r'(?:' + IPV6SEG + r':){1,5}(?::' + IPV6SEG + r'){1,2}',  # 1::7:8             1:2:3:4:5::7:8   1:2:3:4:5::8
        r'(?:' + IPV6SEG + r':){1,4}(?::' + IPV6SEG + r'){1,3}',  # 1::6:7:8           1:2:3:4::6:7:8   1:2:3:4::8
        r'(?:' + IPV6SEG + r':){1,3}(?::' + IPV6SEG + r'){1,4}',  # 1::5:6:7:8         1:2:3::5:6:7:8   1:2:3::8
        r'(?:' + IPV6SEG + r':){1,2}(?::' + IPV6SEG + r'){1,5}',  # 1::4:5:6:7:8       1:2::4:5:6:7:8   1:2::8
        IPV6SEG + r':(?:(?::' + IPV6SEG + r'){1,6})',             # 1::3:4:5:6:7:8     1::3:4:5:6:7:8   1::8
        r':(?:(?::' + IPV6SEG + r'){1,7}|:)',                     # ::2:3:4:5:6:7:8    ::2:3:4:5:6:7:8  ::8       ::
        r'fe80:(?::' + IPV6SEG + r'){0,4}%[0-9a-zA-Z]{1,}',       # fe80::7:8%eth0     fe80::7:8%1  (link-local IPv6 addresses with zone index)
        r'::(?:ffff(?::0{1,4}){0,1}:){0,1}[^\s:]' + IPV4ADDR,     # ::255.255.255.255  ::ffff:255.255.255.255  ::ffff:0:255.255.255.255 (IPv4-mapped IPv6 addresses and IPv4-translated addresses)
        r'(?:' + IPV6SEG + r':){1,4}:[^\s:]' + IPV4ADDR,          # 2001:db8:3:4::192.0.2.33  64:ff9b::192.0.2.33 (IPv4-Embedded IPv6 Address)
    )
    IPV6ADDR = '|'.join(['(?:{})'.format(g) for g in IPV6GROUPS[::-1]])


###############################################################################
# VISUAL FORMAT
###############################################################################
    fmt1    = ('#' * 30 + ' FUNCTION ' + '#' * 30)
    fmt2    = ('#' * 30 + '## TERM ##' + '#' * 30)
    fmt3    = ('#' * 70)
    fmt4    = ('#' * 35)
    fmt5    = ('#' * 25)
###############################################################################
# FUNC MAIN
###############################################################################
    for row in r:
        li += 1
        ix = row.split()
        if row.find('term') != -1:
            func = (ix[ix.index('term')-1]).replace('-', '_').upper()
            term = (ix[ix.index('term')+1]).upper()
        elif row.find != None and row.find('term') == -1:
            term = 'NO TERM FOUND'
            operatorsv()
        if nf != func:
            appj ()
            nf = func
            nt = ''
            osf = True
            print (fmt1 + '\n' + 'function ' + func + ' () {')
        if nt != term:
            nt = term
            ost = True
            v4list = True
            v6list = True
            v6f = False
            print (fmt2 + '\n' + '# ' + term + '\n' + fmt3)
        if re.search('policy-statement' and 'from ', row):
            operatorpv()
            parsepolicy()
        elif re.search('policy-statement' and 'then ', row):
            operatorsv()
            setvalue()
        cp.append(row)
###############################################################################
# APPEND ADDTIONAL PASSED ARGUMENTS
###############################################################################
append ()
