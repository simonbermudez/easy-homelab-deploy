terraform {
  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 4.0"
    }
  }
}

variable "CLOUDFLARE_VM_SSH_ENDPOINT" {
  type = string
}

variable "CLOUDFLARE_ACCOUNT_ID" {
  type = string
}

variable "CLOUDFLARE_TUNNEL_ID" {
  type = string
}

variable "CLOUDFLARE_API_TOKEN" {
  type = string
}

variable "CLOUDFLARE_DNS_NAME" {
  type = string
}

variable "csv_path" {
  default = "../data/tunnels/.csv"
}

provider "cloudflare" {
  api_token = var.CLOUDFLARE_API_TOKEN
}

