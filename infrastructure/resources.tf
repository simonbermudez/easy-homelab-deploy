locals {
  tunnels_csv = csvdecode(file(var.csv_path))
  tunnels     = { for idx, row in local.tunnels_csv : idx => row }
  domains     = distinct([for row in local.tunnels : row.domain])
}

data "cloudflare_zone" "zones" {
  for_each = { for domain in local.domains : domain => domain }
  name     = each.value
}

locals {
  tunnel_zones = {
    for idx, row in local.tunnels_csv :
    idx => merge(row, { zone_id = data.cloudflare_zone.zones[row.domain].zone_id,
    hostname = join("", concat((length(row.subdomain) > 0 ? [row.subdomain, "."] : []), [row.domain])) })
  }
}

output "tunnel_zones" {
    value = local.tunnel_zones
}

data "cloudflare_tunnel" "homelab" {
  account_id = var.CLOUDFLARE_ACCOUNT_ID
  name       = "Homelab"
}


resource "cloudflare_record" "cname_record" {
  for_each = local.tunnel_zones
  zone_id  = each.value.zone_id                                 # Specify the ID of your Cloudflare DNS zone
  name     = length(each.value.subdomain) == 0 ? "@" : each.value.subdomain                                # Specify the domain name where you want to create the CNAME record
  type     = "CNAME"                                            # Specify the record type as CNAME
  value    = "${data.cloudflare_tunnel.homelab.id}.cfargotunnel.com" # Specify the target domain name to which the CNAME should point
    allow_overwrite = true
    proxied         = true
}




resource "cloudflare_tunnel_config" "homelab_tunnels" {
  account_id = var.CLOUDFLARE_ACCOUNT_ID
  tunnel_id  = var.CLOUDFLARE_TUNNEL_ID

  config {
    warp_routing {
      enabled = true
    }
    dynamic "ingress_rule" {
      for_each = local.tunnel_zones # Wrap each row in a list to iterate over it

      content {
        hostname = ingress_rule.value.hostname
        service  = ingress_rule.value.service
        
        origin_request {
            no_tls_verify = strcontains(ingress_rule.value.options, "ssl") ? true : false
        }
        # Add more configuration settings here as needed
      }
    }

    # The last ingress rule to match all URLs
    ingress_rule {
      service = "http_status:404"
    }
  }
}

output "cloudflare_tunnel_config" {
  value = cloudflare_tunnel_config.homelab_tunnels
}