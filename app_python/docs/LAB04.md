
# LAB04 — Yandex Cloud Infrastructure with Pulumi

## Goal
Create a simple infrastructure in Yandex Cloud using Pulumi (Python), including:

- VPC network
- Subnet
- Security Group
- Virtual Machine with SSH access and application port

## Prerequisites

1. Yandex Cloud account.
2. Installed Pulumi and Python 3.10+.
3. Yandex Cloud CLI (`yc`).
4. Python virtual environment for the project:

```bash
python -m venv venv
source venv/Scripts/activate
pip install --upgrade pip setuptools wheel
```

## 1. Service Account Setup

1. Create a service account:

```bash
yc iam service-account create --name lab04-sa
```

2. Create a service account key:

```bash
yc iam key create --service-account-name lab04-sa --output authorized_key.json
```

3. Ensure the key contains `private_key` and `public_key`.

4. Assign folder access to the service account via web console: **Folder → Access Management → Add binding → Role: Editor + Security Admin → Subject: lab04-sa**.

## 2. Pulumi Project Setup

1. Initialize the project:

```bash
pulumi new python
```

- Name: `lab04`
- Stack: `dev`

2. Install Yandex Pulumi provider:

```bash
pip install pulumi_yandex
```

## 3. Project Structure

```
pulumi/
├─ __main__.py
├─ venv/
├─ Pulumi.yaml
└─ Pulumi.dev.yaml
```

## 4. Example `__main__.py`

```python
import pulumi
from pulumi_yandex import Provider
from pulumi_yandex.vpc import Network, SecurityGroup, Subnet
from pulumi_yandex.compute import Instance, boot_disk, resources

yc_provider = Provider("yc",
    service_account_key_file="authorized_key.json",
    cloud_id="your_cloud_id",
    folder_id="b1gp20cgg1ivu6s502bu",
    zone="ru-central1-a"
)

network = Network("lab04-network",
    name="lab04-network",
    opts=pulumi.ResourceOptions(provider=yc_provider)
)

sg = SecurityGroup("lab04-sg",
    network_id=network.id,
    ingress=[{
        "protocol": "TCP",
        "port": 22,
        "v4_cidr_blocks": ["0.0.0.0/0"]
    }, {
        "protocol": "TCP",
        "port": 5000,
        "v4_cidr_blocks": ["0.0.0.0/0"]
    }],
    egress=[{
        "protocol": "ANY",
        "v4_cidr_blocks": ["0.0.0.0/0"]
    }],
    opts=pulumi.ResourceOptions(provider=yc_provider)
)

subnet = Subnet("lab04-subnet",
    network_id=network.id,
    v4_cidr_blocks=["10.5.0.0/24"],
    zone="ru-central1-a",
    opts=pulumi.ResourceOptions(provider=yc_provider)
)

vm = Instance("lab04-vm",
    resources=resources.ResourcesArgs(
        cores=2,
        memory=2
    ),
    boot_disk=boot_disk.BootDiskArgs(
        initialize_params=boot_disk.InitializeParamsArgs(
            image_id="fd8t1v7d1qsb9j3c2g4i",
            size=20
        )
    ),
    network_interfaces=[{
        "subnet_id": subnet.id,
        "nat": True,
        "security_group_ids": [sg.id]
    }],
    metadata={
        "ssh-keys": "ubuntu:" + open("id_rsa.pub").read()
    },
    opts=pulumi.ResourceOptions(provider=yc_provider)
)

pulumi.export("vm_ip", vm.network_interfaces[0].primary_v4_address)
```

## 5. Generate SSH Keys

```bash
ssh-keygen -t rsa -b 2048 -f id_rsa
```

- `id_rsa` — private key
- `id_rsa.pub` — public key used in Pulumi

## 6. Deploy Infrastructure

```bash
source venv/Scripts/activate
winpty pulumi up
```

Confirm with `yes`.

## 7. Verify

```bash
ssh -i id_rsa ubuntu@<vm_ip>
```

Check that port 5000 is accessible.

## 8. Cleanup

```bash
pulumi destroy
pulumi stack rm dev
```

## 9. Summary

- Created VPC network, subnet, security group, and VM.
- Configured service account roles: editor + security-admin.
- Managed infrastructure with Pulumi (Python).
