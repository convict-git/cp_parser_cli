//@authors : Priyanshu Shrivastav, Shruti Umat, Abhishek Saran

const app        = require('express')(),
      bodyParser = require('body-parser'),
      fs         = require('file-system'),
      url        = require('url'),
      sh         = require('shelljs'),
      colors     = require('colors'),
      os         = require('os');

colors.setTheme({
   debug   : 'cyan',
   display : 'white',
   error   : 'red',
   info    : 'green',
   warn    : 'yellow'
});

const user_name = os.userInfo().username.toString(); // get the user_name from os for /home/${user_name}/...
const cur_working_dir = sh.pwd(); // object
console.log(colors.debug(`currently in dir : ${cur_working_dir.toString()}`));

var echo_header_done = false;

const port = 8080; // port to listen
app.use(bodyParser.json());

app.post('/', (req, res) => {
   const data = req.body; // main body
   // console.log(colors.debug(`${JSON.stringify(data, null, 4)}`)); // show main json body

   var online_judge = url.parse(data.url).hostname,
      contest_name = data.group.split(/[\s-()]+/).join('_').split('\'').join('');
      problem_name = data.name.split(/[\s-()]+/).join('_').split('\'').join('');
      test_count = data.tests.length,
      final_path = online_judge + '/' + contest_name + '/' + problem_name,
      time_limit = parseFloat(data.timeLimit) / 1000.0,
      mem_limit = parseInt(data.memoryLimit);

   // console.log(colors.debug(`${online_judge}`));

   //Display
   //
   if (!echo_header_done) {
      echo_header_done = true;
      console.log(colors.display(`==${Date()}==`));
      console.log(colors.info.underline.bold(` *** Round name : ${contest_name} (${online_judge}) *** `));
   }
   console.log('\n');
   console.log(colors.info.bold(`Downloading problem : ${problem_name} ...`));
   console.log(colors.info.italic(`${test_count} sample test case(s) found, time limit : ${time_limit}s, memory : ${mem_limit}MB`));

   // console.log(colors.debug(`${final_path}`));

   // making folders and subfolders ---> online_judges/contest_name/problem_name
   try {
      if (!fs.existsSync(online_judge)) {
         fs.mkdirSync(online_judge);
      }
      if (!fs.existsSync(online_judge + '/' + contest_name)) {
         fs.mkdirSync(online_judge + '/' + contest_name);
      }
      if (!fs.existsSync(online_judge + '/' + contest_name + '/' + problem_name)) {
         fs.mkdirSync(online_judge + '/' + contest_name + '/' + problem_name);
      }
   } catch (err) {
      console.log(colors.error(`${err}`));
   }

   // pconfig json object to be read by tester
   var pconfig_obj = {
      test_count : test_count,
      time_limit : time_limit,
      mem_limit : mem_limit * 1000
   };

   //convert json to string and write into the file
   var pconfig_string = JSON.stringify(pconfig_obj);
   fs.writeFile(final_path + '/pconfig.json', pconfig_string, 'utf8');

   //writing test cases input and output as input + 'idx' ...
   for (var idx = 1; idx <= test_count; idx++) {
      var input_string = data.tests[idx - 1].input;
      var output_string = data.tests[idx - 1].output;

      fs.writeFile(final_path + "/input" + idx, input_string, (err) => {
         if (err) console.log(colors.error(`${err}`));
      });
      fs.writeFile(final_path + "/output" + idx, output_string, (err) => {
         if (err) console.log(colors.error(`${err}`));
      });
   }


   //get the global config file to copy template file
   var parser_config_file = '/home/' + user_name + '/.config/cpparsercli/config.json';
   // console.log(colors.debug(`parser_config_file : ${parser_config_file}`));
   try {
      //check if parser config file exists
      if (!fs.existsSync(parser_config_file)) {
         const cpp_template =
            "#include <bits/stdc++.h>\nusing namespace std;\n\nint main() {\n\treturn 0;\n}\n";

         fs.writeFile(final_path + '/' + problem_name + '.cpp', cpp_template, (err) => {
            if (err) console.log(colors.error(`${err}`));
         });
         console.log(colors.warn.underline(`Warning : config path doesnt exist, default file created`));
      }
      else { // exists so copy the template file from the given location
         var parser_config_json = require(parser_config_file);
         // console.log(colors.debug(`${parser_config_json.Template}`)); // this contains location of template file

         fs.copyFile(parser_config_json.Template, final_path + '/' + problem_name + '.cpp', (err) => {
            if (err) throw err;
            // console.log(colors.debug(`Template file copied`));
         });
      }
   } catch (err) {
      console.log(colors.error(`${err}`));
   }
   res.sendStatus(200);
});

app.listen(port, err => {
   if (err) {
      console.log(colors.error(`${err}`));
      process.exit(1);
   }
   console.log(colors.display.italic(`Listening on port ${port}\n`));
   console.log(colors.display(` ======== Welcome to cp_parser_cli ======== `));
});
