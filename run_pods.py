from time import sleep
from kubernetes import client, config
import numpy as np

# Add a list of directories to copy
DIRECTORIES = []
SOURCE_REGISTRY = ""
DEST_REGISTRY = ""
# Create the image with the Dockerfile
IMAGE = ""
NAMESPACE = "default"


def create_job(directory, IMAGE, SOURCE_REGISTRY, DEST_REGISTRY):
    """
    Create Kubernetes Jobs
    """
    args = [
        "-c",
        f"/usr/local/bin/gcrane cp -r {SOURCE_REGISTRY + directory} {DEST_REGISTRY + directory}",
    ]
    name = directory.replace("_", "-")
    # Configure Pod template container
    container = client.V1Container(
        name=f"{name}-gcrane-container",
        image=IMAGE,
        image_pull_policy="Always",
        command=["/bin/bash"],
        args=args,
    )

    # Create and configure a spec section
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(
            labels={
                "migration": "true",
            },
        ),
        spec=client.V1PodSpec(
            restart_policy="Never",
            service_account="jenkins-workload-id-sa",
            containers=[container],
        ),
    )

    # Create the specification of deployment
    spec = client.V1JobSpec(template=template, backoff_limit=4)

    # Create the job object
    return client.V1Job(
        api_version="batch/v1",
        kind="Job",
        metadata=client.V1ObjectMeta(name=name),
        spec=spec,
    )


def main():
    """
    The main program
    """
    config.load_kube_config()
    v1client = client.BatchV1Api()

    # we will run three jobs at once
    split_list_length = len(DIRECTORIES) / 3
    sub_lists = np.array_split(DIRECTORIES, split_list_length)
    count = 1
    for i in sub_lists:
        print("run number ", count, ": ", list(i))
        for directory in i:
            job = create_job(directory, IMAGE, SOURCE_REGISTRY, DEST_REGISTRY)
            v1client.create_namespaced_job(
                body=job,
                namespace=NAMESPACE,
            )
            while (
                len(
                    [
                        job
                        for job in client.BatchV1Api()
                        .list_namespaced_job(namespace=NAMESPACE)
                        .items
                        if job.status.active == 1
                    ]
                )
                >= split_list_length
            ):
                sleep(5)
        count += 1


if __name__ == "__main__":
    main()
