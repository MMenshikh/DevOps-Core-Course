import pulumi
from pulumi_yandex import ComputeInstance, VpcNetwork, VpcSubnet, VpcSecurityGroup
from pulumi_yandex import Provider

yc_provider = Provider("yc",
                       service_account_key_file="authorized_key.json",
                       cloud_id="b1gu4hpr6n728hvsq2uu",
                       folder_id="b1gp20cgg1ivu6s502bu",
                       zone="ru-central1-a"
                       )

network = VpcNetwork(
    "lab04-network", opts=pulumi.ResourceOptions(provider=yc_provider))

subnet = VpcSubnet("lab04-subnet",
                   network_id=network.id,
                   v4_cidr_blocks=["10.5.0.0/24"],
                   zone="ru-central1-a",
                   opts=pulumi.ResourceOptions(provider=yc_provider)
                   )

sg = VpcSecurityGroup("lab04-sg",
                      network_id=network.id,
                      ingresses=[  # <-- было ingress
                          {"protocol": "TCP", "description": "SSH",
                           "port": 22, "v4_cidr_blocks": ["0.0.0.0/0"]},
                          {"protocol": "TCP", "description": "App",
                           "port": 5000, "v4_cidr_blocks": ["0.0.0.0/0"]}
                      ],
                      egresses=[  # <-- было egress
                          {"protocol": "ANY", "description": "Allow all outbound",
                           "v4_cidr_blocks": ["0.0.0.0/0"]}
                      ],
                      opts=pulumi.ResourceOptions(provider=yc_provider)
                      )

vm = ComputeInstance("lab04-vm",
                     platform_id="standard-v1",
                     resources={"cores": 2, "memory": 2},
                     boot_disk={"initialize_params": {
                         "image_id": "fd87ce1b8tgh9b", "size": 20}},
                     network_interfaces=[{"subnet_id": subnet.id,
                                          "nat": True, "security_group_ids": [sg.id]}],
                     metadata={
                         "ssh-keys": "ubuntu:YOUR_SSH_PUBLIC_KEY_CONTENT"},
                     opts=pulumi.ResourceOptions(provider=yc_provider)
                     )
