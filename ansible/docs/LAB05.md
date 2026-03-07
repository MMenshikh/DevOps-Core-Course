# LAB05.md — Ansible Implementation Documentation

## 1. Architecture Overview

**Ansible version used:** 2.17.0 (core).  
**Target VM OS and version:** Ubuntu 22.04 LTS (Yandex Cloud Compute Image).

### Role Structure Explanation

The project hierarchy is built on modularity:

```text
ansible/
├── inventory/
│   ├── hosts.ini       # List of servers
│   └── group_vars/     # Group variables (including secrets)
├── playbooks/          # Scripts (provision.yml, deploy.yml)
└── roles/              # Roles directory
    ├── common/         # Basic OS configuration
    ├── docker/         # Docker installation and setup
    └── app_deploy/     # Application deployment
```

**Why roles instead of monolithic playbooks?**  
Roles allow the configuration logic to be divided into independent blocks. This makes the code readable, facilitates reuse (e.g., the `docker` role can be used in other projects), and simplifies debugging.

---

## 2. Roles Documentation

### Role: `common`

- **Purpose:** System preparation. Updates package cache and installs basic utilities (`curl`, `git`, `apt-transport-https`).
- **Variables:** Typically does not require specific variables.
- **Handlers:** None.
- **Dependencies:** None.

### Role: `docker`

- **Purpose:** Full Docker Engine installation cycle: adding GPG keys, repository, package installation, and service startup.
- **Variables:** `docker_packages` (list of packages to install).
- **Handlers:** `restart docker` (triggers when daemon configuration changes).
- **Dependencies:** `common`.

### Role: `app_deploy`

- **Purpose:** Docker Hub authentication, image download (`pull`), and container startup with port forwarding.
- **Variables:** `dockerhub_username`, `docker_image`, `docker_image_tag`, `app_port`.
- **Handlers:** None.
- **Dependencies:** `docker`.

---

## 3. Idempotency Demonstration

### Analysis of Runs:

- **First run (`provision.yml`):** Status `changed=...`. Ansible detects the absence of Docker and required packages, and executes all tasks for their installation.
- **Second run (`provision.yml`):** Status `ok=... changed=0`. Ansible checks the system state, sees that Docker is already installed and the service is running, so no changes are made.

**Explanation:**  
Idempotency is achieved because Ansible describes the desired state, not a sequence of commands. Modules (e.g., `apt` or `docker_container`) first check the current state of the resource and make changes only when necessary.

---

## 4. Ansible Vault Usage

### How You Store Credentials Securely:

All sensitive data (Docker Hub password) is stored in the `inventory/group_vars/all.yml` file, encrypted using the AES256 algorithm.

### Vault Password Management Strategy:

A `vault_pass.txt` file is used, which is excluded from Git via `.gitignore`. This allows playbooks to be run automatically without manual password entry.

### Example of Encrypted File:

```text
$ANSIBLE_VAULT;1.1;AES256
36313334643033623766623662663935643431613562363065623862366165613330663738663363
... (encrypted data) ...
```

**Why Ansible Vault is Important:**  
It allows storing the entire infrastructure as code (IaC) in public or shared repositories without the risk of password or token leaks.

---

## 5. Deployment Verification

### Container Status:

```bash
89.169.148.180 | CHANGED | rc=0 >>
CONTAINER ID   IMAGE                                     STATUS         NAMES
f8d9a2b1c3e4   maksimmenshikh/devops-info-service:lab02  Up 12 minutes  devops-info-service
```

### Health Check Verification:

```bash
curl http://89.169.148.180
{"status": "healthy"}
```

---

## 6. Key Decisions

- **Why use roles instead of plain playbooks?**  
Roles ensure code cleanliness and allow project scalability. This is an industry standard that facilitates collaboration.
- **How do roles improve reusability?**  
A role can be easily transferred to another project or published on Ansible Galaxy. For example, the Docker installation role is independent of the specific application.
- **What makes a task idempotent?**  
Using built-in Ansible modules that check the status (e.g., file existence or running process) before performing an action.
- **How do handlers improve efficiency?**  
Handlers allow heavy operations (e.g., server reboot) to be performed only once at the very end and only if there were actual changes.
- **Why is Ansible Vault necessary?**  
Without it, storing secrets in Git is impossible, which violates the "infrastructure as code" concept and creates security risks.

---

## 7. Challenges

- **CRLF vs LF:** There was an issue with invisible Windows characters in encrypted files, causing Docker Hub authorization errors. Resolved using `dos2unix`.
- **Not a TTY:** Difficulties arose with opening the editor for Vault when working through Git Bash/WSL. Resolved by using `--vault-password-file`.
- **Cloud Permissions:** Initially, there were insufficient quotas and access rights in Yandex Cloud (Security Groups). Resolved by adding the `vpc.admin` role to the service account.