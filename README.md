# Local development

1. Install docker: https://docs.docker.com/installation

2. Install fig:

        $ pip install fig

3. Build the docker containers:

        $ fig build

4. Start the docker containers:

        $ fig up


# Deploy

1. Install elastic beanstalk cli:

        $ pip install awsebcli

2. *First deploy only*: initialize elastic beanstalk:

        $ eb init
        $ eb create <app-name-with-env>

3. Deploy the web service:

        $ eb deploy <app-name-with-env>

4. Deploy the worker:

        $ KEY_NAME=<ec2-keypair-name> \
          TAG_NAME=<branch-name> \
          DOCKER_ENV='{"NAME": "Ford", "GREETING": "Hello"}' \
          ./deploy.py

5. After the new worker is up and running, terminate the old one.


# TODO

- Build an AMI with Docker already installed.
- Better way to set DOCKER_ENV.
- Some way to know immediately when new worker instance is ready.
- Automatically terminate old workers.
- Possibly, just clone the repo and build the docker image on the instance. This
  could be made pretty fast by having a base image built on the AMI.
