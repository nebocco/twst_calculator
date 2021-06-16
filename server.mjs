import express from 'express';
import path from 'path';
import serveStatic from 'serve-static';
import sslRedirect from 'heroku-ssl-redirect'

const app = express();
app.use(sslRedirect())
app.use(serveStatic(__dirname + "/dist"));
let port = process.env.PORT || 5000;
app.listen(port);
console.log('server started '+ port);