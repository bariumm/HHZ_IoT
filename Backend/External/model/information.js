var SchemaObject = require('schema-object');

var sensor = new SchemaObject({
    sensorName: String,
    location: String,
    unit: String,
    value: String,
    date: Date
});

module.exports = {
    sensorSchema: sensor
}