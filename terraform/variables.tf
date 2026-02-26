variable "cloud_id" {}
variable "folder_id" {}

variable "zone" {
  default = "ru-central1-a"
}

variable "vm_name" {
  default = "lab04-vm"
}

variable "platform_id" {
  default = "standard-v1"
}

variable "cores" {
  default = 2
}

variable "memory" {
  default = 2
}

variable "image_id" {
  description = "Ubuntu 22.04 LTS image ID"
  type        = string
  default     = "fd817i7o8012578061ra"
}

variable "ssh_public_key_path" {
  default = "~/.ssh/id_rsa.pub"
}