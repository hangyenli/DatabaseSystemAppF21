import {Client} from 'pg'
import {v4 as uuidv4} from 'uuid';

function log(data: any) {
    console.log(data);
}

type Query = {
    text: string;
    values?: Array<string>;
};

class DB {
    async query(query: Query) {
        const client = new Client({
            user: 'project',
            host: 'localhost',
            database: 'project',
            password: 'project',
        });
        try {
            await client.connect();
            const ret = await client.query(query)
            await client.end();
            if (ret.command === 'INSERT'){
                   return 'INSERT SUCCESS'
            }else{
                return ret.rows ? ret.rows : null
            }
        } catch (e: any) {
            return e.message
        }
    }
}


async function main() {
    const db = new DB();
    //usage of insert query
    let query: Query = {
        text: 'INSERT INTO users(id,name) VALUES($1,$2)',
        values: [uuidv4(), 'honghao']
    }
    let ret = await db.query(query);
    log(ret)

    //usage of select query
    query = {
        text: 'select * from users'
    }
    ret = await db.query(query);
    log(ret)
}


main().then(() => {
    console.log('Program executed successfully')
})
