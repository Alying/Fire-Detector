console.log("test1");

const client = stitch.Stitch.initializeDefaultAppClient('firevideosdb-yrpwy');
const db = client.getServiceClient(stitch.RemoteMongoClient.factory, 'mongodb-atlas').db('VideosDB');

console.log("test2");

client.auth.loginWithCredential(new stitch.AnonymousCredential()).then(user => {
    console.log(user);
    db.collection('VideosCollection').find().toArray()
});

function addToDB(){
    console.log("test3");
    const id = document.getElementById("id").value;
    const url = document.getElementById("url").value;
    const videostream = document.getElementById("videostream").value;

    const doc = { id, url, videostream }; 

    //var dict = {"id" : document.getElementById("id").value, "url": document.getElementById("url").value,"videostream": document.getElementById("videostream").value}
    client.auth.loginWithCredential(new stitch.AnonymousCredential()).then(user => db.collection('VideosCollection').insertOne(doc));
}
function getAllPosts(){
    client.auth.loginWithCredential(new stitch.AnonymousCredential()).then(user => db.collection('VideosCollection').find());
}

function updateToDB() {
    console.log("test3");     
    const vid_id = document.getElementById("id").value;
    const vid_url = document.getElementById("url").value;
    const vid_videostream = document.getElementById("videostream").value;

    const doc = { vid_id, vid_url, vid_videostream }; 


    //client.auth.loginWithCredential(new stitch.AnonymousCredential()).then(user => 
    db.collection('VideosCollection').updateOne({id: vid_id}, {$set:{id: vid_id, url:vid_url, videostream:vid_videostream}}, {upsert:true})
    .then(() => 
    db.collection('VideosCollection').find().asArray()
  ).then(docs => {
      console.log("Found docs", docs)
      console.log("[MongoDB Stitch] Connected to Stitch")
  }).catch(err => {
    console.error(err)
  });

}
