// playground-5.mongodb.js
const { MongoClient } = require('mongodb');

const password = process.env.MONGO_PWD;
if (!password) {
  console.error('Set MONGO_PWD environment variable first.');
  process.exit(1);
}

// encode in case the password has special chars
const uri = `mongodb+srv://kanagalakarthik2468_db_user:${encodeURIComponent(password)}@cluster0.tkagiyn.mongodb.net/?retryWrites=true&w=majority`;

const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });

async function run() {
  try {
    await client.connect();
    console.log('Connected to MongoDB Atlas');
    const db = client.db('test'); // replace with your DB name
    const collections = await db.listCollections().toArray();
    console.log('Collections:', collections.map(c=>c.name));
  } catch (err) {
    console.error('Connection error:', err);
  } finally {
    await client.close();
  }
}

run();
