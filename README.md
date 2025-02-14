
# LaunchiCube

A simple multi-instance launcher for ClassiCube, inspired by MultiMC, and made in Python

## Requirements

- Recomended Python Version: 3.12
- requests
- Pillow

## Features

🟩 = Done
🟨 = In Development
🟥 = Not In Development

- 🟨 Instances
	- 🟩 Multi-Instances
   	- 🟩 Adding Instances
	- 🟨 Custom Instance Icons
	- 🟥 Deleting Instances
	- 🟥 Editing Instances
	- 🟥 Plugin Manage
	- 🟥 Multiple Instances Running
  		- 🟥 Stop Button
  		- 🟥 Management of Multiple Instances
	- 🟥 Custom Clients
- 🟨 Misc
	- 🟨 Windows, Mac, Linux, and 32bit Support
   		- 🟩 Windows Downloads
  		- 🟨 Mac Downloads
   		- 🟨 Linux Downloads
   		- 🟨 32bit Downloads For All OSes
	- 🟥 Account Switcher
  		- 🟥 Windows Encryption
  		- 🟥 Unix Encryption (May not add as it will be Quite difficult. It's XTEA encryption with machine and OS specific key. OG code [here](https://github.com/ClassiCube/ClassiCube/blob/6d5a5b78c8b8e99d5bb4f557b8caafd9d5bb8a5b/src/Platform_Posix.c#L1382). It was deliberately designed so passwords could not be transferred between devices or easily accessed by other apps)
	- 🟥 Settings
	- 🟥 Themes

## Bugs

- Client can't use plugins, because "ClassiCube.exe is missing"
