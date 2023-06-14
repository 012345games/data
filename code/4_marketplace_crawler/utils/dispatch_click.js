const CDP = require('chrome-remote-interface');

CDP((client) => {

  function getRandomInt(max) {
    return Math.floor(Math.random() * Math.floor(max));
  };

  count = 100;
  // const keys = ['U+0020','U+0057','U+0041','U+0044','U+0053'];
  const keys = ['20','57','41','44','53'];
  const option_key = {};
  const options = {
    x: 42,
    y: 42,
    button: 'left',
    clickCount: 1
  };
  setTimeout(rndkey, 1000);



  function rndkey(){
    option_key.keyIdentifier = keys[Math.floor(Math.random() * (keys.length - 1))];
    Promise.resolve().then(() => {
      option_key.type = 'rawKeyDown';
      return client.Input.dispatchKeyEvent(option_key);
    }).then(() => {
      option_key.type = 'keyUp';
      return client.Input.dispatchKeyEvent(option_key);
    }).catch((err) => {
      console.error(err);
    });
    console.log('pressed', option_key.keyIdentifier);
    count--;
    if(count){
      setTimeout(rndkey, 200);
    }
  };

  function rndclick(){
    options.x = getRandomInt(1000);
    options.y = getRandomInt(1000);

    Promise.resolve().then(() => {
      options.type = 'mousePressed';
      return client.Input.dispatchMouseEvent(options);
    }).then(() => {
      options.type = 'mouseReleased';
      return client.Input.dispatchMouseEvent(options);
    }).catch((err) => {
      console.error(err);
    });
    console.log('clicked', options.x, options.y, clickcount);
    count--;
    if(count){
      setTimeout(rndclick, 200);
    }
  };

}).on('error', (err) => {
  console.error(err);
});
