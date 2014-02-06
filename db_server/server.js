var fs = require('fs');
var http = require('http');
var mysql = require('mysql');
var readline = require('readline');
var io = require('socket.io');

var emit = null;
var dbStatus = null;

var input = readline.createInterface({
	input:process.stdin,
	output:process.stdout,
	terminal:false
});

var server = http.createServer(function(req,res) {
	var url;
	if(url = req.url.match(/\/api\//gi)) {
		var request = req.url.split('/api/')[1];
		res.writeHead(200);
		emit('/'+request,function(data) {
			res.end(data);
		});
	} else {
		fs.readFile(__dirname+'/index.html',function(err,data) {
			if(err) {
				res.writeHead(500);
				return res.end('The file index.html could not be read. ('+err+')');
			}

			res.writeHead(200,{'Content-Type':'text/html'});
			res.end(data);
		});
	}
});

var database = mysql.createConnection({
	database:'test',
	host:'localhost',
	pass:'',
	user:'root',
});

if(!emit) emit = function(param,callback) {
	var url = param.split('/')[1];
	if(!dbStatus) {
		dbStatus = 1;
		database.connect();
	}

	database.query('SELECT * FROM '+url,function(err,rows,cols) {
		if(err) {
			callback.call(this,err.message);
			console.log('MySQL returned error: '+err);
			return err;
		} else {
			callback.call(this,JSON.stringify(rows));
		}
	});
};

io.listen(server).sockets.on('connection',function(client) {
	// database.query('INSERT INTO test (name,data) VALUES ("'+client.id+'","'+client.handshake.headers.host+'")',function(err,response) {
	// 	if(err) console.log(err);
	// 	console.log(response);
	// });

	client.emit('connected',{
		message:'Connected.',
		data:client.handshake.headers
	});
		
	input.on('line',function(line) {
		client.emit('line',{
			'sender':'[server]',
			'message':line
		});
	});
});

server.listen(8888);
