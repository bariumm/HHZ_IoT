var mysql = require('mysql');

var connection = mysql.createConnection({
    host     : 'localhost',
    user     : 'hhz',
    password : 'HHZ.Digital17',
    database : 'digital_hhz'
});

function connect() {
    if(connection.state === 'disconnected'){
        //connection.connect();
    }
}

function end() {
    //connection.end();
}

function test(callback) {
    connect();
    var query = 'SELECT 1 + 1 AS solution';
    connection.query(query, function (error, results, fields) {
        if (error) throw error;
        console.log('The solution is: ', results[0].solution);
        if(results[0].solution == '2'){
            callback('Database is working')
        } else {
            callback(results[0])
            // callback('Database connection failed')
        }
    });
    end();
}

function saveSensorData(data, callback) {
    //var query = 'INSERT INTO states (state_id, domain, entity_id, state, attributes, event_id, last_changed, last_updated, created) VALUES (';
    var query = 'INSERT INTO states (';

    var keys = '';
    var values = '';

    var first = true;
    for (var key in data) {
        if(first){
            first = false;

            keys = keys + key;
            values = values + "'" + data[key] + "'";
        } else {
            keys = keys + ',' + key;
            values = values + ",'" + data[key] + "'";
        }
    }

    query = query + keys + ') VALUES (' + values + ');';
    // console.log('Query: ' + query)
    // return(true)

    connection.query(query, function (error, results, fields) {
        if (error){
            console.log('Error saveSensorData: ' + error);
            callback(error);
        } else {
            callback(true)
        }
    });
}

function getSensorData(id, callback) {
    var query = 'SELECT * from states WHERE entity_id = "' + id + '" ORDER BY created DESC LIMIT 1';
    connection.query(query, function (error, results, fields) {
        if (error){
            console.log('Error getSensorData: ' + error);
            callback(error);
        } else {
            callback(results)
        }
    });
}

function getAllSensorIds(callback) {
    var query = 'SELECT DISTINCT(entity_id) from states';
    connection.query(query, function (error, results, fields) {
        if (error){
            console.log('Error getAllSensorIds: ' + error);
            callback(error);
        } else {
            callback(results)
        }
    });
}

function getNews(days, callback) {
    var query = 'SELECT * from hhz_news WHERE created >= CURDATE() - INTERVAL ' + days + ' DAY';
    connection.query(query, function (error, results, fields) {
        if (error){
            console.log('Error getNews: ' + error);
            callback(error);
        } else {
            callback(results)
        }
    });
}

function addNews(message, url, callback) {
    var query = 'INSERT INTO hhz_news (message, URL, created) VALUES ("' + message + '", "' + url + '", now());';
    connection.query(query, function (error, results, fields) {
        if (error){
            console.log('Error addNews: ' + error);
            callback(error);
        } else {
            callback(true)
        }
    });
}

module.exports = {
    connect: connect,
    end: end,
    saveSensorData: saveSensorData,
    getSensorData: getSensorData,
    getAllSensorIds: getAllSensorIds,
    getNews: getNews,
    addNews: addNews,
    test: test
}