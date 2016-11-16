import * as riot from 'riot';

document.addEventListener("DOMContentLoaded", (event) => {
    riot.mount('*');
    riot.route.start(true);
});
