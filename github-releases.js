const { graphql } = require("@octokit/graphql");
require('dotenv').config();

class DriverRelease {
  constructor(driverName, title, createdAt) {
    this.driverName = driverName;
    this.title = title;
    this.createdAt = new Date(createdAt);
  }

  static compareFn() {
    return function (a,b) { return b.createdAt - a.createdAt }
  }

  toString() {
    const dt = this.createdAt;
    var dtString = `${dt.getMonth() + 1}/${dt.getDate()}/${dt.getFullYear()}`;
    return `[${this.driverName}] ${this.title} (${dtString}\n`;
  }
}

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

const repoData = (async(repo) =>
  graphqlWithAuth(`
    query fileCommits($name: String!, $owner: String!) {
      repository( name: $name, owner: $owner ) {
        releases(last: 5) {
          nodes {
            name
            createdAt
            url
          }
        }
      }
    }`,
    {
      name: repo.name,
      owner: repo.owner
    }));

async function run() {
  var releaseInfo = new Array();

  for (let i=0; i<driverRepos.length; i++) {
    data = await repoData(driverRepos[i]);

    var nodes = data.repository.releases.nodes;
    nodes.forEach(x => {
      releaseInfo.push(new DriverRelease(driverRepos[i].name, x.name, x.createdAt));
    });
  }

  console.log(releaseInfo.sort((a, b) => b.createdAt - a.createdAt));
}

run();
