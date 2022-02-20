'use strict';

const express = require('express');
const { parse } = require('request/lib/cookies');
const app = express();
app.use(express.json());

// Your code starts here. Placeholders  for .get and .post are provided for
// your convenience.

let condidates = [];


app.post('/candidates', function(req, res) {
    let condidate= req.body;
    condidates.push(condidate);
    res.send(200);
});




app.get('/candidates/search', function(req, res) {
  let R ='';
  let SK = req.query.skills.toString();
  let array = SK.split(',');
  console.log(array);

  arry_of_nb_of_skills



    for (let j = 0; j < condidates.length; j++) {
      let cond = condidates[j];
      let z= 0;

      for (let i = 0; i < array.length; i++) {
        let s = array[i];
        

      }
      

      if (cond.skills[z] == s) {
        nb_of_skills++;
      }
    }
   
    
  

  res.send(200);
});
 app.listen(process.env.HTTP_PORT || 3000);