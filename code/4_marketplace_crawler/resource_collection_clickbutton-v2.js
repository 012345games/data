/**
GT -- full profiling, no in-depth crawling (homepage only)
*/
const Chrome = require('chrome-remote-interface');
const chrome_launcher = require('chrome-launcher');
const fs = require('fs');
const request = require('request');
const artifical_delay = n => new Promise(resolve => setTimeout(resolve, n));
const args = process.argv.slice(2);

var TRACE_CATEGORIES = ["devtools.timeline"];

var rawEvents = [];

const trace_path = 'PATH_TRACING/';
const static_script = 'PATH_STATIC_SCRIPT/';
const dynamic_script = 'PATH_DYNAMIC_SCRIPT/';
const dom_out = './PATH_DOM/';
const cookie_out = 'PATH_COOKIES/';
// cpu profiler
const profile_out = 'PATH_PROFILER/';
// screenshots
const screenshot_out = "PATH_SCREENSHOT/";

console.log('Args', args);

const url = args.shift() || '';
console.log("visiting: ", url);

if ( !url ) {
  process.stderr.write('No URL specified\n');
  process.exit(1);
}

if (args.length > 6){
  var cdp_port = parseInt(args[6]);
}
else{
  var cdp_port = 9222;
}
console.log("Chrome Debugging Protocol port: ", cdp_port);

inputs = `{${url}\n}`;
fs.appendFileSync('./crawled_sites.txt', inputs);

Chrome({port: cdp_port}, function(chrome){
  with(chrome) {
    // const network_trace = generateFilename(url);
    const network_trace = args[0]; //passing the folder name as cli argument
    console.log('Args', args);
    Page.enable();
    Network.enable();
    Profiler.enable();
    Debugger.enable();
    DOM.enable();
    Runtime.enable();

    //flush current cache and cookies
    Network.clearBrowserCookies();
    Network.clearBrowserCache();

    if (!fs.existsSync(static_script+network_trace)){

      fs.mkdirSync(static_script+network_trace);
      fs.mkdirSync(
          +network_trace);
      fs.mkdirSync(screenshot_out+network_trace);
      fs.mkdirSync(trace_path+network_trace); }

      Debugger.scriptParsed((params) =>{
        Debugger.getScriptSource({
          scriptId: params.scriptId
        }, function(err, msg){
          if (err){
            message = `{${url}\t${msg}\n}`
            fs.appendFileSync('./error_file.txt', message);}

            else{
              stringo = JSON.stringify(msg, null, 2);
              fs.writeFile(static_script+network_trace+ '/'+params.scriptId, stringo, (err)=>{
                if (err) throw err;
              });

              record = `${url}\t${params.url}\t${params.scriptId}\n`;
              fs.appendFileSync(static_script+network_trace+'/'+network_trace, record);
            }}
          )

        });


        Network.requestWillBeSent((params) =>{
          //explicit request of dynamically loaded js (remove filter .js to dump ALL dynamically loaded contents!)
          if (params.request.url.endsWith(".js")){
            request(params.request.url, function(error, response, body){
              let json = JSON.stringify(body);
              fs.writeFile(dynamic_script + network_trace + "/" + params.requestId,json, (err) =>{
                if (err) throw err;
              }); })
            }
            event_trace = JSON.stringify(params, null, 2);
            fs.appendFileSync(trace_path+network_trace+"/"+ network_trace +'.reqtrace', event_trace);
          });

          Network.responseReceived((params) =>{

            event_trace = JSON.stringify(params, null, 2);
            fs.appendFileSync(trace_path+network_trace +"/"+network_trace +'.restrace', event_trace);
          });

          Network.webSocketCreated((params) =>{
            event_trace = JSON.stringify(params, null, 2);
            fs.appendFileSync(trace_path+network_trace+"/"+ network_trace +'.wstrace', event_trace);
          });

          Network.webSocketClosed((params) =>{
            event_trace = JSON.stringify(params, null, 2);
            fs.appendFileSync(trace_path+network_trace+"/"+ network_trace +'.wstrace', event_trace);
          });

          Network.webSocketFrameSent((params) =>{
            event_trace = JSON.stringify(params, null, 2);
            fs.appendFileSync(trace_path+network_trace+"/"+ network_trace +'.wstrace', event_trace);
          });

          Tracing.start({
            "categories":   TRACE_CATEGORIES.join(','),
            "options":      "sampling-frequency=1000"  // 1000 is default and too slow. --> GT setting to 100ms?
          });

          //by default, https
          var navigation_url = "https://".concat(url);
          if (url.includes('httpplay')){
            var navigation_url = "http://".concat(url);
          }
          Page.navigate({url: navigation_url});

          //full exp duration
          const timeout_ms =  parseInt(args[1]);
          console.log("Timeout (total)", timeout_ms);

          //timeout (click on button)
          const timeout_click_ms =  parseInt(args[2]);
          if(timeout_click_ms!=-1){
            console.log("Timeout (to click)", timeout_click_ms);
          }

          //button to click (match on id or class)
          const match_on = args[3];
          const button_target = args[4].replace("[]"," ");
          if (match_on!='-1' && button_target!='-1'){
            console.log("Button " + match_on + " (to start game)", button_target);
            setTimeout(ttclick, timeout_click_ms);
            //just in case the deault splash-button appears
            setTimeout(ttclick_default_button, timeout_click_ms+5000);

          }

          async function ttclick(){
            if(match_on == "id"){
              console.log(`document.getElementById('` + button_target + `').click()`)
              await Runtime.evaluate({
                expression: `document.getElementById('` + button_target + `').click()`
              })
            }
            if(match_on == "class"){
              console.log(`document.getElementsByClassName('` + button_target + `')[0].click()`)
              await Runtime.evaluate({
                expression: `document.getElementsByClassName('` + button_target + `')[0].click()`
              })
            }
            if(match_on == "tag"){
              console.log(`document.getElementsByTagName('` + button_target + `')[0].click()`)
              await Runtime.evaluate({
                expression: `document.getElementsByTagName('` + button_target + `')[0].click()`
              })
            }
          }

          async function ttclick_default_button(){
              console.log(`document.getElementById('gdsdk__splash-button').click()`)
              await Runtime.evaluate({
                expression: `document.getElementById('gdsdk__splash-button').click()`
              })
          }

          //initialise rnd keys
          const keys = ['U+0020','U+0057','U+0041','U+0044','U+0053'];

          //initialise click/key
          const options = {
            x: 43,
            y: 43,
            button: 'left',
            clickCount: 1
          };
          const option_key = {};
          const timeout_rndclick_ms =  parseInt(args[5]);

          //get max click coordinates (based on current inner-window size)
          var max_x = 1000;
          getWidth().then((a) =>{
            console.log("Inner width", a);
            const max_x = a;
          }).catch((err) => {
            console.error(err);
          });
          var max_y = 1000;
          getHeight().then((a) =>{
            console.log("Inner heigth", a);
            const max_y = a;
          }).catch((err) => {
            console.error(err);
          });

          //number of random keys/clicks
          var clickcount = (timeout_ms-timeout_rndclick_ms)/200; //1 every 200 ms

          //start timer
          if(timeout_rndclick_ms!='-1'){
            setTimeout(rndkey, timeout_rndclick_ms);
          }

          //number of screenshots
          var nscreenshots = timeout_ms/10000 -1; //1 every 10s
          var screenshot_id = 0;
          setTimeout(getScreenshot, 10000)

          Profiler.start();  // setTimeout(tt,timeoutms) finishes function after the whole experiment ends

          //final timeout (resource collection)
          setTimeout(tt, timeout_ms); // should be 45 secs based on OutGuard paper [WWW'19] should suffice for capturing malicious behaviours (cryptojacking)
          function tt(){
            //GT -- modified
            Profiler.stop({},
              function(err, msg){
                if (err){
                  message = `{${url}\t${msg}\n}`
                  fs.appendFileSync('./error_file.txt', message);}

                  else{
                    stringo = JSON.stringify(msg, null, 2);
                    fs.writeFile(profile_out+network_trace+ '.cpuprofile', stringo, (err)=>{
                      if (err) throw err;
                    });
                  }}
                );
            Network.getAllCookies({},
              function(err, msg){
                if (err){
                  message = `{${url}\t${msg}\n}`
                  fs.appendFileSync('./error_file.txt', message);}

                  else{
                    stringo = JSON.stringify(msg, null, 2);
                    fs.writeFile(cookie_out+network_trace+ '.cookies', stringo, (err)=>{
                      if (err) throw err;
                    });
                  }}
                );
                DOM.getDocument({
                  "depth":   -1,
                  "pierce":   true
                },
                function(err, msg){
                  if (err){
                    message = `{${url}\t${msg}\n}`
                    fs.appendFileSync('./error_file.txt', message);
                    console.log(message);}
                    else{
                      stringo = JSON.stringify(msg, null, 2);
                      console.log(dom_out+network_trace.replace(/[\/]/g,"__")+ '.flatteneddom');
                      fs.writeFile(dom_out+network_trace.replace(/[\/]/g,"__")+ '.flatteneddom', stringo, (err)=>{
                        if (err) throw err;
                      });
                      // chrome.close();
                    }}
                  );
                  Tracing.end();
                }

                Tracing.tracingComplete(function () {
                  //not writing devtools trace file to save space!
                  // fs.writeFileSync(trace_path+network_trace +"/"+network_trace + '.devtools.trace' , JSON.stringify(rawEvents, null, 2));
                  console.log('Not writing trace file (save space): ' + trace_path+network_trace +"/"+network_trace + '.devtools.trace');
                  chrome.close();
                });

                Tracing.dataCollected(function(data){
                  var events = data.value;
                  // rawEvents = rawEvents.concat(events);
                });

                function generateFilename(address){
                  const dummy_value = address.replace('http://', '');
                  const fname = `${dummy_value}-${Date.now()}`;
                  return fname
                }

                function rndclick(){
                  options.x = getRandomInt(max_x);
                  options.y = getRandomInt(max_y);
                  Promise.resolve().then(() => {
                    options.type = 'mousePressed';
                    return Input.dispatchMouseEvent(options);
                  }).then(() => {
                    options.type = 'mouseReleased';
                    return Input.dispatchMouseEvent(options);
                  }).catch((err) => {
                    console.error(err);
                  });
                  console.log("clicked:",options.x, options.y, clickcount);
                  clickcount--;
                  if(clickcount){
                    if (Math.random()>0.5){
                      setTimeout(rndkey, 200);
                    }
                    else{
                      setTimeout(rndclick, 200);
                    }
                  }
                };

                function rndkey(){
                  option_key.keyIdentifier = keys[Math.floor(Math.random() * (keys.length - 1))];
                  Promise.resolve().then(() => {
                    option_key.type = 'rawKeyDown';
                    return Input.dispatchKeyEvent(option_key);
                  }).then(() => {
                    option_key.type = 'keyUp';
                    return Input.dispatchKeyEvent(option_key);
                  }).catch((err) => {
                    console.error(err);
                  });
                  console.log('pressed', option_key.keyIdentifier);
                  clickcount--;
                  if(clickcount){
                    if (Math.random()>0.5){
                      setTimeout(rndkey, 200);
                    }
                    else{
                      setTimeout(rndclick, 200);
                    }
                  }
                };

                function getRandomInt(max) {
                  return Math.floor(Math.random() * Math.floor(max));
                };

                function getWidth(){
                  return Runtime.evaluate({expression: `window.innerWidth`}).then((result) => {
                    const a = result.result.value;
                    return a;
                  });
                };

                function getHeight(){
                  return Runtime.evaluate({expression: `window.innerHeight`}).then((result) => {
                    const a = result.result.value;
                    return a;
                  });
                };

                function getScreenshot(){
                  Page.captureScreenshot({}, function(err, msg){
                    if (err){
                      message = `{${url}\t${msg}\n}`
                      fs.appendFileSync('./error_file.txt', message);}
                    else{
                        stringo = JSON.stringify(msg.data, null, 2);
                        var buf = Buffer.from(stringo.substring(1,stringo.length-1), 'base64');
                        fs.writeFile(screenshot_out+network_trace+'/'+ screenshot_id.toString() +'.png',
                                     buf, (err)=>{
                          if (err) throw err;
                        });
                      }
                    screenshot_id++;
                    nscreenshots--;
                    if (nscreenshots){
                      setTimeout(getScreenshot, 10000);
                    }
                    });
                };

              //with chrome ends here
              }
            }).on('error', function(e){

              console.error('Cannot connect to Chrome');
            });
