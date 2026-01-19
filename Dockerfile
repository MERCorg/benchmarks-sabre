FROM ubuntu:24.04

# Install dependencies
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
# Dependencies for mCRL2
 build-essential \
 cmake \
 git \
 libboost-dev \
 z3 \
 # Required to install Rust
 curl \
 # Requires for the Python scripts
 python3 \
 python3.12-venv
 
# Build the mcrl22lps and lps2lts tools of mCRL2 from source
COPY ./mCRL2 /root/mCRL2/

# Configure build
RUN mkdir ~/mCRL2/build && cd ~/mCRL2/build && cmake . \
 -DCMAKE_BUILD_TYPE=RELEASE \
 -DMCRL2_ENABLE_DEVELOPER=ON \
 -DMCRL2_ENABLE_GUI_TOOLS=OFF \
 ~/mCRL2

ARG THREADS=8
RUN cd ~/mCRL2/build && make -j${THREADS} mcrl2rewrite

# Install Rust for building merc
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# Build merc-rewrite from source
COPY ./merc /root/merc/

ARG THREADS=8
ENV PATH="/root/.cargo/bin:${PATH}"
RUN cd ~/merc/ \
    && cargo build --release -j${THREADS} --bin merc-rewrite
    
# Install merc-py module, and create a virtual environment
COPY merc-py /root/merc-py/

RUN python3 -m venv /root/.venv && /root/.venv/bin/pip install /root/merc-py

# Copy the scripts to ensure that these are fixed.
COPY scripts /root/scripts/

