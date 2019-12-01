## Basic Dependencies
Most users can skip this section.  

Make sure your packages are up to date.
```bash
sudo apt-get update && sudo apt-get upgrade
```

Instructions are given for Ubuntu Linux. The required dependencies are:  

- Python 3.5+, Python 3.5+-dev
- docker
- wget
- unzip
- gcc/g++

```bash
$ sudo apt-get install python3.6 python3.6-dev
```

**If using WSL(Windows Subsystem for Linux)**
You'll also need to install python 2. This is included by default in standalone Ubuntu, but not WSL.
```bash
sudo apt-get install python
```

---

# Using the Preconfigured Docker Images
This is the easiest and fastest way to get things up and running. We've provided a script to automate much of this process.

## Docker
Install docker with 
```bash
sudo apt-get remove docker docker-engine docker.io
sudo apt install docker.io
```

Now enable docker using  
```bash
sudo systemctl start docker
sudo systemctl enable docker
```

**WSL users** should follow [this guide](https://nickjanetakis.com/blog/setting-up-docker-for-windows-and-wsl-to-work-flawlessly#configure-docker-for-windows)


Now run the provided `buildScript` with  
```bash
bash buildScript
```

---

# Building from source
Follow this guide if you want to build on your local machine without using the container.

## Environment
We recommend using Anaconda to manage your environment.  

Create a conda environment:  
```bash
$ conda create --name deephol
$ conda activate deephol
```

Now install the following Python packages.  
*h5py, six,
numpy, scipy, wheel, mock, pyfarmhash, grpcio, grpcio-
tools, keras_applications, keras_preprocessing*

```sh
$ pip install h5py six numpy scipy wheel
mock pyfarmhash grpcio  
$ pip install keras_applications ==1.0.6
keras_preprocessing ==1.0.5 --no - deps
```

### Clone the necessary repositories
```bash
$ git clone https://github.com/tensorflow/deepmath.git
$ git clone https://github.com/brain-research/hol-light.git
```

### Update Submodules for tensorflow

```bash
$ cd deepmath 
$ git submodule update --init
```

### Bazel
Bazel is a build manager for tensorflow. We need to install this in order to build deepmath.

```bash
$ wget https://github.com/bazelbuild/bazel/releases/download/0.21.0/bazel-0.21.0-installer-linux-x86_64.sh
$ chmod 777 bazel-0.21.0-installer-linux-x86_64.sh
$ bash bazel-0.21.0-installer-linux-x86_64.sh --prefix=$HOME/bazel --user
$ PATH=$HOME/bazel/bin:$PATH
```

### Configure tensorflow
Navigate to the tensorflow dirctory and configure the following options, editing as necessary.

```bash
$ cd deepmath/tensorflow
TF_IGNORE_MAX_BAZEL_VERSION=1   TF_NEED_OPENCL_SYCL=0   TF_NEED_COMPUTECPP=1   TF_NEED_ROCM=0   TF_NEED_CUDA=0   TF_ENABLE_XLA=0   TF_DOWNLOAD_CLANG=0   TF_NEED_MPI=0   TF_SET_ANDROID_WORKSPACE=0 CC_OPT_FLAGS="-march=native -Wno-sign-compare"  ./configure
```

Now you need to set the PYTHON_BIN_PATH environment variable.
```bash
$ export $PYTHON_BIN_PATH=<$(which python)
```

## Build tensorflow with Bazel

This step will take awhile. go fix yourself some snacks while it works. Also, it will fail if you have less than 8GB of memory available, so maybe kill some of those chrome tabs?

```bash
$ cd ..
$ bazel build -c opt //deepmath/deephol:main --define grpc_no_ares=true --python_path=$PYTHON_BIN_PATH
```

## Running the HOL-Light container  
Set up a docker network, and run the provided container on that network. It will be helpful to save the ip address in an environment variable.

```sh
$ docker network create holist_net
$ docker run -d --network=holist_net --name=holist gcr.io/deepmath/hol-light
$ export HNET_IP="$(sudo docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' holist)"
```

To stop the container, run  

```sh
$ docker stop holist && docker rm holist && docker network rm holist_net
```

## Run deephol
Before running, you need to specify some configuration files. Some sample files are provided.  


```sh
$ wget https://storage.googleapis.com/deepmath/deephol.zip -O /tmp/deephol.zip
$ unzip /tmp/deephol.zip -d ./data
```

Now we can run deephol with 
```sh
$ python bazel-bin/deepmath/deephol/main --prover_options=data/configuration/prover_options.textpb --output=data/proof_logs.textpbs --proof_assistant_server_address=$HNET_IP:2000
```

# Check Your Proofs
You can expect some errors in the generated proofs, so you'll need to check them with HOL-Light.  

```sh
$ python bazel-bin/deepmath/deephol/utilities/proof_checker --theorem_database=/data/theorem_database_v1.1.textpb \ 
--proof_logs=data/proof_logs.textpbs \ 
--out_file=data/synthetic_proofs.ml

$ cp data/proof_logs.textpbs ../hol-light
$ cd ..
$ docker build -f hol-light/Dockerfile_check_proofs --ulimit stack=1000000000 --tag check_proofs hol-light/
$ docker run check_proofs
```

## Configuration
Configuration options can be found in \\ \lstinline{deepmath/data/configuration/prover_options.textpb}. \\ Available configuration options are determined by \\ \lstinline{deepmath/deephol/deephol.proto}. \\ Whenever changes are made to \lstinline{deephol.proto}, it must be compiled with: 

```sh
$ python -m grpc_tools.protoc -I. --python_out=bazel-genfiles/deepmath/deephol/ deepmath/deephol/deephol.proto
\end{lstlisting}{}
```
