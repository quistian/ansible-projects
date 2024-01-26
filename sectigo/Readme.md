# EIS NetDev Sectigo Documentation

## URLs of interest:

### UofT Information Security:

https://isea.utoronto.ca/services/pki-certificates/acme-implementation/

- To create a new Sectigo account:

```
curl 'https://cert-manager.com/api/acme/v2/account' -i -X POST \
  -H 'Content-Type: application/json' \
  -H 'login: account' \
  -H 'password: password!' \
  -H 'customerUri: uot' \
  -d '{"acmeServer":"https://acme.sectigo.com/v2/OV","name":"apitest","organizationId":6339}'
```

- To find the Account ID of the new ACME account:

```
curl 'https://cert-manager.com/api/acme/v2/account?position=0&size=10&organizationId=6339&name=apitest&acmeServer=https://acme.sectigo.com/v2/OV&status=Pending' -i -X GET \
  -H 'login: account' \
  -H 'password: password' \
  -H 'customerUri: uoft'
```

- To add new domains to the created ACME Sectigo account:

```
curl 'https://cert-manager.com/api/acme/v2/account/24282/domain' -i -X POST \
  -H 'Content-Type: application/json' \
  -H 'login: account' \
  -H 'password: password' \
  -H 'customerUri: uot' \
  -d '{"domains":[{"name":"si.utoronto.ca"}]}'
```

### From the Sectigo Certificate Manger web site:

https://cert-manager.com/customer/uot?locale=en#acme

Dashboard ---> Enrollment ---> ACME

Clicking on our URL: https://acme.sectigo.com/v2/OV

ACME --> Accounts

From there click on the eis-net-dev Account name already created

This will show 5 new boxes and icons::

Trash   Edit   Details   Clients View Audit

Details shows the follow account info and credentials:

ACME Account Details
Contacts russell.sutherland@utoronto.ca
ACME URL https://acme.sectigo.com/v2/OV

AccountID: 0ICUzWHZHb9VwZQ_h6gc6A
KeyID: 0ICUzWHZHb9VwZQ_h6gc6A

HMAC Key: JE4mJ2g3cFV1U2hR3e4Vj_NR-azzJ6CW27bIm7NySeVj9S1uGKARN3VvG44pGZkuhB-THofRe5bVMyQSLCwjiQ


These EAB credentials can be used now directly with certbot:

$ certbot certonly \
--standalone \
--non-interactive \
--agree-tos \
--email mailboxa@domain.com \
--server https://acme.sectigo.com/v2/OV \
--eab-kid 0ICUzWHZHb9VwZQ_h6gc6A \
--eab-hmac-key JE4mJ2g3cFV1U2hR3e4Vj_NR-azzJ6CW27bIm7NySeVj9S1uGKARN3VvG44pGZkuhB-THofRe5bVMyQSLCwjiQ \
--domain certdomain.com \
--cert-name DVcert

-----

SThis is a sample Ansible playbook to demonstrate connection to Digicert ACME URLs in CertCentral to issue certificates. This includes creating an ACME account using External Account Binding, generating a CSR and private Key, and delivering the certificate using ACMEv2 protocol to the 'data' directory. 

It uses the following two acme modules from the community.crypto collection:
   1. acme_certificate module to issue a certificate. 
   (https://docs.ansible.com/ansible/latest/collections/community/crypto/acme_certificate_module.html#ansible-collections-community-crypto-acme-certificate-module)
   2. acme_account module to create an account using external account binding. 
   (https://docs.ansible.com/ansible/latest/collections/community/crypto/acme_account_module.html#ansible-collections-community-crypto-acme-account-module)


Below are the steps to configure and get a certificate using this playbook:

1. Create an ACME Directory URL in your Digicert CertCentral account under Automation > ACME Directory URLs to get External Account Binding (EAB). This step is optional if you already have your EAB credentials.

2. Open digicert_acme_cert_main.yml and update the below fields under vars to specify the certificate parameters.  

    cert_cn: <Certificate common_name>
    contact_email: <email_id_of_admin>
    eab_kid: <External account binding KID value copied from ACME Directory URL during creation>
    eab_key: <External account binding HMAC key copied from ACME directory URL during  creation>

(Optional) You can update the other default settings as below:
    1. data_dir "data" is created in the same directory where the playbook file digicert_acme_cert_main.yml exists. you can change it to any desired path. It will contain all generated keys and certificates as described above.
    2. Certificate SAN field value is currently coded as subject_alt_name: "DNS: www.{{ cert_cn }},DNS:{{ cert_cn }}". For example, if cert_cn value is example.com then this playbook request certificate with SANs www.example.com,example.com. this can be changed per your needs.

3. Run the Ansible playbook. Make sure you have digicert_acme_cert_main.yml and get-cert.yml in the same directory.

   As a root user: ansible-playbook digicert_acme_cert_main.yml

         OR

   As a non-root user: ansible-playbook --become-user <BECOME_USER> digicert_acme_cert_main.yml


After successful execution you will see the following in the 'data' directory:

data/
   accountkey.pem
   {{cert_cn}}.csr
   {{cert_cn}}.key
   {{cert_cn}}.pem
   {{cert_cn}}-chain.pem
   {{cert_cn}}-fullchain.pem



