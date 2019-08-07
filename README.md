# dq-packer-ops-win-bastion
This AMI is used as a NFS share box

## Features

### `packer.json`
This file contains a wrap up for Ansible script to be run inside a Windows 2012 R2 server

#### `scripts`
- `disable-esc-and-iac.ps1` turn off annoying Windows pop-ups
- `monitor_stopped_win_services.ps1` checks if there are any service in the *stopped* state where they are set to *automatic* startup
- `setupwrm.ps1` enable WRM service so packer can interact with the instance
- `sysprep-bundleconfig.ps1` turn on sysprep using a custom xml config file
- `sysprep-ec2config.ps1` add EC2 specific sysprep values

## Deploying / Publishing
Drone min ver 0.5 is needed to deploy with `.drone.yaml` file

## Contributing

If you'd like to contribute, please fork the repository and use a feature
branch. Pull requests are warmly welcome.

More information in [`CONTRIBUTING`](./CONTRIBUTING)

## Licensing
The code in this project is licensed under this [`LICENSE`](./LICENSE)
