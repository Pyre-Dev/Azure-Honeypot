# Terraform-Deployed Azure Cowrie Honeypot

This project automatically deploys a Cowrie SSH honeypot on Azure using Terraform + cloud-init.

##  Stack
- Azure Resource Group, VM, NSG
- Cowrie Honeypot (simulated SSH service)
- Auto-installed via cloud-init

## Deploy

```bash
terraform init
terraform apply

## Parsing logs in this host is done by SSH-ing into the honeypot VM and copying the log file

SSH
scp azureuser@<vm-ip>:/opt/cowrie/var/log/cowrie/cowrie.json

python parse_logs.py

Enter the file name when prompted (e.g., cowrie.json)