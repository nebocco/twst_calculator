let express = require('express');
let path = require('path');
let serveStatic = require('serve-static');
let redirectSSL = require('redirect-ssl');
// import sslRedirect from 'heroku-ssl-redirect'

const app = express();
app.use(redirectSSL);
app.use(serveStatic(__dirname + "/dist"));
let port = process.env.PORT || 5000;
app.listen(port);
console.log('server started '+ port);