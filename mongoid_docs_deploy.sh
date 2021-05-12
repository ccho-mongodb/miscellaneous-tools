#!/bin/sh

# version branch names in descending order
VERSIONS=(master 7.3 7.2 7.1 7.0 6.4 6.3 6.2 6.1 5.4)

# clean
git checkout master
make clean

# build each version in order
for i in "${VERSIONS[@]}"; do
  echo "Branch [$i]: Generating HTML and local directories"
  git checkout $i && git pull && make html publish
done

# Prompt in case errors encountered
read -p "Proceed with deploy? " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
  [[ "$0" = "$BASH_SOURCE" ]] && exit 1 || return 1
fi

# deploy
for i in "${VERSIONS[@]}"; do
  echo "Deploying [$i]"
  git checkout $i && yes | make deploy
done

echo "Deployment complete!"
