var express = require('express');
var router = express.Router();
var db = require('../config/mySQL');

var temp = [];

var password = 'qhdwu65dqwd35';

var newsAuth= 'HHZ.News';

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Digital HHZ' });
});

//-------------------------------
// ---------- SENSORS -----------
//-------------------------------

router.post('/data/post', function (req, res) {
    if(req.body.pass==password) {
        var eventId = req.body.event_id;
        if(!eventId){
            eventId = -1;
        }
        var result = {
            state_id: req.body.state_id,
            domain: req.body.domain,
            entity_id: req.body.entity_id,
            state: req.body.state,
            attributes: req.body.attributes,
            event_id: eventId,
            last_changed: req.body.last_changed,
            last_updated: req.body.last_updated,
            created: req.body.created
        };
        db.connect();
        db.saveSensorData(result,function (data) {
            if(data==true){
                res.send(true)
            } else {
                res.send(false)
            }
        });
    } else {
        res.send('Authentication failed')
    }
});

router.get('/data/get', function (req, res) {
    if(req.query.pass==password || true) {
        db.connect();
        db.getSensorData(req.query.id, function (data) {
            //db.end();
            res.send(data)
        })
    }
});

router.get('/data/getAll', function (req, res) {
    if(req.query.pass==password || true) {
        db.connect();
        db.getAllSensorIds(function (data) {
            var sensors = [];
            data.forEach(function (value, index) {
                var first = true;
                db.getSensorData(value.entity_id, function (sensor) {
                    sensors.push(sensor);
                    if(index==data.length-1){
                        //db.end();
                        res.send(sensors)
                    }
                });
                first = false;
            })
        })
    }
});

router.get('/data/getAllIds', function (req, res) {
    if(req.query.pass==password || true) {
        db.connect();
        db.getAllSensorIds(function (data) {
            db.end();
            res.send(data)
        })
    }
});

//-------------------------------
// ------------ NEWS ------------
//-------------------------------

router.get('/news/get', function (req, res) {
    if(req.query.pass==password || true) {
        var days = 14;
        if(req.query.days){
            days = req.query.days
        }
        db.connect();
        db.getNews(days, function (data) {
            db.end();
            res.send(data)
        })
    }
});

router.get('/news', function(req, res, next) {
    res.render('startNews', { });
});

router.post('/news', function(req, res, next) {
    if(req.body.auth==newsAuth){
        res.render('addNews', {auth: req.body.auth });
    } else {
        res.render('startNews', { });
    }
});

router.post('/addNews', function(req, res, next) {
    if(req.body.auth==newsAuth || true){
        db.connect();
        db.addNews(req.body.message, req.body.url, function (data) {
            if(data==true){
                res.render('addNews', {auth: req.body.auth, message: 'News added' });
            } else {
                res.render('addNews', {auth: req.body.auth, message: 'Error on saving news' });
            }
            db.end();
        })
    } else {
        res.render('addNews', {auth: req.body.auth, message: 'Error on saving news' });
    }
});

router.get('/test', function (req, res) {
    db.test(function (data) {
        res.send(data)
    })
});

module.exports = router;
