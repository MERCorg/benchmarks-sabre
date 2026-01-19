# Overview

These are various example rewrite systems from the Rewrite Engine Competition
[1]. Note that the REC specifications with META blocks have been omitted since
it is unclear how to expand them. The resulting mCRL2 specifications are used
for comparison studies between mCRL2 and the Sabre rewriter implemented in Rust.
The benchmark results are shown below. Timeouts of 10 minutes (600 seconds) are indicated by '-'.

>  [1] Durán, F., Garavel, H. (2019). The Rewrite Engines Competitions: A RECtrospective. In: Beyer, D., Huisman, M., Kordon, F., Steffen, B. (eds) Tools and Algorithms for the Construction and Analysis of Systems. Lecture Notes in Computer Science, vol. 11429. Springer, Cham. [DOI](https://doi.org/10.1007/978-3-030-17502-3_6)

## Running

Running the benchmarks requires initializing the git submodules:

```bash
git submodule update --init
```

The benchmarks can be run inside a [Docker](https://www.docker.com/) container. First, build the Docker image:

```bash
docker build . -t sabre_artifact
```

Then, run the container, mounting a local `results` directory to store the results:

```bash
docker run -it --rm --mount type=bind,source=./results,target=/root/results --mount type=bind,source=./merc/examples/REC,target=/root/REC sabre_artifact
```

```bash
/root/.venv/bin/python3 /root/scripts/run_mcrl2.py /root/mCRL2/build/stage/bin/ jitty /root/REC/mcrl2/ /root/results/
/root/.venv/bin/python3 /root/scripts/run_mcrl2.py /root/mCRL2/build/stage/bin/ jittyc /root/REC/mcrl2/ /root/results/
/root/.venv/bin/python3 /root/scripts/run_merc.py /root/merc/target/release/ innermost /root/REC/rec/ /root/results/
/root/.venv/bin/python3 /root/scripts/run_merc.py /root/merc/target/release/ sabre /root/REC/rec/ /root/results/
```

## Results

The C++ code was compiled with GCC 13.3.0 and the Rust code with rustc 1.92.0.
Benchmarks were performed on an i7-12800H running Linux in WSL. The results can
be found in the `results` directory.
