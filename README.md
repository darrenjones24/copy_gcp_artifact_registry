# copy_gcp_artifact_registry
Create k8s jobs to copy list of directories in a GCP artifact registry in parallel 


Build out the Dockerfile and upload to a registry
Add lists of directories to copy, and the source/dest of the artifact registries

Be sure to setup kubectl for the cluster we intend to run this on. 