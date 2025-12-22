
import dns.resolver

# Query A record
# answer = dns.resolver.resolve('openai.azure.com', 'A')
# for rdata in answer:
#     print(rdata.address)

# Query NS records
ns_answer = dns.resolver.resolve('openai.azure.com', 'NS')
for ns in ns_answer:
    print(ns.target)
