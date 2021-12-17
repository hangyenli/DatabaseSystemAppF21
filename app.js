const express = require('express')
const {Pool} = require("pg");
const {v4: uuidv4} = require('uuid');
const app = express()
const port = 3000
const axios = require('axios')


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
    res.send(req.body)
})

//retrieve user strategy by id
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
            res.send(result.rows ? result.rows[0] : null)
        } catch (e) {
            await client.query('ROLLBACK')
            throw e
        } finally {
            client.release()
        }
    })().catch(e => res.send(e))
})

//update user strategy
app.post('/updateUserStrategy/:userId/:strategy', async (req, res) => {
    const id = req.params.userId;
    const strategy = req.params.strategy;
    (async () => {
        const client = await pool.connect()
        try {
            await client.query('BEGIN')
            const queryText = `update userStrategy
                               set strategyName = $1
                               where userId = $2`
            await client.query(queryText, [strategy, id])

            await client.query('COMMIT')
            res.send({status: "ok"})
        } catch (e) {
            await client.query('ROLLBACK')
            throw e
        } finally {
            client.release()
        }
    })().catch(e => res.send(e))
})

//register a new user on master server
app.post('/registerUser/:userId', async (req, res) => {
    const id = req.params.userId;
    (async () => {
        const client = await pool.connect()
        try {
            await client.query('BEGIN')
            //check if user already exists
            let q0 = `select *
                      from users
                      where id = $1`
            let result = await client.query(q0, [id])
            //if user not existed, create user and default user strategy
            if (result.rowCount == 0) {
                let q1 = `insert into users
                          values ($1)`
                await client.query(q1, [id])
                let q2 = `insert into userStrategy
                          values ($1, $2)`
                await client.query(q2, [id, 'fcfs'])
                await client.query('COMMIT')
                res.send(id + ' registered successfully and default strategy set as fcfs')
            } else {
                //if user exists, do nothing
                res.send('user already existed')
            }
        } catch (e) {
            await client.query('ROLLBACK')
            throw e
        } finally {
            client.release()
        }
    })().catch(e => res.send(e))
})

//for application instance to publish task to master
app.post('/addTask', async (req, res) => {
    (async () => {
        const client = await pool.connect()
        try {
            //insert the task to taskQueue
            await client.query('BEGIN');
            const uid = uuidv4();
            const task = req.body.query;
            const userId = req.body.userId;
            const address = "http://localhost:" + req.body.address;
            const queryText = `insert into taskQueue
                               values ($1, $2, $3, $4)`
            await client.query(queryText, [uid, userId, address, task])
            //if there are sessions on, then perform changes depending on strategy
            let result = await client.query(`select *
                                             from session
                                             where userId = $1
                                               and applicationAddress != $2
                                               and status = 'on'`, [userId, address])
            const sessions = result.rows;
            //if no other session online, commit the changes to taskQueue
            if (sessions.length === 0) {
                await client.query('COMMIT')
            } else {
                //if there are other session online, force them to adapt the changes and do not commit task to taskQueue
                result = await client.query(`select *
                                             from userStrategy
                                             where userId = $1`, [userId])
                const strategy = result.rows[0].strategyname;

                //for every session
                for (let i = 0; i < sessions.length; i++) {
                    //force execute
                    axios
                        .post(sessions[i].applicationaddress + '/run', {
                            todo: task,
                            userId: userId
                        })
                        .then(res => {
                            console.log(`statusCode: ${res.status}`)
                        })
                        .catch(error => {
                            console.error(error)
                        })
                }

                //no changes to commit
                await client.query('ROLLBACK')
            }
            res.send({status: 'ok'})
        } catch (e) {
            await client.query('ROLLBACK')
            throw e
        } finally {
            client.release()
        }
    })().catch(e => res.send(e))
})

//get all session by userId and app address
app.get('/getSession/:userId/:address', async (req, res) => {
    const id = req.params.userId;
    const address = "http://localhost:" + req.params.address;

    (async () => {
        const client = await pool.connect()
        try {
            await client.query('BEGIN')
            const queryText = `select *
                               from session
                               where userId = $1
                                 and applicationAddress = $2`
            const result = await client.query(queryText, [id, address])
            await client.query('COMMIT')
            res.send(result.rows ? result.rows[0] : null)
        } catch (e) {
            await client.query('ROLLBACK')
            throw e
        } finally {
            client.release()
        }
    })().catch(e => res.send(e))
})

//get task from master by userId and application address
app.get('/getTask/:userId/:address', async (req, res) => {
    const id = req.params.userId;
    const address = "http://localhost:" + req.params.address;
    (async () => {
        const client = await pool.connect()
        try {
            await client.query('BEGIN')
            const queryText = `select *
                               from taskqueue
                               where userId = $1
                                 and applicationAddress != $2`
            const result = await client.query(queryText, [id, address])
            await client.query('COMMIT')
            res.send(result.rows ? result.rows : [])
        } catch (e) {
            await client.query('ROLLBACK')
            throw e
        } finally {
            client.release()
        }
    })().catch(e => res.send(e))
})

//notify master some tasks are done and should be removed from taskQueue
app.post('/deleteTask', async (req, res) => {
    const ids = req.body['ids'];
    (async () => {
        const client = await pool.connect()
        try {
            await client.query('BEGIN')
            for (let i = 0; i < ids.length; i++) {
                let q = `delete
                         from taskqueue
                         where id = $1`
                await client.query(q, [ids[i]])
                await client.query('COMMIT')

            }
            res.send('ok')
        } catch (e) {
            await client.query('ROLLBACK')
            throw e
        } finally {
            client.release()
        }
    })().catch(e => res.send(e))
})

//update the current status of the session
app.post('/updateSession', async (req, res) => {
    const rb = req.body;
    (async () => {
        const client = await pool.connect()
        try {
            await client.query('BEGIN')
            //check if session with the same userId and App address exists before
            let query = `select *
                         from session
                         where userId = $1
                           and applicationAddress = $2`
            let result = await client.query(query, [rb.userId, rb.applicationAddress])
            if (result.rowCount == 0) {
                //if never existed before, record application address and create session
                query = `insert into userApplicationAddress
                         values ($1, $2)`
                result = await client.query(query, [rb.userId, rb.applicationAddress])
                query = `insert into session
                         values ($1, $2, $3)`
                result = await client.query(query, [rb.userId, rb.applicationAddress, 'on'])
            } else {
                //if existed before, just perform update (on/off)
                query = `update session
                         set status = $3
                         where userId = $1
                           and applicationAddress = $2`
                await client.query(query, [rb.userId, rb.applicationAddress, rb.status])
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