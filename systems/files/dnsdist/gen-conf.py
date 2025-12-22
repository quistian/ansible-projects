#!/usr/bin/env python3

import io
import sys
from pathlib import Path

'''

generate the dnsdist configuration file

-- These are comments

Here are the data types:
    Server: generated with newServer()
    ComboAddress: represents an IP address and Port
    DNSName: represents a FQDN
    Netmask: represents a netmask or network
    NetmaskGroup: represents a group of netmasks
    SuffixMatchNode: represents a group of domain suffixes for fast searching
    DNSHeader: a header of a DNS packet
    ClientState: the addresses and ports that dnsdist is listening on

'''

DnsDistDir = '/etc/dnsdist'
GlobalAcl = 'global.acl'
AzureAcl = 'on-prem-azure-nets'
AzurePrivZones = 'azure-priv-zones'
AzurePubZones = 'azure-pub-zones'
LocalZones = 'local-zones'
LocalZones = 'forward.zones'
ArpaZones = 'arpa.zones'
TypoZones = 'typo.zones'

Ans1 = '128.100.235.12'
Ans2 = '128.100.213.12'
LocalHost = '127.0.0.1'
Dns1 = '128.100.100.128'
Dns4 = '128.100.56.130'
Dns4Resolver = '128.100.56.130'
Dns5 = '128.100.96.34'
Cira1 = '149.112.121.10'
Cira2 = '149.112.122.10'
CloudF = '1.1.1.1'
Four9s = '9.9.9.9'

MyIp = Dns4

LocalPort = 5353
Port = 53
ControlPort = 5333
WebPort = 8088

EISNet = '128.100.102.0/23'
SafeNets = '{\'127.0.0.1/8\', \'128.100.56.128/27\', \'128.100.102.0/23\'}'
DefServer = {'128.100.96.34': 'dns5'}

'''
        'dns4pdnsreolver': Dns4Resolver,
        'cloudflare': CloudF,
        '4nines': Four9s,
'''

Pools = {
    '': {
        'cira1': Cira1,
        'cira2': Cira2,
    },
    'local': {
        'dns1': Dns1,
        'dns5': Dns5,
        'localhost': LocalHost,
    },
    'bluecat': {
        'ans1': Ans1,
        'ans2': Ans2,
    },
    'azure_prod': {
        'prod1': '142.1.78.12',
        'prod2': '142.1.78.13',
        'prod3': '142.1.78.14',
        'prod4': '142.1.78.15',
    },
    'azure_qa': {
        'qa1': '142.150.247.12',
        'qa2': '142.150.247.13',
        'qa3': '142.150.247.14',
        'qa4': '142.150.247.15',
    },
    'typo': {'blackhole': '128.100.100.129'},
}

WebPw = 'John1717'
ApiKey = 'fichoo2Choh8'

CacheSize = 100000

#    print(f'includeDirectory("{DnsDistDir}")')

def glob():
    print('-- Listen Sockets')
    print(f'setLocal("{LocalHost}:{LocalPort}")')
    print(f"addLocal('{Dns4}:{Port}')")

    print("\n-- Control Socket, Console and Webserver")
    print(f"controlSocket('{LocalHost}:{ControlPort}')")
    print("setKey('QfhaEHPbEM+zPBR1tQe6K6pceGorSbqxZLoZtFrcPLw=')")
    print(f"setConsoleACL({SafeNets})")

    print(f"webserver('{MyIp}:{WebPort}')")
    print(f"setWebserverConfig({{password='{WebPw}', apiKey='{ApiKey}', acl='{EISNet}'}})")

    print("\n-- Access Control Lists")
    print(f"setACLFromFile('{DnsDistDir}/{GlobalAcl}')")

def servers():
    print("\n-- Pools")
    for pool in Pools:
        pdict = Pools[pool]
#        print(f"setPoolServerPolicy(roundrobin, '{pool}')")
        for srv in pdict:
            print(f"newServer({{name='{srv}', address='{pdict[srv]}', pool='{pool}'}})")
    print("\n-- Packet Caches")
    print(f"pc = newPacketCache({CacheSize})")
    print("getPool(''):setCache(pc)")

def dynamic_blocks():
    rate = 60
    brate = 40000
    exceed = 15
    block = 60
    print("\n-- Dynamic Blocks")
    print("local dbr = dynBlockRulesGroup()")
    print(f"dbr:setQueryRate({rate}, {exceed}, 'Exceeded query rate', {block})")
    print(f"dbr:setRCodeRate(DNSRCode.NXDOMAIN, {rate}, {exceed}, 'Exceeded NXD rate', {block})")
    print(f"dbr:setRCodeRate(DNSRCode.SERVFAIL, {rate}, {exceed}, 'Exceeded ServFail rate', {block})")
    print(f"dbr:setQTypeRate(DNSQType.ANY, {int(rate/1.5)}, {exceed}, 'Exceeded ANY rate', {block})")
    print(f"dbr:setResponseByteRate({brate}, {exceed}, 'Exceeded Byte rate', {block})") 

def net_mask_groups():
    print("\n-- NetMask Groups")
    aclf = f"{DnsDistDir}/{AzureAcl}"
    print("az_nmg = newNMG()")
    lines = Path(aclf).read_text().splitlines()
    for l in lines:
        if l[0] != '#':
            print(f"az_nmg:addMask('{l}')")

def suffix_match_nodes():
    print("\n-- Suffix Match Nodes")

    azure_priv_f = f"{DnsDistDir}/{AzurePrivZones}"
    azure_pub_f = f"{DnsDistDir}/{AzurePubZones}"

    print("azure_priv_smn = newSuffixMatchNode()")
    lines = Path(azure_priv_f).read_text().splitlines()
    for l in lines:
        if l[0] != '#':
            print(f"azure_priv_smn:add('{l}')")

    print("azure_pub_smn = newSuffixMatchNode()")
    lines = Path(azure_pub_f).read_text().splitlines()
    for l in lines:
        if l[0] != '#':
            print(f"azure_pub_smn:add('{l}')")

    print()
    local_names = f"{DnsDistDir}/{LocalZones}"
    print("local_smn = newSuffixMatchNode()")
    lines = Path(local_names).read_text().splitlines()
    for l in lines:
        if l[0] != '#':
            print(f"local_smn:add('{l}')")

    print()
    arpa_names = f"{DnsDistDir}/{ArpaZones}"
    print("arpa_smn = newSuffixMatchNode()")
    lines = Path(arpa_names).read_text().splitlines()
    for l in lines:
        if l[0] != '#':
            print(f"arpa_smn:add('{l}')")

    print()
    typo_names = f"{DnsDistDir}/{TypoZones}"
    print("typo_smn = newSuffixMatchNode()")
    lines = Path(typo_names).read_text().splitlines()
    for l in lines:
        if l[0] != '#':
            print(f"typo_smn:add('{l}')")

def regex_patterns():
    digits_dot = '[0-9]{3}.*\\\.'
    print("\n-- Regex Rules")
    print("ams_prefix = RegexRule('[DQS]301AMS.*\\\.')")
    print(f"prod_prefix = RegexRule('^[NP]{digits_dot}')")
    print(f"qa_prefix = RegexRule('^[DQS]{digits_dot}')")

def selectors():
    print("\n-- Selectors")
    print("azure_net_rule = NetmaskGroupRule(az_nmg)")
    print("local_name_rule = SuffixMatchNodeRule(local_smn)")
    print("arpa_rule = SuffixMatchNodeRule(arpa_smn)")
    print("typo_rule = SuffixMatchNodeRule(typo_smn)")
    print("azure_priv_name_rule = SuffixMatchNodeRule(azure_priv_smn)")
    print("azure_pub_name_rule = SuffixMatchNodeRule(azure_pub_smn)")
    print("prod_prefix_rule = OrRule({prod_prefix, ams_prefix})")
    print("azure_prefix_rule = OrRule({prod_prefix, qa_prefix})")
    print("prod_selector = AndRule({azure_net_rule, azure_priv_name_rule, prod_prefix_rule})")
    print("qa_selector = AndRule({azure_net_rule, azure_priv_name_rule, qa_prefix})")
    print("no_recurse_selector = AndRule({azure_net_rule, azure_pub_name_rule, azure_prefix_rule})")

def actions():
    print("\n-- Actions")
    print("addAction(local_name_rule, PoolAction('local'))")
    print("addAction(no_recurse_selector, PoolAction('local'))")
    print("addAction(arpa_rule, PoolAction('bluecat'))")
    print("addAction(typo_rule, PoolAction('typo'))")
    print("addAction(prod_selector, PoolAction('azure_prod'))")
    print("addAction(qa_selector, PoolAction('azure_qa'))")

def lua_functions():
    print("\n-- Functions")
    print("function mainentance()")
    print("    dbr:apply()")
    print("end")

def main():
    glob()
    servers()
    dynamic_blocks()
    net_mask_groups()
    suffix_match_nodes()
    regex_patterns()
    selectors()
    actions()
    #lua_functions()

if __name__ == '__main__':
    sys.exit(main())
