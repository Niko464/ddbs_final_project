import Surreal from 'surrealdb.js';

const db = new Surreal('http://127.0.0.1:8000/rpc');

async function setupDb() {
	try {
		await db.signin({
			user: 'root',
			pass: 'root'
		})

		await db.use('test', 'test');
	} catch (e) {
		console.error('ERROR While setting up the database.', e);
	}
}

async function main() {

	await setupDb();

	/*
	Example:

	let created = await db.create("person", {
		title: 'Founder & CEO',
		name: {
			first: 'Tobie',
			last: 'Morgan Hitchcock',
		},
		marketing: true,
		identifier: Math.random().toString(36).substr(2, 10),
	});

	let groups = await db.query('SELECT marketing, count() FROM type::table($tb) GROUP BY marketing', {
		tb: 'person',
	});

	console.log(groups);
	groups[0].result.forEach(element => {
		console.log(element);
	});*/
}


await main();