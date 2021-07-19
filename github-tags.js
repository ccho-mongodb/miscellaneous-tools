const { graphql } = require("@octokit/graphql");
require('dotenv').config();

const versionFilter = /[-.]*(beta|alpha|rc|b[0-9]+)[0-9]*/i;

const graphqlWithAuth = graphql.defaults({
  headers: {
    authorization: `token ${process.env.GITHUB_ACCESS_TOKEN}`,
  },
});

const driverRepos = [
  { name: "mongo-c-driver", owner: "mongodb", desc: "C Driver" },
  { name: "mongo-cxx-driver", owner: "mongodb", desc: "C++ Driver" },
  { name: "mongo-csharp-driver", owner: "mongodb", desc: "C# Driver" },
  { name: "mongo-go-driver", owner: "mongodb", desc: "Go Driver" },
  { name: "mongo-java-driver", owner: "mongodb", desc: "Java Sync, Java Async, and Scala Driver" },
  { name: "node-mongodb-native", owner: "mongodb", desc: "Node.js Driver" },
  { name: "mongo-php-library", owner: "mongodb", desc: "PHP Driver Library and Extensions" },
  { name: "mongo-python-driver", owner: "mongodb", desc: "PyMongo Driver" },
  { name: "motor", owner: "mongodb", desc: "Motor Driver" },
  { name: "mongo-ruby-driver", owner: "mongodb", desc: "Ruby Driver" },
  { name: "mongoid", owner: "mongodb", desc: "Mongoid ODM" },
  { name: "mongo-rust-driver", owner: "mongodb", desc: "Rust Driver" },
  { name: "mongo-rust-driver", owner: "mongodb", desc: "Rust Driver" },
];

driverRepos.forEach(repo => {

  graphqlWithAuth(`
    query fileCommits($name: String!, $owner: String!) {
      repository( name: $name, owner: $owner ) {
      refs(last: 5, refPrefix: "refs/tags/") {
        nodes {
          id
          name
          target {
            ... on Tag{
              id
              message
              tagger {
                  name
                  email
                  date
              }
            }
          }
        }
      }
        }
      }
    `,
    {
      name: repo.name,
      owner: repo.owner
    }
  ).then(function(response) {
    console.log(`${repo.name}:`);
    var nodes = response.repository.refs.nodes;
    if (! nodes || nodes.length === 0) {
      console.log("No versions found");
    } else {
      nodes.forEach(x => {
        if (x && x.target && x.target.tagger && x.target.tagger.date) {
          if (! x.name.match(versionFilter)) {
            console.log(x.name + ": " + x.target.tagger.date);
          }
        }
      }
      );
    }
    console.log();
  })
}
);

