var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

/* GET another page */
router.get('/a', function(req, res, next) {
  res.render('another', { title: 'Express' });
});

module.exports = router;
