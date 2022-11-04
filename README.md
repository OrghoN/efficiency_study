# Overview

A generator level simulation to create and plot data related to K0sK0s -> pi+pi-pi+pi- events resulting from double pomeron exchanges.

# Installation

## Prerequisites

- Linux Operating System
- git
- singularity

### Linux Operating System

Any linux operating system will work with this generation code.
Because it relies on a singularity container, it is not compatible with either windows or mac.
If you intend to use either windows or mac as the host system, a virtual machine with singularity preloaded can be found [here.](https://app.vagrantup.com/sylabs)
A guide on installing ubuntu if you want to use linux but don't have it can be found [here.](https://ubuntu.com/tutorials/install-ubuntu-desktop#1-overview)

### git
Git is required for this code.
It usually comes preinstalled with most linux systems.
A quick way to check if you have it is to
```bash
git --version
```

if git is installed, it should return a version number.

If git is not installed, you should be able to install it with the package manager for your operating system.

### Singularity

Singularity is required for this code because it is designed to run in a singularity container.
A detailed guide to installing singularity can be found [here.](https://docs.sylabs.io/guides/3.0/user-guide/installation.html)

#### Quick Install for Ubuntu >= 20.04

These commands will install singularity on Ubuntu systems >= 20.04.
However it is important to note that this is well behind the latest version of singularity and as such some of the newer features will not be available if you choose to install it this way.

This method requires wget. if it is not installed on your system, it can be obtained through

```bash
sudo apt update
sudo apt -y install wget
```

It is then time to enable the [neuro debian repository.](http://neuro.debian.net/pkgs/singularity-container.html)

```bash
wget -O- http://neuro.debian.net/lists/focal.us-tn.full | sudo tee /etc/apt/sources.list.d/neurodebian.sources.list
sudo apt-key adv --recv-keys --keyserver hkps://keyserver.ubuntu.com 0xA5D32F012649A5A9
sudo apt update
```

Once the repository has been added, singularity can be installed with

```bash
sudo apt install -y singularity-container
```

To test if singularity was successfully installed, you can run

```bash
singularity --version
```

If successfully installed, it will show you the version of singularity installed.

## Installation Instructions

Navigate to the directory from which you wish to run these scripts.
Once there, you can run

```bash
git clone git@github.com:OrghoN/efficiency_study.git
```

This will clone the repository.
Next step is to build the singularity container.

```bash
cd efficiency_study
sudo singularity build pythia.sif pythiaUbuntu.def
```

This step can take a little bitof time because it involves installing the appropriate versions of the prerequisite software for these scripts.

The container comes with the following software packages:

- python3
- wget
- pip
- rsync
- numpy
- matplotlib
- pythia

# Usage

In order to use the software, the first thing to do is to invoke a shell within the singularity container. This can be achieved with the following command

```bash
singularity shell pythia.sif
```

The generation script can be invoked with

```bash
python3 mymain04.py
```

The plotting script can be invoked with

```bash
python3 sim_hists.py
```

To change data generation parameters such as number of events to be generated without editing the python file, a user can make edits to mymain04.cmnd. See
the Pythia8 documentation on command files for more information.