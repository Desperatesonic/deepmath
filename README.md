## Basic Dependencies
Most users can skip this section.  

Make sure your packages are up to date.
```bash
sudo apt-get update && sudo apt-get upgrade
```

### Python
First, you'll need to install Python 3.5 or higher, along with the development version. We used 3.6.

```bash
$ sudo apt-get install python3.6 python3.6-dev
```

### venv
You'll also need venv for managing virtual environments.
```bash
$ sudo apt-get install virtualenv
```

### gcc/g++
```bash
$ sudo apt-get install gcc g++
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

## Setting up your virtual environment
We strongly recommend running in a virtual environment. Should you choose not to, be sure to install [pip](https://pip.pypa.io/en/stable/). 

```bash
$ sudo apt-get install python3-venv
$ python3 -m venv /path/to/working/environment
```

Now navigate to your new environment and activate it
```bash
$ cd /path/to/working/environment
$ source bin/activate
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
$ bash bazel-0.21.0-installer-linux-x86_64.sh --prefix=$HOME/bazel
$ PATH=$HOME/bazel/bin:$PATH
```

### Install Dependencies

```bash
$ pip3 install h5py six numpy scipy wheel mock pyfarmhash grpcio
$ pip3 install keras_applications==1.0.6 keras_preprocessing==1.0.5 --no-deps
```

### Configure tensorflow
Navigate to the tensorflow dirctory and configure the following options.

```bash
$ cd deepmath/tensorflow
TF_IGNORE_MAX_BAZEL_VERSION=1   TF_NEED_OPENCL_SYCL=0   TF_NEED_COMPUTECPP=1   TF_NEED_ROCM=0   TF_NEED_CUDA=0   TF_ENABLE_XLA=0   TF_DOWNLOAD_CLANG=0   TF_NEED_MPI=0   TF_SET_ANDROID_WORKSPACE=0 CC_OPT_FLAGS="-march=native -Wno-sign-compare"  ./configure
```

Tensorflow will ask you to specify a python path. It will also give you a default option. Select the default and take note of the path it gives you.  
Now set the environment variable to that value.
```bash
$ export $PYTHON_BIN_PATH=<path given by tensorflow>
```

## Build tensorflow with Bazel

This step will take awhile. go fix yourself some snacks while it works.

```bash
$ cd ..
$ bazel build -c opt //deepmath/deephol:main --define grpc_no_ares=true --python_path=$PYTHON_BIN_PATH
```

## Run deephol
Now we can run deephol with 
```bash
$ python3 bazel-bin/deepmath/deephol/main
```
