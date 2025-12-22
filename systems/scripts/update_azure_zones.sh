#!/bin/bash
# scripts/update_azure_zones.sh

cd "$(dirname "$0")/.."

echo "Extracting Azure DNS zones..."
./scripts/extract_priv_pub_names.py \
    files/azure_pvdns_zones.json \
    --endings com net io org \
    --private-output files/private_dns_zones.txt \
    --public-output files/public_dns_forwarders.txt

# echo "Deploying dnsdist configuration..."
# ansible-playbook playbooks/configure_dnsdist.yml
