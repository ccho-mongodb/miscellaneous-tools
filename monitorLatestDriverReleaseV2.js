exports = async function (arg) {
    const token = context.values.get("GAT");

    let releaseRepos = [
        "mongodb/mongo-python-driver",
        "mongodb/motor",
        "mongodb/mongo-php-library",
        "mongodb/mongo-java-driver",
        "mongodb/node-mongodb-native",
        "mongodb/mongo-ruby-driver",
        "mongodb/mongoid",
        "mongodb/mongo-rust-driver",
        "mongodb/mongo-csharp-driver",
        "mongodb/mongo-c-driver",
        "mongodb/mongo-cxx-driver",
        "mongodb/mongo-go-driver",
        "mongodb/mongo-swift-driver",
        "mongodb/mongo-kafka",
        "mongodb/mongo-csharp-analyzer"
    ];

    // TODO: track these using the GitHub "/tags" endpoint
    let tagOnlyRepos = [
      "mongodb/mongo-spark",
      "mongodb/mongo-efcore-provider"
    ];

    // Use Maps for convenient comparison
    let gh_map = await Promise.all(releaseRepos.map(async repo => { return getReleaseTags(repo, token) })).then(convert_to_map);
    let db_map = await getExistingTags().then(convert_to_map);

    await compareTags(db_map, gh_map)
      .then(updateTags)
      .then(createTickets);

};


async function convert_to_map(release_data) {
  const r = new Map();
  for (let i=0; i<release_data.length; i++) {
    r.set(release_data[i].repo, release_data[i].tags); 
  }
  return r;
}

async function getReleaseTags(repoPath, token) {
    let releaseTagUrl = `https://api.github.com/repos/${repoPath}/releases`;
    return context.http.get({
      url: releaseTagUrl,
      headers: {
        Authorization: [`token ${token}`],
      },
    })
    .then(response => JSON.parse(response.body.text()))
    .then((data) => {
        const tag_names = data.flatMap(release => 
            (!release.draft && !release.prerelease) ? release.tag_name:[]);
        return {repo: repoPath, tags: tag_names};
    })
}

async function getExistingTags() {
    const cluster = context.services.get('mongodb-atlas');
    const versions = cluster.db("releases").collection("versions");

    let existing_data = [];
    try {
      const cursor = await versions.find();

      for await (const doc of cursor) {
        existing_data.push(doc);
      }

    } catch (err) {
      console.error(err);
      return err;
    }
    return existing_data;
}

// returns a Map of the GitHub tags not found in the db data
async function compareTags(db_tags, gh_tags) {
  const diffs = new Map();
  
  gh_tags.forEach((val, key, map) => {
      const db_versions = db_tags.get(key);
      const diff = val.filter(version => db_versions.indexOf(version) < 0);
      if (diff.length > 0) {
        diffs.set(key, diff)
      }
    }
  )
  return diffs;
}

async function updateTags(diff_map) {
    const cluster = context.services.get('mongodb-atlas');
    const versions = cluster.db("releases").collection("versions");

    update_docs = [];

    for (const [key, val] of diff_map) {
        update_docs.push(
            {
                updateOne: {
                    filter: { repo: key },
                    update: { $addToSet: { tags: { $each:  val } } },
                    upsert: true,
            }
        });
    }

    if (update_docs.length > 0) {
      await versions.bulkWrite(update_docs);
    }

    // return for chaining
    return diff_map;
}

// Create one JIRA ticket per driver
async function createTickets(releases) {
  releases.forEach((versions, repo, entry) => {
    context.functions.execute('createJiraTicket', {
      fields: {
        project: { id: "14181" }, // Project: DOCSP
        issuetype: { id: "3" }, // Type: Task
        priority: { id: "3" }, // Priority: P3 - Major
        labels: [
          "driver-version-update",
          "feature"
        ],
        components: [
          { id: "18334" }, // Drivers
        ],
        // Feedback Info
        summary: `Driver and Connector Version Updates`,
        description: `
          Driver: ${repo}
              Release versions added: ${versions}

              cc [~rachelle.palmer@mongodb.com]`
            }
        })
  });
}
