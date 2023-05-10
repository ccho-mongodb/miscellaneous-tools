Docker Image for Hugo v0.25.x Legacy JVM Driver Documentation Builds
--------------------------------------------------------------------

1. To build the Docker image, run the following command:

```sh
docker build -t ccho-mongodb/hugo-legacy-build .
```

2. To start an interactive shell in the Docker container built from the image, run the following command:

```sh
docker run -ti ccho-mongodb/hugo-legacy-build /bin/bash
```

