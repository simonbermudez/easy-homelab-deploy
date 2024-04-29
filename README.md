# Easy Homelab Deploy tool

This system allows you to manage Cloudflare Tunnel configurations and DNS records easily using Terraform for infrastructure management and Python for interacting with Cloudflare's API. It also provides a Dockerized deployment setup for seamless deployment.

## Table of Contents

- [Features](#features)
- [Setup](#setup)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Terraform Configuration](#terraform-configuration)
  - [Python Utility](#python-utility)
  - [Docker Deployment](#docker-deployment)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Infrastructure as Code**: Uses Terraform to manage Cloudflare infrastructure resources such as tunnels and DNS records.
- **Python Utility**: Provides a Python utility to interact with Cloudflare's API for adding and deleting tunnel configurations.
- **Docker Deployment**: Offers a Dockerized deployment setup for easy deployment to any environment.

## Setup

### Prerequisites

Before getting started, ensure you have the following:

- Cloudflare API token with appropriate permissions.
- Cloudflare Account ID and Tunnel ID.
- `.env` file with Cloudflare credentials.

### Installation

1. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/simonbermudez/easy-homelab-deploy.git
    ```

2. Navigate to the project directory:

    ```bash
    cd easy-homelab-deploy
    ```

## Usage

### Terraform Configuration

1. Modify the `data` and `resource` blocks in `resources.tf` according to your tunnel configurations.

2. Set the Cloudflare API token, Account ID, and other variables in `.env` file.

3. Run Terraform commands to apply the configuration:

    ```bash
    terraform init
    terraform apply
    ```

### Python Utility

1. Ensure your `.env` file is properly configured with Cloudflare credentials.

2. Use the Python utility to manage tunnel configurations:
    This class is responsible for managing Cloudflare Tunnel configurations and DNS records.
    example usage: 
    ```
    manager = CloudflareTunnelManager()
    example_tunnel = {'hostname': 'subdomain.domain_managed_by_cloudflare.com',
                    'service': 'http://ip_or_hostname_running_your_app:port'
    }
    manager.add_tunnel_configuration(example_tunnel)
    manager.delete_tunnel_configuration('subdomain.domain_managed_by_cloudflare.com')
    ```

### Docker Deployment

This image is meant to be ran as a github action, but this is still a WIP.

1. Build the Docker image:

    ```bash
        docker compose up .
    ```

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
