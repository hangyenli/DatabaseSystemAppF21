const express = require('express')
const {Pool} = require("pg");
const {v4: uuidv4} = require('uuid');
const app = express()
const port = 3000

app.use(express.json())    // <==== parse request body as JSON

const credentials = {
    user: "master_admin",
    host: "localhost",
    database: "master_database",
    password: "master_password",
    port: 5432,
};
const pool = new Pool(credentials);


app.get('/', async (req, res) => {
    res.send({status: 'ok'})
})
app.post('/test', async (req, res) => {
    console.log("post")
    console.log(req.body)
    res.send(req.body)
})

app.get('/getUserStrategy/:userId', async (req, res) => {
    const id = req.params.userId;
    (async () => {
        const client = await pool.connect()
        try {
            await client.query('BEGIN')
            const queryText = `select *
                               from userStrategy
                               where userId = $1`
            const result = await client.query(queryText, [id])
            await client.query('COMMIT')
            res.send(result.rows ? result.rows : null)
        } catch (e) {
            await client.query('ROLLBACK')
            throw e
        } finally {
            client.release()
        }
    })().catch(e => res.send(e))
})

app.post('/registerUser/:userId', async (req, res) => {
    const id = req.params.userId;
    (async () => {
        const client = await pool.connect()
        try {
            await client.query('BEGIN')
            let q1 = `insert into users
                      values ($1)
                      returning id`
            await client.query(q1, [id])
            let q2 = `insert into userStrategy
                      values ($1, $2)`
            await client.query(q2, [id, '71e56d8e-f665-40ca-b812-3b820dd671cb'])
            await client.query('COMMIT')
            res.send(id + ' registered successfully and default strategy set as fcfs')
        } catch (e) {
            await client.query('ROLLBACK')
            throw e
        } finally {
            client.release()
        }
    })().catch(e => res.send(e))
})

app.post('/updateSession',async (req,res)=>{
    const rb = req.body;
    (async () => {
        const client = await pool.connect()
        try {
            await client.query('BEGIN')
            let query = `select *
                               from session
                               where userId = $1 and applicationAddress=$2`
            let result = await client.query(query, [rb.userId,rb.applicationAddress])
                            console.log(result);
            if (result.rowCount == 0){
                console.log('sss')
                query = `insert into userApplicationAddress values ($1,$2)`
                result = await client.query(query, [rb.userId,rb.applicationAddress])
                query = `insert into session values ($1,$2,$3)`
                result = await client.query(query, [rb.userId,rb.applicationAddress,'on'])
                console.log(result);
            }else{
                query = `update session set status = $3 where userId = $1 and applicationAddress = $2`
                await client.query(query, [rb.userId,rb.applicationAddress, rb.status])
            }
            await client.query('COMMIT')
            res.send(id + ' successfully added session')
        } catch (e) {
            await client.query('ROLLBACK')
            throw e
        } finally {
            client.release()
        }
    })().catch(e => res.send(e))
})

app.listen(port, () => {
    console.log(`Master server listening at http://localhost:${port}`)
})