const Profile = require('cpuprofile').Profile;
const args = process.argv.slice(2);
const profileFile = args.shift() || '';
// input = `{${profileFile}\n}`;

// read and parse a .cpuprofile file
let content = require('fs').readFileSync(profileFile, {encoding: 'utf8'});
let parsed = JSON.parse(content);
console.log(parsed);

// create Profile
let profile = Profile.createFromObject(parsed);

// generate formatted overview on self and total times
let output = profile.formattedBottomUpProfile();

require('fs').writeFileSync(profileFile + '.bottomup' , JSON.stringify(output, null, 2));
