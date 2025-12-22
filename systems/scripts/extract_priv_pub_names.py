#!/usr/bin/env python3
"""
Extract Azure Private DNS zone names and Public DNS zone forwarders from JSON file.
"""

import json
import sys
import argparse
import yaml

from pathlib import Path


def extract_dns_zones(json_file, private_output="private_dns_zones.txt", 
                      public_output="public_dns_forwarders.txt",
                      exclude_envs=None,
                      filter_domains=None,
                      endings=None):
    """
    Read Azure DNS mapping JSON and extract zone names to separate files.
    
    Args:
        json_file: Path to input JSON file
        private_output: Output file for private DNS zone names
        public_output: Output file for public DNS zone forwarders
        exclude_envs: List of cloud environments to exclude (e.g., ['China', 'USGovernment'])
        filter_domains: List of domain patterns to filter out (e.g., ['.us', '.cn'])
        endings: List of TLD endings to include (e.g., ['com', 'net', 'io', 'org'])
                If specified, only domains ending with these will be included
    """
    
    # Read JSON file
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{json_file}' not found")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in '{json_file}': {e}")
        sys.exit(1)
    
    # Set default exclusions if not provided
    if exclude_envs is None:
        exclude_envs = []
    
    if filter_domains is None:
        filter_domains = []
    
    if endings is None:
        endings = []
    
    def should_filter_domain(domain_name):
        """Check if domain should be filtered based on patterns."""
        # If endings whitelist is specified, only include domains ending with those
        if endings:
            # Normalize the domain name and check if it ends with any allowed ending
            for ending in endings:
                # Add dot prefix if not present in the ending
                ending_pattern = ending if ending.startswith('.') else f'.{ending}'
                if domain_name.endswith(ending_pattern):
                    return False  # Don't filter - it matches an allowed ending
            return True  # Filter out - doesn't match any allowed ending
        
        # Otherwise use the blacklist filter
        if not filter_domains:
            return False
        for pattern in filter_domains:
            if pattern in domain_name:
                return True
        return False
    
    # Use sets to store unique values
    private_zones = set()
    public_forwarders = set()
    filtered_count = 0
    
    # Iterate through the JSON structure
    # Structure: Commercial/China/USGovernment -> Categories -> List of resources
    for cloud_env, categories in data.items():
        # Skip excluded environments
        if cloud_env in exclude_envs:
            print(f"Skipping environment: {cloud_env}")
            continue
            
        if not isinstance(categories, dict):
            continue
            
        for category, resources in categories.items():
            if not isinstance(resources, list):
                continue
                
            for resource in resources:
                # Extract private DNS zone name
                if "Private DNS zone name" in resource:
                    private_zone = resource["Private DNS zone name"]
                    if private_zone:  # Only add non-empty values
                        if should_filter_domain(private_zone):
                            filtered_count += 1
                        else:
                            if '{regionName}' in private_zone:
                                cc = private_zone.replace('{regionName}', 'canadacentral')
                                ce = private_zone.replace('{regionName}', 'canadaeast')
                                private_zones.add(cc)
                                private_zones.add(ce)
                            elif '{regionCode}' in private_zone:
                                cc = private_zone.replace('{regionCode}', 'cc')
                                ce = private_zone.replace('{regionCode}', 'ce')
                                private_zones.add(cc)
                                private_zones.add(ce)
                            else:
                                private_zones.add(private_zone)
                
                # Extract public DNS zone forwarders
                if "Public DNS zone forwarders" in resource:
                    forwarders = resource["Public DNS zone forwarders"]
                    if isinstance(forwarders, list):
                        for forwarder in forwarders:
                            if forwarder:  # Only add non-empty values
                                if should_filter_domain(forwarder):
                                    filtered_count += 1
                                else:
                                    public_forwarders.add(forwarder)
    
# Write private DNS zones to a yaml file

    pzones = {"azure_private_zones": sorted(private_zones)}
    group_vars_path = Path.home() / "systems" / "inventory" / "group_vars"
    private_zone_path = group_vars_path / "dnsdist_servers" / "private_zones.yaml"
    with open(private_zone_path, 'w') as f:
        yaml.safe_dump(
            pzones,
            f,
            default_flow_style=False,
            sort_keys=False,
            indent=2,
            explicit_start=True,
            allow_unicode=True
        )

    #with open(private_output, 'w') as f:
    #for zone in sorted(private_zones):
    #    f.write(f"{zone}\n")

    # Write public DNS forwarders to file
    with open(public_output, 'w') as f:
        for forwarder in sorted(public_forwarders):
            f.write(f"{forwarder}\n")

    # Print summary
    print(f"Extraction complete!")
    print(f"  Private DNS zones: {len(private_zones)} unique entries -> {private_output}")
    print(f"  Public DNS forwarders: {len(public_forwarders)} unique entries -> {public_output}")
    if endings:
        print(f"  Only included domains ending with: {endings}")
        print(f"  Filtered out: {filtered_count} entries")
    elif filter_domains:
        print(f"  Filtered domains (matching {filter_domains}): {filtered_count} entries")


if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Extract Azure Private DNS zone names and Public DNS zone forwarders from JSON file."
    )
    parser.add_argument(
        'input_file',
        nargs='?',
        default='azure_dns_mapping.json',
        help='Input JSON file (default: azure_dns_mapping.json)'
    )
    parser.add_argument(
        '--exclude',
        nargs='+',
        default=[],
        metavar='ENV',
        help='Cloud environments to exclude (e.g., --exclude China USGovernment)'
    )
    parser.add_argument(
        '--exclude-china-us',
        action='store_true',
        help='Shortcut to exclude both China and USGovernment environments and filter .us/.cn domains'
    )
    parser.add_argument(
        '--filter-domains',
        nargs='+',
        default=[],
        metavar='PATTERN',
        help='Filter out DNS names containing these patterns (e.g., --filter-domains .us .cn)'
    )
    parser.add_argument(
        '--endings',
        nargs='+',
        default=[],
        metavar='TLD',
        help='Only include domains ending with these TLDs (e.g., --endings com net io org). Overrides --filter-domains.'
    )
    parser.add_argument(
        '--private-output',
        default='private_dns_zones.txt',
        help='Output file for private DNS zones (default: private_dns_zones.txt)'
    )
    parser.add_argument(
        '--public-output',
        default='public_dns_forwarders.txt',
        help='Output file for public DNS forwarders (default: public_dns_forwarders.txt)'
    )
    
    args = parser.parse_args()
    
    # Handle shortcut flag
    exclude_envs = list(args.exclude)
    filter_domains = list(args.filter_domains)
    endings = list(args.endings)
    
    if args.exclude_china_us:
        # Exclude environment sections
        exclude_envs.extend(['China', 'USGovernment'])
        # Also filter domain names containing .us or .cn (only if not using --endings)
        if not endings:
            filter_domains.extend(['.us', '.cn'])
        # Remove duplicates while preserving order
        exclude_envs = list(dict.fromkeys(exclude_envs))
        filter_domains = list(dict.fromkeys(filter_domains))
    
    # Check if file exists
    if not Path(args.input_file).exists():
        print(f"Error: Input file '{args.input_file}' not found")
        print(f"\nUsage: {sys.argv[0]} [input_file.json] [options]")
        parser.print_help()
        sys.exit(1)
    
    extract_dns_zones(
        args.input_file,
        private_output=args.private_output,
        public_output=args.public_output,
        exclude_envs=exclude_envs,
        filter_domains=filter_domains,
        endings=endings
    )
