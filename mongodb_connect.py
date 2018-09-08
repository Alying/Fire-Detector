import pymongo
client = pymongo.MongoClient("mongodb://rohith:#cd3amsAXUW5UJ79@pennappscluster-shard-00-00-oxlvg.gcp.mongodb.net:27017,pennappscluster-shard-00-01-oxlvg.gcp.mongodb.net:27017,pennappscluster-shard-00-02-oxlvg.gcp.mongodb.net:27017/test?ssl=true&replicaSet=PennAppsCluster-shard-0&authSource=admin")
db = client.test