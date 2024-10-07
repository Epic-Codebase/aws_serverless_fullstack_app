# was_tasks

## Infrastructure

The easiest way to manage servers, subnets, load balancers, managed databases, etc. is by using infrastructure-as-code (IaC). Inside the "infrastructure" folder we'll store configuration files for our tool(s) of choice. These are usually long YAML, JSON, or HCL files.

## Services

Anything that is long-running or talks to our end users is considered a service. It can be monolithic Django application, Vue UI, or a couple of microservice APIs -- all will reside in this folder.